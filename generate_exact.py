"""
EXACT template-reuse generator.
Keeps reference image pixels 100% intact except text boxes.
- Header, footer, illustrations, pills backgrounds, brushes: untouched (exact theme/design).
- Only swaps: SECTIONS x-y, badge numbers, Section N labels, titles, easy paragraphs, takeaway paragraphs, chapter box.
Free, offline (Pillow only), no misspellings, quota resume via quota_state.json.
"""
import json, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
DATA = BASE / "data" / "bns_sections.json"
OUT = BASE / "output_exact"
STATE = BASE / "quota_state.json"

def find_ref():
    cands = list(BASE.glob("BNS Sections*.png"))
    # prefer reference image (largest, contains 'reference')
    for c in cands:
        if "reference" in c.name.lower():
            return c
    # fallback: largest png not in output
    cands = [c for c in cands if "output" not in str(c)]
    return max(cands, key=lambda p: p.stat().st_size)

REF = find_ref()

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REG = r"C:\Windows\Fonts\arial.ttf"

def F(size, bold=True):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    except:
        return ImageFont.load_default()

NAVY = (11, 36, 71)
BODY = (35, 35, 35)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# Coordinates measured from 992x1586 grid (exact). Scaled dynamically.
# Format: (x0,y0,x1,y1) in reference pixels.
BOXES_992 = {
    "sections_numbers": (492, 395, 715, 432),   # wider to fully cover old SECTIONS 1-3
    "chapter": (795, 480, 955, 542),            # "Chapter I / Preliminary"
    "cards_x": [(14, 326), (338, 650), (664, 978)],
    "badge": (10, 565, 112, 660),               # relative to card x0 (dx)
    "section_pill": (118, 574, 296, 620),       # taller to cover brush bleed
    "top_block": (12, 632, 300, 925),           # title + easy pill + easy para (redrawn together)
    "takeaway_block": (12, 1115, 300, 1224),    # takeaway pill + para (redrawn together)
}

def scale_box(box, W, H):
    x0,y0,x1,y1 = box
    sx, sy = W/992.0, H/1586.0
    return (int(x0*sx), int(y0*sy), int(x1*sx), int(y1*sy))

def sample_bg(img, box):
    x0,y0,x1,y1 = box
    # sample border pixels average
    pixels = []
    for x in [x0+2, (x0+x1)//2, x1-2]:
        for y in [y0+2, y1-2]:
            pixels.append(img.getpixel((max(0,min(img.width-1,x)), max(0,min(img.height-1,y)))))
    r = sum(p[0] for p in pixels)//len(pixels)
    g = sum(p[1] for p in pixels)//len(pixels)
    b = sum(p[2] for p in pixels)//len(pixels)
    return (r,g,b)

def render_post(sections):
    img = Image.open(REF).convert("RGB")
    W,H = img.size
    draw = ImageDraw.Draw(img)
    sx, sy = W/992.0, H/1586.0

    def S(v):
        return int(v*sx) if isinstance(v,(int,float)) else v

    # 1) SECTIONS numbers
    bx = scale_box(BOXES_992["sections_numbers"], W, H)
    bg_navy = img.getpixel(((bx[0]+bx[2])//2, bx[1]-8)) if bx[1]-8>0 else NAVY
    # cover only numbers area with navy sampled
    draw.rectangle(bx, fill=(12, 38, 74))
    s0, s1 = sections[0]['n'], sections[2]['n']
    txt = f"SECTIONS {s0}-{s1}"
    f_sec = F(int(26*sx), True)
    # center in box
    draw.text(((bx[0]+bx[2])//2, (bx[1]+bx[3])//2), txt, font=f_sec, fill="white", anchor="mm")

    # 2) Chapter box (right of info strip)
    cb = scale_box(BOXES_992["chapter"], W, H)
    card_bg_sample = (253, 247, 228)
    draw.rectangle(cb, fill=card_bg_sample)
    # chapter: use first section's chapter, or combined if span
    chaps = [s['chapter_short'] for s in sections]
    topics = [s['chapter_topic'] for s in sections]
    if len(set(chaps)) == 1:
        ch1 = chaps[0].replace("Chapter ", "Chapter ")
        tp1 = topics[0]
    else:
        ch1 = f"{chaps[0]}-{chaps[-1]}"
        tp1 = topics[0]
    f_ch_b = F(int(20*sx), True)
    f_ch_r = F(int(16*sx), False)
    draw.text(((cb[0]+cb[2])//2, cb[1]+int(16*sy)), ch1, font=f_ch_b, fill=NAVY, anchor="ma")
    # topic may be long, wrap to 2 lines
    tl = wrap(draw, tp1, f_ch_r, (cb[2]-cb[0])-10)
    yy = cb[1]+int(38*sy)
    for ln in tl[:2]:
        draw.text(((cb[0]+cb[2])//2, yy), ln, font=f_ch_r, fill=(40,40,40), anchor="ma")
        yy += int(20*sy)

    # 3) Cards - exact pixels kept except text blocks
    cards_x = BOXES_992["cards_x"]
    # pill colors matching reference pattern: card0 pink, card1 mint, card2 pink
    EASY_PILL = [(255, 190, 205), (190, 235, 220), (255, 190, 205)]
    TAKE_PILL = [(235, 210, 250), (190, 235, 220), (235, 210, 250)]
    for i, sec in enumerate(sections):
        cx0, cx1 = cards_x[i]
        cx0, cx1 = int(cx0*sx), int(cx1*sx)
        card_w = cx1 - cx0
        # badge - fully redraw navy circle
        b = BOXES_992["badge"]
        bb = (cx0+int(b[0]*sx), int(b[1]*sy), cx0+int(b[2]*sx), int(b[3]*sy))
        draw.ellipse(bb, fill=(12,38,74))
        f_badge = F(int(38*sx), True)
        draw.text(((bb[0]+bb[2])//2, (bb[1]+bb[3])//2), f"{sec['n']:02d}", font=f_badge, fill="white", anchor="mm")
        # section pill - cover wider/taller, redraw yellow
        sp = BOXES_992["section_pill"]
        spb = (cx0+int(sp[0]*sx), int(sp[1]*sy), cx0+int(sp[2]*sx), int(sp[3]*sy))
        draw.rectangle(spb, fill=(255, 205, 55))
        f_sp = F(int(19*sx), True)
        draw.text(((spb[0]+spb[2])//2, (spb[1]+spb[3])//2), f"Section {sec['n']}", font=f_sp, fill=NAVY, anchor="mm")
        # top block: title + easy pill + easy para redrawn together (no ghosts)
        tb = BOXES_992["top_block"]
        tbox = (cx0+int(tb[0]*sx), int(tb[1]*sy), cx0+int(tb[2]*sx), int(tb[3]*sy))
        bg = (252, 250, 238)
        draw.rectangle(tbox, fill=bg)
        # title
        f_title = F(int(25*sx), True)
        lines = wrap(draw, sec['title'], f_title, (tbox[2]-tbox[0])-10)
        while len(lines)>3 and f_title.size>17:
            f_title = F(f_title.size-1, True)
            lines = wrap(draw, sec['title'], f_title, (tbox[2]-tbox[0])-10)
        lines = lines[:3]
        ty = tbox[1]+4
        for ln in lines:
            draw.text(((tbox[0]+tbox[2])//2, ty), ln, font=f_title, fill=NAVY, anchor="ma")
            ty += int(f_title.size*1.18)
        ty += int(6*sy)
        # easy pill (redrawn to match reference colors)
        pill_w = int(190*sx)
        pill_h = int(28*sy)
        pill_x0 = (tbox[0]+tbox[2]-pill_w)//2
        # round pill via rectangle (simple)
        draw.rounded_rectangle([pill_x0, ty, pill_x0+pill_w, ty+pill_h], radius=pill_h//2, fill=EASY_PILL[i])
        f_ep = F(int(14*sx), True)
        draw.text((pill_x0+pill_w//2, ty+pill_h//2), "Easy Explanation", font=f_ep, fill=NAVY, anchor="mm")
        ty += pill_h + int(8*sy)
        # easy para
        f_easy = F(int(14*sx), False)
        elines = wrap(draw, sec['easy'], f_easy, (tbox[2]-tbox[0])-8)
        # fit into remaining space
        max_lines = max(1, (tbox[3]-ty)//int(f_easy.size*1.35))
        elines = elines[:max_lines]
        while len(elines)>max_lines and f_easy.size>11:
            f_easy = F(f_easy.size-1, False)
            elines = wrap(draw, sec['easy'], f_easy, (tbox[2]-tbox[0])-8)
            max_lines = max(1, (tbox[3]-ty)//int(f_easy.size*1.35))
            elines = elines[:max_lines]
        ey = ty
        for ln in elines:
            if ey + f_easy.size > tbox[3]:
                break
            draw.text((tbox[0]+4, ey), ln, font=f_easy, fill=BODY)
            ey += int(f_easy.size*1.38)
        # takeaway block: pill + para redrawn
        kb = BOXES_992["takeaway_block"]
        kbox = (cx0+int(kb[0]*sx), int(kb[1]*sy), cx0+int(kb[2]*sx), int(kb[3]*sy))
        draw.rectangle(kbox, fill=bg)
        kpill_w = int(170*sx)
        kpill_h = int(26*sy)
        kpill_x0 = (kbox[0]+kbox[2]-kpill_w)//2
        ky = kbox[1]+2
        draw.rounded_rectangle([kpill_x0, ky, kpill_x0+kpill_w, ky+kpill_h], radius=kpill_h//2, fill=TAKE_PILL[i])
        f_kp = F(int(13*sx), True)
        draw.text((kpill_x0+kpill_w//2, ky+kpill_h//2), "Key Takeaway", font=f_kp, fill=NAVY, anchor="mm")
        ky += kpill_h + int(6*sy)
        f_k = F(int(13*sx), False)
        klines = wrap(draw, sec['takeaway'], f_k, (kbox[2]-kbox[0])-8)
        for ln in klines[:4]:
            if ky + f_k.size > kbox[3]:
                break
            wln = draw.textlength(ln, font=f_k)
            draw.text(((kbox[0]+kbox[2]-wln)//2, ky), ln, font=f_k, fill=BODY)
            ky += int(f_k.size*1.38)
    return img

def load_data():
    return json.loads(DATA.read_text(encoding="utf-8"))

def get_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except:
            pass
    return {"next_start":4, "done":[]}

def save_state(s):
    STATE.write_text(json.dumps(s, indent=2), encoding="utf-8")

def gen_batch(start, count):
    data = load_data()
    by_n = {d['n']: d for d in data}
    OUT.mkdir(parents=True, exist_ok=True)
    made = []
    for k in range(count):
        s = start + k*3
        if s+2 > 358:
            break
        secs = [by_n[s], by_n[s+1], by_n[s+2]]
        img = render_post(secs)
        fname = OUT / f"BNS_Sections_{s:03d}-{s+2:03d}_exact.png"
        img.save(fname)
        print(f"Saved {fname}")
        made.append(str(fname))
    return made

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=None)
    ap.add_argument("--count", type=int, default=3)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    st = get_state()
    if a.all:
        made = gen_batch(4, (358-4)//3+1)
        st["next_start"] = 359
        st["done"].extend(made)
        save_state(st)
        return
    start = st.get("next_start",4) if (a.resume or a.start is None) else a.start
    made = gen_batch(start, a.count)
    if made:
        st["next_start"] = start + len(made)*3
        st["done"].extend(made)
        save_state(st)
        print(f"Next start: {st['next_start']}. Re-run with --resume to continue.")
    else:
        print("Nothing to generate.")

if __name__ == "__main__":
    main()
