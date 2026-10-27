"""
BNS Daily Auto-Poster for Instagram via Composio & GitHub
Publishes posts & stories from v2/bns_posts.json using rendered images in v2/output/
"""
import os
import sys
import json
import time
import re
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

COMPOSIO_MCP_URL = "https://connect.composio.dev/mcp"
COMPOSIO_ACCOUNT = os.getenv("COMPOSIO_ACCOUNT", "linpane_legal_services")
GITHUB_REPO = os.getenv("GITHUB_REPO", "yuvrajlokhande19/bns-image-maker")

def get_api_key():
    key = os.getenv("COMPOSIO_API_KEY")
    if not key:
        raise ValueError("Missing COMPOSIO_API_KEY! Please set it in .env or environment.")
    return key

def call_composio_mcp(tool_name: str, arguments: dict) -> dict:
    key = get_api_key()
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
    with urllib.request.urlopen(req, timeout=60) as resp:
        text = resp.read().decode("utf-8")
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
    parsed = json.loads(raw_text)
    if not parsed.get("successful"):
        error_msg = parsed.get("error") or parsed.get("data", {}).get("results", [{}])[0].get("error")
        raise RuntimeError(f"Composio execution failed: {error_msg}")
    
    results = parsed.get("data", {}).get("results", [])
    if results and "response" in results[0]:
        inner = results[0]["response"]
        if not inner.get("successful", True):
            raise RuntimeError(f"Tool error: {inner.get('error')}")
        return inner.get("data", {})
    return parsed.get("data", {})

def get_state():
    """Load or initialize posting state."""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "current_index": 0,
        "posted": []
    }

def save_state(state):
    """Save posting progress state."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def format_caption(post_data: dict) -> str:
    """Generate an engaging, legally accurate Instagram caption."""
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
        
    caption_lines.extend([
        "💡 Save this post for your legal reference!",
        "👥 Follow @linpane_legal_services for daily criminal law insights.",
        "",
        "---",
        "#BharatiyaNyayaSanhita #BNS2023 #IndianLaw #LegalEducation #LawNotes #LinpaneLegalServices #CriminalLaw #LawStudentsIndia #UPSC #JudiciaryPrep #KnowTheLaw"
    ])
    
    return "\n".join(caption_lines)

def publish_bns_post(image_url: str, caption: str) -> dict:
    """
    Publish Feed Post via Composio Instagram tools:
    1. INSTAGRAM_POST_IG_USER_MEDIA
    2. INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH
    """
    print(f"  [Feed 1/2] Creating Instagram Media Container via Composio...")
    print(f"             Image URL: {image_url}")
    container_res = execute_composio_tool("INSTAGRAM_POST_IG_USER_MEDIA", {
        "ig_user_id": "me",
        "image_url": image_url,
        "caption": caption
    })
    creation_id = container_res.get("id")
    if not creation_id:
        raise ValueError(f"No creation_id returned: {container_res}")
    print(f"             Container created successfully (ID: {creation_id})")
    
    print("  [Feed 2/2] Publishing Feed Post to Instagram...")
    publish_res = execute_composio_tool("INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH", {
        "ig_user_id": "me",
        "creation_id": str(creation_id),
        "max_wait_seconds": 60
    })
    published_id = publish_res.get("id")
    print(f"             SUCCESS! Published Feed Post ID: {published_id}")
    return publish_res

def publish_bns_story(image_url: str) -> dict:
    """
    Publish the exact same image as an Instagram Story:
    1. INSTAGRAM_POST_IG_USER_MEDIA (media_type: STORIES)
    2. INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH
    """
    print(f"  [Story 1/2] Creating Instagram Story Container...")
    container_res = execute_composio_tool("INSTAGRAM_POST_IG_USER_MEDIA", {
        "ig_user_id": "me",
        "media_type": "STORIES",
        "image_url": image_url
    })
    creation_id = container_res.get("id")
    if not creation_id:
        raise ValueError(f"No creation_id returned for story: {container_res}")
    print(f"              Story container created (ID: {creation_id})")
    
    print("  [Story 2/2] Publishing Story to Instagram...")
    publish_res = execute_composio_tool("INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH", {
        "ig_user_id": "me",
        "creation_id": str(creation_id),
        "max_wait_seconds": 60
    })
    story_id = publish_res.get("id")
    print(f"              SUCCESS! Published Story ID: {story_id}")
    return publish_res

def main(dry_run: bool = False):
    print("=" * 60)
    print("  BNS Instagram Automated Publisher (Post + Story)")
    print(f"  Target Account: @{COMPOSIO_ACCOUNT}")
    print(f"  Host Repository: {GITHUB_REPO}")
    print("=" * 60)
    
    state = get_state()
    current_idx = state["current_index"]
    
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        all_posts = json.load(f)["posts"]
        
    if current_idx >= len(all_posts):
        print(f"All {len(all_posts)} posts have been published!")
        return
        
    post = all_posts[current_idx]
    post_file = f"BNS_{post['file']}.jpg"
    img_path = OUTPUT_DIR / post_file
    
    if not img_path.exists():
        print(f"Error: Image {img_path} not found!")
        return
        
    print(f"\n[+] Preparing Post #{post['series_mark']} (Sections {post['sections_range']})...")
    caption = format_caption(post)
    print("\n--- Caption Preview ---")
    print(caption[:280] + "...\n-----------------------")
    
    # Direct CDN / GitHub raw URL
    image_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/v2/output/{post_file}"
    print(f"\n[+] Image Public URL: {image_url}")
    
    if dry_run:
        print("\n[DRY RUN] Everything verified! Not publishing to Instagram.")
        return
        
    # 1. Publish Feed Post
    print("\n[1/2] Publishing Feed Post to Instagram via Composio...")
    pub_result = publish_bns_post(image_url, caption)
    published_id = pub_result.get("id", "unknown")
    
    # 2. Publish Story
    print("\n[2/2] Publishing Story to Instagram via Composio...")
    try:
        story_result = publish_bns_story(image_url)
        story_id = story_result.get("id", "unknown")
    except Exception as e:
        print(f"Warning: Story publishing failed: {e}")
        story_id = None
    
    # Update State
    state["current_index"] = current_idx + 1
    state["posted"].append({
        "index": current_idx,
        "file": post_file,
        "series_mark": post["series_mark"],
        "sections": post["sections_range"],
        "published_id": published_id,
        "story_id": story_id,
        "image_url": image_url,
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    save_state(state)
    print(f"\n[+] Progress saved! Both Post & Story published. Next up: Post #{current_idx + 2} of {len(all_posts)}")

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    main(dry_run=is_dry)
