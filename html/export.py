"""Render posts.json through template.html and screenshot to exact 1080x1350 PNG via headless Chrome.
Usage: python export.py [post-file ...]  (default: all posts in posts.json)
State: writes quota_state_html.json with last exported post for stop/resume.
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent
TPL = BASE / "template.html"
POSTS = BASE / "posts.json"
OUT = BASE.parent / "output_html"
STATE = BASE / "quota_state_html.json"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"done": []}

def render_post(post):
    html = TPL.read_text(encoding="utf-8")
    rep = {
        "SERIES_MARK": post["series_mark"],
        "SECTIONS_RANGE": post["sections_range"],
        "CHAPTER_NUM": post["chapter_num"],
        "CHAPTER_NAME": post["chapter_name"],
    }
    for i, c in enumerate(post["cards"], 1):
        rep[f"N{i}"] = c["n"]
        rep[f"S{i}"] = c["s"]
        rep[f"TITLE{i}"] = c["title"]
        rep[f"EASY{i}"] = c["easy"]
        rep[f"TAKE{i}"] = c["takeaway"]
        subs = "".join(f'<span class="subchip">{s}</span>' for s in c.get("subs", []))
        rep[f"SUBS{i}"] = subs
    for k, v in rep.items():
        html = html.replace("{{" + k + "}}", v)
    assert "{{" not in html, "unfilled token remains"
    page = BASE / (post["file"] + ".html")
    page.write_text(html, encoding="utf-8")
    return page

def shoot(page, dest, scale=2):
    import os, time
    big = dest.with_suffix(".big.png")
    tmp = dest.with_suffix(".tmp.png")
    url = page.resolve().as_uri()
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           "--window-size=1080,1350", f"--force-device-scale-factor={scale}",
           "--virtual-time-budget=5000", f"--screenshot={big}", url]
    subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    with Image.open(big) as im:
        im = im.convert("RGB")
        if im.size != (1080, 1350):
            im = im.resize((1080, 1350), Image.LANCZOS)
        im.save(tmp)
    big.unlink(missing_ok=True)
    for _ in range(5):
        try:
            os.replace(tmp, dest)
            break
        except OSError:
            time.sleep(1)
    else:
        raise OSError(f"cannot write {dest} after retries")
    return dest

def main():
    posts = json.loads(POSTS.read_text(encoding="utf-8"))["posts"]
    want = sys.argv[1:]
    st = load_state()
    OUT.mkdir(parents=True, exist_ok=True)
    for p in posts:
        if want and p["file"] not in want:
            continue
        page = render_post(p)
        dest = OUT / (p["file"] + "-1080x1350.png")
        shoot(page, dest)
        print("saved", dest, dest.stat().st_size)
        if p["file"] not in st["done"]:
            st["done"].append(p["file"])
    STATE.write_text(json.dumps(st, indent=2), encoding="utf-8")
    print("state:", st)

if __name__ == "__main__":
    main()
