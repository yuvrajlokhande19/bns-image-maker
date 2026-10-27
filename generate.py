"""
BNS Image Maker - Free local generator (Pillow only, no API cost, no misspellings)
Replicates LINPANE Legal Services style: 3 sections per post.
Usage:
  python generate.py --start 4 --count 5
  python generate.py --resume
  python generate.py --all
State file quota_state.json enables stop-and-resume (quota refuel workflow).
"""
import json, argparse, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
DATA = BASE / "data" / "bns_sections.json"
OUT = BASE / "output"
STATE = BASE / "quota_state.json"

W, H = 1080, 1350
CREAM = (255, 249, 232)
NAVY = (11, 36, 71)
NAVY2 = (16, 52, 102)
YELLOW = (255, 203, 46)
YELLOW_D = (242, 181, 20)
INK = (30, 30, 30)
TEAL = (45, 140, 130)
PINK_BG = (255, 209, 220)
MINT_BG = (197, 240, 217)
LAV_BG = (232, 217, 255)
CARD_BG = (255, 253, 245)

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REG = r"C:\Windows\Fonts\arial.ttf"
FONT_ITALIC = r"C:\Windows\Fonts\ariali.ttf"

def font(size, bold=True):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    except:
        return ImageFont.load_default()

def font_reg(size):
    try:
        return ImageFont.truetype(FONT_REG, size)
    except:
        return ImageFont.load_default()

def wrap(draw, text, fnt, max_w):
    words=text.split()
    lines=[]
    cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t, font=fnt)<=max_w:
            cur=t
        else:
            if cur:
                lines.append(cur)
            cur=w
    if cur:
        lines.append(cur)
    return lines

def draw_brush(draw, xy, fill):
    # simple brush-like rectangle with jagged edges
    x0,y0,x1,y1=xy
    draw.rounded_rectangle(xy, radius=10, fill=fill)
    # small spikes to mimic brush
    for x in range(x0+10, x1-10, 26):
        draw.polygon([(x,y0),(x+10,y0-4),(x+20,y0)], fill=fill)
        draw.polygon([(x,y1),(x+10,y1+4),(x+20,y1)], fill=fill)

def draw_header(draw, sections):
    # Top bar
    # Logo circle left
    draw.ellipse([18,12,92,86], fill=NAVY, outline=YELLOW, width=3)
    d2=ImageDraw.Draw(draw._image) if hasattr(draw,'_image') else draw
    # scales symbol as text
    try:
        draw.text((55,48), "§", font=font(34), fill=YELLOW, anchor="mm")
    except:
        pass
    draw.text((108,18), "LINPANE", font=font(32), fill=NAVY)
    draw.text((108,50), "LEGAL SERVICES", font=font(16), fill=NAVY)
    draw.text((108,70), "YOUR RIGHTS  |  OUR PRIORITY", font=font_reg(11), fill=(80,80,80))
    # website pill
    draw.rounded_rectangle([660,14,1062,58], radius=22, fill=YELLOW)
    draw.text((861,36), "linpanelegalservices.in", font=font(19), fill=NAVY, anchor="mm")
    # Info Presents
    draw_brush(draw, [22,96,220,130], YELLOW)
    draw.text((121,113), "Info Presents", font=font(19), fill=NAVY, anchor="mm")
    # U badge + Basic of Law
    draw.ellipse([70,134,150,214], fill=YELLOW)
    draw.ellipse([70,134,150,214], outline=NAVY, width=2)
    draw.text((110,174), "U", font=font(52), fill=NAVY, anchor="mm")
    draw.text((168,152), "Basic of Law", font=font(26), fill=(20,20,20), anchor="lm")
    draw.text((168,182), "by Linpane Legal Services", font=font_reg(15), fill=(40,40,40), anchor="lm")
    draw.text((30,214), "Simple Laws  |  Better Awareness", font=font_reg(14), fill=NAVY)
    draw.text((30,234), "A Stronger You", font=font(15), fill=NAVY)
    # BNS huge
    # crown above BNS
    cx, cy = 540, 62
    draw.polygon([(cx-28,cy+18),(cx-28,cy),(cx-14,cy+10),(cx,cy-8),(cx+14,cy+10),(cx+28,cy),(cx+28,cy+18)], fill=None, outline=NAVY, width=3)
    draw.text((540,150), "BNS", font=font(130), fill=NAVY, anchor="mm", stroke_width=2, stroke_fill=YELLOW)
    draw.text((540,148), "BNS", font=font(130), fill=(14,60,110), anchor="mm")
    draw_brush(draw, [300,232,790,300], YELLOW)
    draw.text((545,254), "THE BHARATIYA NYAYA", font=font(26), fill=NAVY, anchor="mm")
    draw.text((545,280), "SANHITA, 2023", font=font(26), fill=NAVY, anchor="mm")
    # Start here pill
    s0,s1=sections[0]['n'], sections[2]['n']
    draw_brush(draw, [300,308,790,346], NAVY)
    draw.text((545,327), f"START HERE  •  SECTIONS {s0}-{s1}", font=font(20), fill="white", anchor="mm")
    # right tagline + book stack (no external images - free & copyright-safe)
    draw.text((880,96), "New Law.", font=font_reg(17), fill=(30,30,30))
    draw.text((880,118), "Stronger Justice.", font=font_reg(17), fill=(30,30,30))
    draw.text((880,140), "A Safer Tomorrow.", font=font_reg(17), fill=(30,30,30))
    # book stack (simple)
    draw.rounded_rectangle([830,190,1050,238], radius=8, fill=(16,52,80))
    draw.rounded_rectangle([822,238,1058,288], radius=8, fill=(22,66,100))
    draw.text((940,212), "JUSTICE", font=font(15), fill=YELLOW, anchor="mm")
    draw.text((940,230), "FAIRNESS", font=font(13), fill="white", anchor="mm")
    draw.text((940,263), "EQUALITY", font=font(13), fill="white", anchor="mm")
    # small gavel head sitting on books
    draw.rounded_rectangle([905,158,985,184], radius=6, fill=(133,77,35))
    draw.rectangle([940,184,952,192], fill=(90,50,20))

def draw_info_strip(draw):
    y0=360
    draw.rounded_rectangle([14,y0,1066,y0+62], radius=12, fill=(255,243,205), outline=(200,180,120))
    # 3 cols
    draw.text((70,y0+16), "BNS is Act No. 45 of 2023", font=font(15), fill=NAVY)
    draw.text((70,y0+36), "Enacted on 25 December 2023", font=font_reg(13), fill=(40,40,40))
    draw.line([360,y0+8,360,y0+54], fill=(180,160,120), width=2)
    draw.text((480,y0+16), "Comes into force from", font=font_reg(13), fill=(40,40,40))
    draw.text((480,y0+34), "1 July 2024", font=font(15), fill=NAVY)
    draw.line([700,y0+8,700,y0+54], fill=(180,160,120), width=2)
    # chapter dynamic passed via global? draw placeholder, overwritten later
    return y0+62

def draw_card(draw, x0, y0, w, h, sec, idx, accent):
    draw.rounded_rectangle([x0,y0,x0+w,y0+h], radius=18, fill=CARD_BG, outline=TEAL, width=2)
    # number badge
    draw.ellipse([x0+12,y0+8,x0+88,y0+84], fill=NAVY)
    draw.text((x0+50,y0+46), f"{sec['n']:02d}", font=font(32), fill="white", anchor="mm")
    # Section pill
    draw.rounded_rectangle([x0+100,y0+18,x0+w-12,y0+52], radius=12, fill=YELLOW)
    draw.text((x0+100+(w-112)//2,y0+35), f"Section {sec['n']}", font=font(17), fill=NAVY, anchor="mm")
    cy=y0+92
    # title
    title=sec['title']
    lines=wrap(draw, title, font(22), w-28)
    lines=lines[:3]
    for ln in lines:
        draw.text((x0+w//2,cy), ln, font=font(21), fill=NAVY, anchor="ma")
        cy+=26
    cy+=6
    # Easy Explanation pill
    pill_bg = PINK_BG if (accent%2==0) else MINT_BG
    draw.rounded_rectangle([x0+60,cy,x0+w-60,cy+26], radius=13, fill=pill_bg)
    draw.text((x0+w//2,cy+13), "Easy Explanation", font=font(14), fill=NAVY, anchor="mm")
    cy+=32
    # easy text
    elines=wrap(draw, sec['easy'], font_reg(14), w-30)
    elines=elines[:7]
    for ln in elines:
        draw.text((x0+15,cy), ln, font=font_reg(14), fill=(35,35,35))
        cy+=19
    cy+=8
    # icon area (simple vector per card position)
    iy=cy
    # draw book / magnifier / scale depending on card position
    cx=x0+w//2
    if accent%3==0:
        draw.rounded_rectangle([cx-70,iy,cx+70,iy+86], radius=8, fill=NAVY, outline=YELLOW, width=2)
        draw.text((cx,iy+28), "BNS", font=font(22), fill=YELLOW, anchor="mm")
        draw.text((cx,iy+52), "2023", font=font(18), fill="white", anchor="mm")
        draw.text((cx,iy+70), sec['chapter_short'], font=font_reg(11), fill="white", anchor="mm")
    elif accent%3==1:
        draw.rounded_rectangle([cx-70,iy,cx+20,iy+86], radius=4, fill="white", outline=NAVY, width=2)
        draw.text((cx-25,iy+14), "DEFINITIONS", font=font(10), fill=NAVY, anchor="mm")
        draw.ellipse([cx+5,iy+30,cx+65,iy+90], outline=NAVY, width=4, fill=(220,235,255))
        draw.line([cx+55,iy+80,cx+80,iy+105], fill=NAVY, width=6)
    else:
        # scales
        draw.line([cx-50,iy+10,cx+50,iy+10], fill=NAVY, width=4)
        draw.line([cx,iy+10,cx,iy+60], fill=NAVY, width=4)
        draw.polygon([(cx-50,iy+10),(cx-70,iy+50),(cx-30,iy+50)], outline=NAVY, width=3)
        draw.polygon([(cx+50,iy+10),(cx+30,iy+50),(cx+70,iy+50)], outline=NAVY, width=3)
        draw.rounded_rectangle([cx-60,iy+55,cx+60,iy+80], radius=6, fill=NAVY)
        draw.text((cx,iy+67), "LAW", font=font(12), fill=YELLOW, anchor="mm")
    cy=iy+112
    # Key Takeaway
    draw.rounded_rectangle([x0+40,cy,x0+w-40,cy+26], radius=13, fill=LAV_BG)
    draw.text((x0+w//2,cy+13), "Key Takeaway", font=font(13), fill=NAVY, anchor="mm")
    cy+=30
    tlines=wrap(draw, sec['takeaway'], font_reg(13), w-30)
    tlines=tlines[:3]
    for ln in tlines:
        # center
        ww=draw.textlength(ln, font=font_reg(13))
        draw.text((x0+(w-ww)/2,cy), ln, font=font_reg(13), fill=(40,40,40))
        cy+=18
    return cy

def draw_footer(draw):
    y0=H-210
    draw_brush(draw, [240,y0,840,y0+44], NAVY)
    draw.text((540,y0+22), "Like  •  Comment  •  Follow", font=font(26), fill="white", anchor="mm")
    draw.text((540,y0+58), "to stay updated with more such legal insights!", font=font_reg(15), fill=(40,40,40), anchor="ma")
    draw.rounded_rectangle([840,y0+70,1050,y0+180], radius=8, fill=(255,220,120), outline=(200,150,30))
    draw.text((945,y0+110), "Better\nKnowledge\nBetter\nDecisions", font=font(16), fill=NAVY, anchor="mm")
    # bottom navy bar
    draw.rectangle([0,H-110,W,H], fill=NAVY)
    draw.text((540,H-88), "LINPANE LEGAL SERVICES", font=font(22), fill="white", anchor="mm")
    draw.rounded_rectangle([390,H-64,690,H-34], radius=15, fill=YELLOW)
    draw.text((540,H-49), "linpanelegalservices.in", font=font(14), fill=NAVY, anchor="mm")
    draw.text((540,H-22), "Law Made Simple  |  Knowledge Builds Confidence  |  Together for a Safer Tomorrow", font=font_reg(11), fill=(220,220,220), anchor="mm")
    draw.text((120,H-70), "Like\nif you found this helpful!", font=font_reg(13), fill="white")
    draw.text((380,H-80), "Comment: Your thoughts matter!", font=font_reg(12), fill="white")
    draw.text((650,H-80), "Follow for more legal updates!", font=font_reg(12), fill="white")

def render_post(sections):
    img=Image.new("RGB",(W,H),CREAM)
    draw=ImageDraw.Draw(img)
    draw_header(draw, sections)
    y_after=draw_info_strip(draw)
    # chapter line under strip: show chapters covered
    chaps=sorted(set([s['chapter_short']+": "+s['chapter_topic'] for s in sections]))
    chap_txt="  |  ".join(chaps)
    if len(chap_txt)>110:
        chap_txt=sections[0]['chapter_short']+f" onwards (Secs {sections[0]['n']}-{sections[2]['n']})"
    draw.text((540,y_after+16), chap_txt, font=font_reg(13), fill=NAVY, anchor="ma")
    y0=y_after+36
    card_w=(W-48)//3
    card_h=H-y0-230
    for i,sec in enumerate(sections):
        x0=16+i*(card_w+8)
        draw_card(draw, x0, y0, card_w, card_h, sec, sec['n'], i)
    draw_footer(draw)
    # disclaimer tiny
    draw.text((540,H-8), "For awareness only. Refer to India Code bare act. Not legal advice.", font=font_reg(9), fill=(180,180,180), anchor="mm")
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

def generate_batch(start, count):
    data=load_data()
    by_n={d['n']:d for d in data}
    made=[]
    for k in range(count):
        s=start+k*3
        if s+2>358:
            break
        secs=[by_n[s],by_n[s+1],by_n[s+2]]
        img=render_post(secs)
        OUT.mkdir(parents=True, exist_ok=True)
        fname=OUT/f"BNS_Sections_{s:03d}-{s+2:03d}.png"
        img.save(fname)
        print(f"Saved {fname}")
        made.append(str(fname))
    return made

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=None)
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--all", action="store_true")
    args=ap.parse_args()
    st=get_state()
    if args.all:
        start=4
        # 4..358 in steps of 3 => (358-3)//3 = 118 posts (last 358-360 capped). Actually 4-6 ... 358 needs handling remainder.
        # We'll do 4-6 up to 355-357, plus final 356-358 overlapping? Better: sequential non-overlapping from 4, last batch may be 1-2 sections padded.
        # Simpler: generate 4-6 ... 358 inclusive with step 3, last batch if <3 pad with note.
        count=(358-4)//3+1
        made=generate_batch(start, count)
        st["next_start"]=359
        st["done"].extend(made)
        save_state(st)
        return
    if args.resume or args.start is None:
        start=st.get("next_start",4)
    else:
        start=args.start
    made=generate_batch(start, args.count)
    if made:
        # update next_start to after last batch
        last_batch_start=start+(len(made)-1)*3
        st["next_start"]=last_batch_start+3
        st["done"].extend(made)
        save_state(st)
        print(f"Next start: {st['next_start']}. State saved. Re-run with --resume to continue after quota refuel.")
    else:
        print("Nothing to generate (end reached).")

if __name__=="__main__":
    main()
