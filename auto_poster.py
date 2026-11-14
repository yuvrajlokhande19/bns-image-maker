"""
BNS Daily Auto-Poster for Instagram & X (Twitter) via Composio & Tweepy
Publishes feed posts, stories & tweets from v2/bns_posts.json using rendered images in v2/output/
"""
import os
import sys
import json
import time
import re
import urllib.error
import urllib.request
import urllib.parse
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Paths
BASE_DIR = Path(__file__).resolve().parent
POSTS_FILE = BASE_DIR / "v2" / "bns_posts.json"
OUTPUT_DIR = BASE_DIR / "v2" / "output"
STATE_FILE = BASE_DIR / "v2" / "posting_state.json"
LOCAL_ENV_FILE = BASE_DIR / ".env"

def load_local_env():
    """Load local .env if present."""
    if LOCAL_ENV_FILE.exists():
        with open(LOCAL_ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in os.environ:
                        os.environ[k.strip()] = v.strip().strip('"').strip("'")

load_local_env()

# Instagram (Composio) Config
COMPOSIO_MCP_URL = "https://connect.composio.dev/mcp"
COMPOSIO_ACCOUNT = os.getenv("COMPOSIO_ACCOUNT", "linpane_legal_services")
GITHUB_REPO = os.getenv("GITHUB_REPO", "yuvrajlokhande19/bns-image-maker")

# Twitter / X Credentials (from environment or .env)
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

def get_composio_api_key():
    key = os.getenv("COMPOSIO_API_KEY")
    if not key:
        raise ValueError("Missing COMPOSIO_API_KEY! Please set it in .env or environment.")
    return key

class ComposioToolError(RuntimeError):
    """Raised when a Composio tool invocation fails with extracted nested details."""
    def __init__(self, message: str, is_auth_error: bool = False):
        super().__init__(message)
        self.is_auth_error = is_auth_error


AUTH_ERROR_MARKERS = (
    "oauthexception",
    '"code":190',
    '"code": 190',
    "error validating access token",
    "has not authorized application",
    "status 401",
    "http 401",
    "invalid oauth access token",
)

TRANSIENT_ERROR_MARKERS = (
    "timeout",
    "timed out",
    "temporarily unavailable",
    "media id is not available",
    "not ready",
    "please wait",
    "connection reset",
    "remote end closed",
    "http 500",
    "http 502",
    "http 503",
    "http 504",
    "status 500",
    "status 502",
    "status 503",
    "status 504",
)


def _is_auth_failure(msg: str) -> bool:
    low = msg.lower()
    return any(m in low for m in AUTH_ERROR_MARKERS)


def _is_transient_failure(exc: Exception) -> bool:
    if isinstance(exc, ComposioToolError) and exc.is_auth_error:
        return False
    if isinstance(exc, (urllib.error.URLError, TimeoutError, ConnectionError)):
        if isinstance(exc, urllib.error.HTTPError):
            return exc.code >= 500 or exc.code == 429
        return True
    low = str(exc).lower()
    if _is_auth_failure(low):
        return False
    return any(m in low for m in TRANSIENT_ERROR_MARKERS)


def _extract_composio_errors(parsed: dict) -> list[str]:
    """Collect unique nested response/tool errors so batch wrappers don't hide Meta's reason."""
    details = []

    def _add(val):
        if val:
            s = str(val)
            if s not in details:
                details.append(s)

    results = parsed.get("data", {}).get("results", []) or []
    for item in results:
        if not isinstance(item, dict):
            continue
        resp = item.get("response")
        if isinstance(resp, dict):
            if resp.get("error"):
                _add(resp.get("error"))
            elif not resp.get("successful", True) and resp.get("data"):
                _add(resp.get("data"))
        _add(item.get("error"))
    _add(parsed.get("error"))
    return details


def call_composio_mcp(tool_name: str, arguments: dict) -> dict:
    key = get_composio_api_key()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-consumer-api-key": key
    }
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time()),
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    req = urllib.request.Request(COMPOSIO_MCP_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            text = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        raise ComposioToolError(f"Composio HTTP {e.code}: {body}", is_auth_error=(e.code == 401 or _is_auth_failure(body)))
    match = re.search(r"data: (\{.*\})", text)
    if match:
        return json.loads(match.group(1))
    raise ValueError(f"Invalid SSE stream response: {text[:200]}")


def execute_composio_tool(tool_slug: str, arguments: dict) -> dict:
    res = call_composio_mcp("COMPOSIO_MULTI_EXECUTE_TOOL", {
        "tools": [
            {
                "tool_slug": tool_slug,
                "account": COMPOSIO_ACCOUNT,
                "arguments": arguments
            }
        ]
    })
    raw_text = res.get("result", {}).get("content", [{}])[0].get("text", "")
    if not raw_text:
        raise ComposioToolError(f"Empty Composio response for {tool_slug}: {res}")
    parsed = json.loads(raw_text)
    if not parsed.get("successful"):
        details = _extract_composio_errors(parsed)
        combined = " | ".join(details) if details else raw_text[:400]
        is_auth = _is_auth_failure(combined)
        hint = (
            f" -> Instagram OAuth token for '{COMPOSIO_ACCOUNT}' expired or was revoked. "
            "Reconnect it in Composio (Instagram toolkit) and re-run."
            if is_auth else ""
        )
        raise ComposioToolError(f"Composio execution failed ({tool_slug}): {combined}{hint}", is_auth_error=is_auth)

    results = parsed.get("data", {}).get("results", [])
    if results and "response" in results[0]:
        inner = results[0]["response"]
        if not inner.get("successful", True):
            err_msg = str(inner.get("error") or inner.get("data") or inner)
            is_auth = _is_auth_failure(err_msg)
            raise ComposioToolError(f"Tool error ({tool_slug}): {err_msg}", is_auth_error=is_auth)
        return inner.get("data", {})
    return parsed.get("data", {})


def run_with_retry(label: str, fn, max_attempts: int = 3):
    """Retry transient network/Graph API processing glitches, fail fast on OAuth/4xx errors."""
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            if attempt >= max_attempts or not _is_transient_failure(exc):
                raise
            wait_s = 5 * (3 ** (attempt - 1))
            print(f"  [!] Transient error during {label} (attempt {attempt}/{max_attempts}): {exc}")
            print(f"      Retrying in {wait_s}s...")
            time.sleep(wait_s)
    raise last_exc


def verify_instagram_connection() -> dict:
    """Confirm Composio Instagram OAuth token for target account is still authorized."""
    info = execute_composio_tool("INSTAGRAM_GET_USER_INFO", {"ig_user_id": "me"})
    username = info.get("username") or COMPOSIO_ACCOUNT
    ig_id = info.get("id", "unknown")
    print(f"  [Pre-flight] Connected Instagram: @{username} (ID: {ig_id})")
    return info


def verify_remote_image(url: str, label: str):
    """Ensure the public GitHub raw image URL responds HTTP 200 before calling Meta Graph API."""
    def _check():
        headers = {"User-Agent": "BNS-AutoPoster/1.0"}
        for method in ("HEAD", "GET"):
            req_headers = dict(headers)
            if method == "GET":
                req_headers["Range"] = "bytes=0-1023"
            req = urllib.request.Request(url, headers=req_headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    if resp.status in (200, 206):
                        ctype = resp.headers.get("Content-Type", "")
                        print(f"  [Pre-flight] {label} OK (HTTP {resp.status}, {ctype})")
                        return
                    raise RuntimeError(f"{label} returned HTTP {resp.status} at {url}")
            except urllib.error.HTTPError as e:
                if method == "HEAD" and e.code == 405:
                    continue
                raise RuntimeError(f"{label} HTTP {e.code} at {url}")
    run_with_retry(f"verify {label}", _check, max_attempts=3)

def get_state():
    """Load or initialize posting state."""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            st = json.load(f)
            if "twitter_current_index" not in st:
                st["twitter_current_index"] = 0
            if "twitter_posted" not in st:
                st["twitter_posted"] = []
            return st
    return {
        "current_index": 0,
        "posted": [],
        "twitter_current_index": 0,
        "twitter_posted": []
    }

def save_state(state):
    """Save posting progress state."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def get_proper_hashtags(post_data: dict) -> list[str]:
    """Generate comprehensive, high-reach, topic-tailored legal hashtags for BNS posts."""
    tags = [
        "#BharatiyaNyayaSanhita",
        "#BNS2023",
        "#IndianLaw",
        "#LinpaneLegalServices",
        "#CriminalLaw",
        "#LegalAwareness",
        "#LawNotes",
        "#LawStudentsIndia",
        "#JudiciaryPrep",
        "#UPSC",
        "#KnowTheLaw",
        "#LegalEducation",
        "#LawyersOfInstagram",
        "#Advocate"
    ]
    
    # 1. Section-specific hashtags
    for card in post_data.get("cards", []):
        s = card.get("s", "").strip()
        if s:
            tags.append(f"#BNSSection{s}")
            
    # 2. Topic & Chapter-specific hashtags
    chapter = (post_data.get("chapter_name", "") + " " + post_data.get("chapter_num", "")).lower()
    all_text = (
        chapter + " " + " ".join(
            (c.get("title", "") + " " + c.get("easy", "") + " " + " ".join(c.get("subs", [])))
            for c in post_data.get("cards", [])
        )
    ).lower()
    
    if any(k in all_text for k in ["woman", "women", "child", "modesty", "sexual", "rape", "marriage", "dowry", "harassment", "voyeurism", "stalking"]):
        tags.extend([
            "#WomenSafety",
            "#WomenRights",
            "#ProtectionOfWomen",
            "#ChildProtection",
            "#StopCrimeAgainstWomen",
            "#LegalRightsOfWomen",
            "#IPCvsBNS"
        ])
    elif any(k in all_text for k in ["murder", "culpable homicide", "hurt", "assault", "kidnapping", "abduction", "body", "life"]):
        tags.extend([
            "#OffencesAgainstBody",
            "#CriminalJusticeSystem",
            "#RightToLife",
            "#IPCvsBNS",
            "#IndianJudiciary"
        ])
    elif any(k in all_text for k in ["theft", "extortion", "robbery", "dacoity", "cheating", "property", "mischief", "criminal breach of trust", "forgery"]):
        tags.extend([
            "#OffencesAgainstProperty",
            "#PropertyLaw",
            "#FinancialCrimes",
            "#CyberCrimeIndia",
            "#IPCvsBNS"
        ])
    elif any(k in all_text for k in ["state", "sedition", "treason", "sovereignty", "armed forces", "public servant", "contempt", "perjury", "election"]):
        tags.extend([
            "#ConstitutionalLaw",
            "#OffencesAgainstState",
            "#PublicTranquility",
            "#IndianConstitution",
            "#IPCvsBNS"
        ])
    else:
        tags.extend([
            "#CriminalJustice",
            "#LegalReform",
            "#NewCriminalLaws",
            "#IPCvsBNS"
        ])
        
    # 3. Regional / Practice authority tags
    tags.extend([
        "#NagpurLawyer",
        "#WardhaLawyer",
        "#MaharashtraLegal"
    ])
    
    # Clean and deduplicate while maintaining order (max 28 to be safe within Instagram's 30 limit)
    seen = set()
    unique_tags = []
    for t in tags:
        t_clean = t.replace(" ", "").replace("-", "")
        if t_clean.lower() not in seen:
            seen.add(t_clean.lower())
            unique_tags.append(t_clean)
            
    return unique_tags[:28]

def format_caption(post_data: dict) -> str:
    """Generate an engaging, legally accurate Instagram caption with proper hashtags."""
    series_mark = post_data.get("series_mark", "01")
    sections_range = post_data.get("sections_range", "")
    chapter_num = post_data.get("chapter_num", "")
    chapter_name = post_data.get("chapter_name", "")
    
    caption_lines = [
        f"⚖️ BNS Legal Series — Post #{series_mark}",
        f"📖 Sections {sections_range} | {chapter_num}: {chapter_name}",
        "",
        "Simplified breakdown of the Bharatiya Nyaya Sanhita (BNS), 2023 for law students, advocates, and citizens:",
        ""
    ]
    
    for card in post_data.get("cards", []):
        s_num = card.get("s", "")
        title = card.get("title", "")
        takeaway = card.get("takeaway", "")
        easy = card.get("easy", "")
        caption_lines.append(f"🔹 Section {s_num}: {title}")
        caption_lines.append(f"   Takeaway: {takeaway}")
        caption_lines.append(f"   Explanation: {easy}")
        caption_lines.append("")
        
    hashtags_str = " ".join(get_proper_hashtags(post_data))
    caption_lines.extend([
        "💡 Save this post for your legal reference!",
        "👥 Follow @linpane_legal_services for daily criminal law insights.",
        "",
        "---",
        hashtags_str
    ])
    
    return "\n".join(caption_lines)

def format_tweet_text(post_data: dict) -> str:
    """Generate concise, high-impact tweet strictly under Twitter's 280-char limit."""
    series_mark = post_data.get("series_mark", "01")
    sections_range = post_data.get("sections_range", "")
    chapter_name = post_data.get("chapter_name", "")
    if len(chapter_name) > 25:
        chapter_name = chapter_name[:22] + "..."
    
    header = f"⚖️ BNS Series — Post #{series_mark}\n📖 Sections {sections_range} | {chapter_name}\n\n"
    footer = "\n\n#BNS2023 #IndianLaw #LinpaneLegalServices"
    
    cards = post_data.get("cards", [])
    card_lines = []
    for card in cards:
        s = card.get("s", "")
        t = card.get("title", "")
        if len(t) > 28:
            t = t[:25] + "..."
        card_lines.append(f"🔹 Sec {s}: {t}")
        
    full = header + "\n".join(card_lines) + footer
    if len(full) > 270:
        card_lines = []
        for card in cards:
            s = card.get("s", "")
            t = card.get("title", "")
            if len(t) > 20:
                t = t[:18] + ".."
            card_lines.append(f"🔹 Sec {s}: {t}")
        full = header + "\n".join(card_lines) + footer
    return full

def publish_bns_post(image_url: str, caption: str) -> dict:
    """Publish Feed Post via Composio Instagram tools."""
    print(f"  [Feed 1/2] Creating Instagram Media Container via Composio...")
    print(f"             Image URL: {image_url}")
    container_res = run_with_retry(
        "Feed container creation",
        lambda: execute_composio_tool("INSTAGRAM_POST_IG_USER_MEDIA", {
            "ig_user_id": "me",
            "image_url": image_url,
            "caption": caption
        }),
    )
    creation_id = container_res.get("id")
    if not creation_id:
        raise ValueError(f"No creation_id returned: {container_res}")
    print(f"             Container created successfully (ID: {creation_id})")

    print("  [Feed 2/2] Publishing Feed Post to Instagram...")
    publish_res = run_with_retry(
        "Feed container publish",
        lambda: execute_composio_tool("INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH", {
            "ig_user_id": "me",
            "creation_id": str(creation_id),
            "max_wait_seconds": 60
        }),
    )
    published_id = publish_res.get("id")
    print(f"             SUCCESS! Published Feed Post ID: {published_id}")
    return publish_res

def publish_bns_story(image_url: str) -> dict:
    """Publish 9:16 vertical Story via Composio Instagram tools."""
    print(f"  [Story 1/2] Creating Instagram Story Container...")
    container_res = run_with_retry(
        "Story container creation",
        lambda: execute_composio_tool("INSTAGRAM_POST_IG_USER_MEDIA", {
            "ig_user_id": "me",
            "media_type": "STORIES",
            "image_url": image_url
        }),
    )
    creation_id = container_res.get("id")
    if not creation_id:
        raise ValueError(f"No creation_id returned for story: {container_res}")
    print(f"              Story container created (ID: {creation_id})")

    print("  [Story 2/2] Publishing Story to Instagram...")
    publish_res = run_with_retry(
        "Story container publish",
        lambda: execute_composio_tool("INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH", {
            "ig_user_id": "me",
            "creation_id": str(creation_id),
            "max_wait_seconds": 60
        }),
    )
    story_id = publish_res.get("id")
    print(f"              SUCCESS! Published Story ID: {story_id}")
    return publish_res

def publish_twitter_post(image_path: Path, text: str) -> dict:
    """Publish Tweet with Infographic Image to X (Twitter)."""
    if not (TWITTER_CONSUMER_KEY and TWITTER_CONSUMER_SECRET and TWITTER_ACCESS_TOKEN and TWITTER_ACCESS_TOKEN_SECRET):
        print("  [X] Twitter credentials not configured. Skipping X post.")
        return None

    try:
        import tweepy
    except ImportError:
        print("  [X] tweepy library not installed. Skipping X post.")
        return None

    print(f"  [X 1/2] Uploading image {image_path.name} to X (Twitter)...")
    try:
        auth = tweepy.OAuth1UserHandler(
            TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
            TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
        )
        api = tweepy.API(auth)
        media = api.media_upload(str(image_path))
        print(f"          Image uploaded successfully! Media ID: {media.media_id}")

        print("  [X 2/2] Publishing Tweet...")
        client = tweepy.Client(
            consumer_key=TWITTER_CONSUMER_KEY,
            consumer_secret=TWITTER_CONSUMER_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )
        res = client.create_tweet(text=text, media_ids=[media.media_id])
        tweet_id = res.data["id"]
        print(f"          SUCCESS! Published Tweet ID: {tweet_id}")
        print(f"          Live URL: https://x.com/linpanelegal/status/{tweet_id}")
        return {"id": str(tweet_id)}
    except Exception as e:
        err_str = str(e)
        if "402" in err_str or "credits" in err_str.lower() or "payment required" in err_str.lower():
            print("  [X] Skipping X (Twitter): X developer account returned 402 CreditsDepleted (free tier cannot post).")
            return None
        raise

def main(dry_run: bool = False):
    print("=" * 60)
    print("  BNS Automated Multi-Platform Publisher (Instagram & X)")
    print(f"  Instagram Target: @{COMPOSIO_ACCOUNT}")
    print(f"  Twitter / X Target: @linpanelegal")
    print(f"  Host Repository:  {GITHUB_REPO}")
    print("=" * 60)
    
    state = get_state()
    ig_idx = state["current_index"]
    tw_idx = state["twitter_current_index"]
    
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        all_posts = json.load(f)["posts"]
        
    # -------------------------------------------------------------
    # PART 1: Instagram Publication (Feed + Story)
    # -------------------------------------------------------------
    if ig_idx < len(all_posts):
        post = all_posts[ig_idx]
        post_file = f"BNS_{post['file']}.jpg"
        img_path = OUTPUT_DIR / post_file
        
        print(f"\n[+] Preparing Instagram Post #{post['series_mark']} (Sections {post['sections_range']})...")
        caption = format_caption(post)
        image_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/v2/output/{post_file}"
        story_file = f"BNS_story-{post['series_mark']}.jpg"
        story_path = OUTPUT_DIR / story_file
        story_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/v2/output/{story_file}"

        if not img_path.exists():
            raise FileNotFoundError(f"Missing local feed post image: {img_path}")

        if dry_run:
            print(f"[DRY RUN] Local Feed exists:  {img_path.name} ({img_path.stat().st_size // 1024} KB)")
            print(f"[DRY RUN] Local Story exists: {story_path.name} ({'OK' if story_path.exists() else 'MISSING'})")
            print(f"[DRY RUN] Caption length: {len(caption)} chars")
            try:
                verify_instagram_connection()
                verify_remote_image(image_url, "Feed Image")
            except Exception as e:
                print(f"[DRY RUN] Pre-flight check warning: {e}")

        if not dry_run:
            try:
                verify_instagram_connection()
                verify_remote_image(image_url, "Feed Image")

                print("\n[1/2] Publishing Feed Post to Instagram via Composio...")
                pub_res = publish_bns_post(image_url, caption)
                pub_id = pub_res.get("id", "unknown")

                print("\n[2/2] Publishing 9:16 Story to Instagram via Composio...")
                try:
                    if not story_path.exists():
                        raise FileNotFoundError(f"Missing local story image: {story_path}")
                    verify_remote_image(story_url, "Story Image")
                    story_res = publish_bns_story(story_url)
                    story_id = story_res.get("id", "unknown")
                except Exception as e:
                    print(f"Warning: Story publishing failed: {e}")
                    story_id = None
                    
                state["current_index"] = ig_idx + 1
                state["posted"].append({
                    "index": ig_idx,
                    "file": post_file,
                    "series_mark": post["series_mark"],
                    "sections": post["sections_range"],
                    "published_id": pub_id,
                    "story_id": story_id,
                    "time": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                save_state(state)
                print(f"[+] Instagram Progress Saved! Next IG post: Post #{ig_idx + 2}")
            except Exception as e:
                print(f"[-] Instagram publication failed: {e}")
                print("    Note: Please reconnect Instagram in Composio to resume Instagram publishing.")
    else:
        print("[!] All Instagram posts completed!")

    # -------------------------------------------------------------
    # PART 2: Twitter / X Publication (Catch-up Mode or Sync)
    # -------------------------------------------------------------
    # If X is behind Instagram (tw_idx < state["current_index"]),
    # post up to 2 posts per run so X catches up quickly!
    x_posts_to_publish = []
    if tw_idx < state["current_index"]:
        # Catch-up: post 2 per run
        x_posts_to_publish = [tw_idx]
        if tw_idx + 1 < state["current_index"] and tw_idx + 1 < len(all_posts):
            x_posts_to_publish.append(tw_idx + 1)
    elif tw_idx < len(all_posts):
        # Synchronized: post 1
        x_posts_to_publish = [tw_idx]

    for target_tw_idx in x_posts_to_publish:
        tw_post = all_posts[target_tw_idx]
        tw_img_file = f"BNS_{tw_post['file']}.jpg"
        tw_img_path = OUTPUT_DIR / tw_img_file
        tw_text = format_tweet_text(tw_post)
        
        print(f"\n[+] Preparing X (Twitter) Post #{tw_post['series_mark']} (Sections {tw_post['sections_range']})...")
        if dry_run:
            print("[DRY RUN] Tweet text preview:\n", tw_text)
            continue
            
        try:
            tw_result = publish_twitter_post(tw_img_path, tw_text)
            if tw_result and "id" in tw_result:
                state["twitter_current_index"] = target_tw_idx + 1
                state["twitter_posted"].append({
                    "index": target_tw_idx,
                    "file": tw_img_file,
                    "series_mark": tw_post["series_mark"],
                    "sections": tw_post["sections_range"],
                    "tweet_id": tw_result["id"],
                    "time": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                save_state(state)
                print(f"[+] X Progress Saved! Next X post: Post #{target_tw_idx + 2}")
            else:
                break
        except Exception as e:
            print(f"[-] X (Twitter) publication notice: {e}")
            break

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    main(dry_run=is_dry)
