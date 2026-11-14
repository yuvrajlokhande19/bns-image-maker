"""
Build the upgraded editorial sketchbook v3 HTML template (v2/locked_template_v3.html)
preserving Linpane Legal Services brand identity (seal, Lady Justice on BNS,
Law Notes badge, Gavel & Books stack) while upgrading layout craft and inserting
dynamic {{ILLUS1}}..{{ILLUS3}} slots for section-specific BNS illustrations.
"""
import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
HTML = ROOT / "html"


def b64(path: Path) -> str:
    data = path.read_bytes()
    ext = path.suffix.lower().lstrip(".")
    mime = "image/png" if ext == "png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def main():
    logo_b64 = b64(HTML / "logo.png")
    lawnotes_b64 = b64(HTML / "lawnotes.png")
    justice_b64 = b64(HERE / "lady_justice_trimmed.png")
    gavel_b64 = b64(HERE / "gavel_books_final.png")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Linpane Legal Services — BNS Series v3</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Caveat+Brush&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Mukta:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --paper:  #FBF7EC;
  --paper2: #F2EBD7;
  --navy:   #0C2540;
  --navy2:  #143A61;
  --gold:   #F2C13A;
  --gold2:  #DDA114;
  --ink:    #1B2A3C;
  --muted:  #4A5B70;
}}

*, *::before, *::after {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  background: #8f887b;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}}

.page {{
  width: 1080px;
  height: 1350px;
  background: radial-gradient(ellipse at 50% 44%, #FCF9F0 45%, #F4EDDC 100%);
  overflow: hidden;
  position: relative;
  font-family: 'Poppins', Arial, sans-serif;
  color: var(--ink);
  display: flex;
  flex-direction: column;
}}

/* Subtle sketchbook parchment stipple grain */
.grain {{
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 50;
  opacity: 0.22;
  background-image: radial-gradient(rgba(12, 37, 64, 0.08) 0.75px, transparent 0.75px);
  background-size: 14px 14px;
}}

/* ── TOP HEADER BAR ── */
.top-header {{
  height: 92px;
  padding: 0 28px;
  background: linear-gradient(180deg, #FFFFFF 0%, #FDFBF5 100%);
  border-bottom: 3px solid var(--gold2);
  box-shadow: 0 2px 0 rgba(12, 37, 64, 0.14);
  display: flex;
  align-items: center;
  gap: 18px;
  position: relative;
  z-index: 10;
}}

.brand-seal {{
  width: 68px;
  height: 68px;
  object-fit: contain;
  flex-shrink: 0;
  filter: drop-shadow(0 2px 3px rgba(12, 37, 64, 0.18));
}}

.brand-text-wrap {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}}

.brand-title {{
  font-family: 'Anton', Impact, sans-serif;
  font-size: 72px;
  line-height: 0.94;
  letter-spacing: 7.4px;
  color: var(--navy);
  text-transform: uppercase;
  white-space: nowrap;
  width: 100%;
}}

.brand-sub-row {{
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 3px;
}}

.brand-sub {{
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 3.5px;
  color: #5D6C7D;
  text-transform: uppercase;
}}

.brand-rule {{
  flex: 1;
  height: 1.5px;
  background: linear-gradient(90deg, var(--gold2) 0%, rgba(221, 161, 20, 0.1) 100%);
}}

/* ── HERO SECTION ── */
.hero {{
  padding: 6px 26px 6px;
  display: grid;
  grid-template-columns: 238px 1fr 238px;
  align-items: center;
  position: relative;
  z-index: 8;
}}

/* Left Hero Column */
.hero-left {{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-top: 2px;
  position: relative;
}}

.info-presents-wrap {{
  position: relative;
  display: inline-block;
  padding: 2px 14px 2px 8px;
  margin-bottom: 2px;
}}

.brush-svg-bg {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}}

.info-presents {{
  position: relative;
  z-index: 1;
  font-family: 'Caveat Brush', cursive;
  font-size: 22px;
  color: var(--navy);
  transform: rotate(-2deg);
  display: block;
}}

.basic-law {{
  font-family: 'Caveat Brush', cursive;
  font-size: 35px;
  line-height: 1.02;
  color: var(--navy);
  margin-top: 2px;
}}

.by-linpane {{
  font-size: 11.2px;
  font-weight: 600;
  color: #425368;
  margin-top: 1px;
}}

.left-motto {{
  font-size: 11px;
  font-weight: 500;
  color: #2A3B4F;
  margin-top: 4px;
  line-height: 1.35;
}}

.stronger-you {{
  font-family: 'Caveat Brush', cursive;
  font-size: 18px;
  color: var(--navy);
  display: inline-flex;
  align-items: center;
  gap: 5px;
}}

.lawnotes-badge {{
  height: 112px;
  width: auto;
  object-fit: contain;
  margin-top: 4px;
  margin-left: 14px;
  filter: drop-shadow(0 3px 5px rgba(12, 37, 64, 0.14));
}}

/* Center Hero Column */
.hero-center {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  position: relative;
}}

.sunburst-bg {{
  position: absolute;
  top: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 380px;
  height: 190px;
  pointer-events: none;
  z-index: 0;
}}

.lady-justice {{
  height: 82px;
  width: auto;
  object-fit: contain;
  position: relative;
  z-index: 5;
  margin-top: 2px;
  margin-bottom: -22px;
  filter: drop-shadow(0 2px 4px rgba(12, 37, 64, 0.22));
}}

.bns-word-wrap {{
  position: relative;
  z-index: 3;
  height: 86px;
  display: flex;
  align-items: center;
  justify-content: center;
}}

.bns-svg-title {{
  width: 300px;
  height: 86px;
  overflow: visible;
}}

.act-title-wrap {{
  position: relative;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  margin-top: 0px;
  z-index: 4;
}}

.act-line-wrap {{
  position: relative;
  padding: 1px 16px;
  margin-bottom: 2px;
}}

.act-line-text {{
  position: relative;
  z-index: 1;
  font-family: 'Poppins', Arial, sans-serif;
  font-size: 15.5px;
  font-weight: 800;
  letter-spacing: 0.9px;
  color: var(--navy);
  line-height: 1.15;
}}

.series-pill {{
  margin-top: 3px;
  background: var(--navy);
  color: #F9D45C;
  font-size: 11.2px;
  font-weight: 700;
  letter-spacing: 1.3px;
  padding: 4px 20px;
  border-radius: 999px;
  border: 1.5px solid var(--navy);
  box-shadow: inset 0 0 0 2px var(--navy), inset 0 0 0 3px rgba(242, 193, 58, 0.65);
  text-transform: uppercase;
  z-index: 4;
}}

.trilingual-motto {{
  margin-top: 4px;
  font-family: 'Mukta', 'Poppins', sans-serif;
  font-size: 12px;
  font-weight: 700;
  color: #2A3B4F;
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 4;
}}

.motto-dot {{
  width: 5px;
  height: 5px;
  background: var(--gold2);
  transform: rotate(45deg);
  display: inline-block;
}}

/* Right Hero Column */
.hero-right {{
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-start;
  position: relative;
}}

.know-right-box {{
  text-align: right;
  margin-bottom: 2px;
}}

.know-top {{
  font-family: 'Caveat Brush', cursive;
  font-size: 19px;
  color: var(--navy);
  line-height: 1.05;
}}

.safer-wrap {{
  position: relative;
  display: inline-block;
  padding: 1px 10px 2px 12px;
}}

.safer-text {{
  position: relative;
  z-index: 1;
  font-family: 'Caveat Brush', cursive;
  font-size: 20px;
  color: var(--navy);
}}

.gavel-books {{
  width: 192px;
  height: 180px;
  object-fit: contain;
  margin-right: 2px;
  filter: drop-shadow(0 4px 8px rgba(12, 37, 64, 0.16));
}}

/* ── METADATA LEDGER BAR ── */
.meta-bar {{
  margin: 4px 26px 9px;
  height: 52px;
  background: linear-gradient(180deg, #FFFDF6 0%, #FBF3DE 100%);
  border: 1.6px solid #C8A148;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(12, 37, 64, 0.06);
  display: grid;
  grid-template-columns: 1fr 0.9fr 1.25fr;
  align-items: center;
  position: relative;
  z-index: 8;
}}

.meta-cell {{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 0 12px;
  height: 36px;
}}

.meta-cell + .meta-cell {{
  border-left: 1.5px dashed rgba(12, 37, 64, 0.25);
}}

.meta-icon {{
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}}

.meta-text-bold {{
  font-size: 12px;
  font-weight: 700;
  color: var(--navy);
  line-height: 1.22;
}}

.meta-text-sub {{
  font-size: 11px;
  font-weight: 500;
  color: #46576B;
  line-height: 1.22;
}}

/* ── 3 SECTION CARDS TRIPTYCH ── */
.cards-grid {{
  flex: 1;
  min-height: 0;
  padding: 0 26px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  position: relative;
  z-index: 8;
}}

.card {{
  border-radius: 15px;
  background: #FFFFFF;
  border: 2px solid var(--c-frame);
  box-shadow: 0 5px 16px rgba(12, 37, 64, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}}

.card-1 {{
  --c-frame: #163B61;
  --c-top: #F2B924;
  --c-pill-bg: #FAD975;
  --c-pill-fg: #0D2944;
  --c-sub-bg: #EFF5FC;
  --c-sub-bdr: #8FB0D4;
  --c-panel: #F6F9FD;
  --c-take-bg: #FFF7E0;
}}

.card-2 {{
  --c-frame: #186258;
  --c-top: #2B8E82;
  --c-pill-bg: #CBECE4;
  --c-pill-fg: #0E3B35;
  --c-sub-bg: #EDF8F5;
  --c-sub-bdr: #7AC4B6;
  --c-panel: #F3FBF8;
  --c-take-bg: #E6F6F1;
}}

.card-3 {{
  --c-frame: #4B3573;
  --c-top: #8B60BE;
  --c-pill-bg: #E9DCF9;
  --c-pill-fg: #2B1B4A;
  --c-sub-bg: #F5F0FC;
  --c-sub-bdr: #B295DA;
  --c-panel: #F8F5FD;
  --c-take-bg: #F0E8FA;
}}

.card-accent-strip {{
  height: 7px;
  width: 100%;
  background: var(--c-top);
  flex-shrink: 0;
}}

.card-inner {{
  flex: 1;
  padding: 11px 13px 12px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 10px;
}}

.card-head {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
}}

.card-badge-row {{
  width: 100%;
  display: flex;
  align-items: center;
  gap: 9px;
}}

.num-seal {{
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--c-frame);
  color: #FFFFFF;
  font-size: 18px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: inset 0 0 0 2.5px var(--c-frame), inset 0 0 0 4px rgba(255, 255, 255, 0.35);
}}

.sec-ribbon {{
  flex: 1;
  height: 32px;
  background: var(--c-pill-bg);
  color: var(--c-pill-fg);
  border-radius: 8px 18px 8px 8px;
  border: 1.4px solid rgba(12, 37, 64, 0.16);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.4px;
}}

.card-title {{
  font-size: 16px;
  font-weight: 800;
  line-height: 1.24;
  color: var(--navy);
  text-align: center;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2px 4px;
}}

.card-rule {{
  width: 90%;
  height: 1px;
  border-top: 1.5px dashed rgba(12, 37, 64, 0.2);
}}

.card-explain-block {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
  margin-top: 2px;
}}

.easy-pill {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: var(--c-sub-bg);
  border: 1px solid var(--c-sub-bdr);
  color: var(--c-frame);
  font-size: 10.6px;
  font-weight: 800;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  padding: 3px 12px;
  border-radius: 999px;
}}

.easy-dot {{
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--c-top);
}}

.card-body {{
  font-size: 13.8px;
  line-height: 1.48;
  font-weight: 500;
  color: #203044;
  text-align: center;
}}

.subs-row {{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 5px;
  margin-top: 4px;
}}

.subchip {{
  font-size: 10.8px;
  font-weight: 700;
  color: var(--c-frame);
  background: #FFFFFF;
  border: 1.2px dashed var(--c-sub-bdr);
  border-radius: 999px;
  padding: 3px 10px;
  line-height: 1.3;
}}

/* Sketchbook Contextual Illustration Frame */
.illus-panel {{
  margin: auto 0;
  flex: 0 0 auto;
  height: 152px;
  width: 100%;
  border-radius: 12px;
  background: var(--c-panel);
  border: 1.4px dashed rgba(12, 37, 64, 0.22);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 8px;
  position: relative;
}}

/* Key Takeaway Footer Box */
.takeaway-box {{
  background: var(--c-take-bg);
  border-left: 4px solid var(--c-frame);
  border-radius: 8px;
  padding: 7px 10px 8px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}}

.takeaway-tag {{
  font-size: 10.2px;
  font-weight: 800;
  letter-spacing: 0.7px;
  text-transform: uppercase;
  color: var(--c-frame);
  display: flex;
  align-items: center;
  gap: 4px;
}}

.takeaway-text {{
  font-size: 11.7px;
  font-weight: 600;
  line-height: 1.35;
  color: #132539;
}}

/* ── CTA + STICKY NOTE SECTION ── */
.cta-zone {{
  padding: 9px 26px 8px;
  height: 114px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 12;
}}

.cta-ribbon {{
  background: var(--navy);
  color: #FFFFFF;
  font-family: 'Caveat Brush', cursive;
  font-size: 25px;
  letter-spacing: 1px;
  padding: 2px 34px 3px;
  border-radius: 999px;
  box-shadow: 0 3px 0 var(--gold2);
  line-height: 1.15;
}}

.cta-ribbon span {{
  color: var(--gold);
  margin: 0 6px;
}}

.cta-sub {{
  font-size: 11.2px;
  font-weight: 600;
  color: #415165;
  margin-top: 4px;
}}

.cta-actions {{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 28px;
  margin-top: 4px;
}}

.cta-item {{
  display: flex;
  align-items: center;
  gap: 7px;
}}

.cta-icon-circle {{
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.4px solid var(--navy);
  flex-shrink: 0;
}}

.cta-item-title {{
  font-size: 11.5px;
  font-weight: 800;
  color: var(--navy);
  line-height: 1.1;
}}

.cta-item-desc {{
  font-size: 10px;
  font-weight: 500;
  color: #46576B;
  line-height: 1.15;
}}

/* Pinned Sticky Note */
.sticky-note {{
  position: absolute;
  right: 28px;
  top: 14px;
  width: 142px;
  padding: 12px 10px 9px;
  background: linear-gradient(170deg, #FBE274 0%, #F2C83B 100%);
  border: 1.3px solid #D3A21E;
  border-radius: 4px 4px 14px 4px;
  transform: rotate(-2.8deg);
  box-shadow: 3px 5px 10px rgba(12, 37, 64, 0.22);
  text-align: center;
  z-index: 20;
}}

.sticky-pin {{
  position: absolute;
  top: -7px;
  left: 50%;
  transform: translateX(-50%);
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #FF6B5B, #B42318);
  border: 1.5px solid #450A0A;
  box-shadow: 0 2px 3px rgba(0,0,0,0.28);
}}

.sticky-text {{
  font-family: 'Caveat Brush', cursive;
  font-size: 16.5px;
  line-height: 1.12;
  color: var(--navy);
}}

/* ── CLEAN NAVY FOOTER BAR (NO DUPLICATE CTA ROW!) ── */
.footer-bar {{
  height: 102px;
  background: linear-gradient(180deg, #0D2744 0%, #081A2E 100%);
  border-top: 3px solid var(--gold2);
  padding: 10px 30px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 10;
}}

.wheat-left, .wheat-right {{
  position: absolute;
  bottom: 10px;
  width: 34px;
  height: 70px;
  opacity: 0.78;
}}

.wheat-left {{ left: 20px; }}
.wheat-right {{ right: 20px; transform: scaleX(-1); }}

.footer-top-row {{
  width: 78%;
  display: flex;
  align-items: center;
  gap: 16px;
}}

.footer-hairline {{
  flex: 1;
  height: 1.5px;
  background: linear-gradient(90deg, transparent, rgba(242, 193, 58, 0.75), transparent);
}}

.site-pill {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(180deg, #F7CF58 0%, #E7AF20 100%);
  color: #091E36;
  font-size: 14.5px;
  font-weight: 800;
  letter-spacing: 0.5px;
  padding: 4px 22px;
  border-radius: 999px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
}}

.socials-row {{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
}}

.social-item {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #F8FAFC;
  font-size: 12.2px;
  font-weight: 600;
}}

.footer-tagline {{
  font-size: 10.8px;
  font-weight: 500;
  letter-spacing: 0.5px;
  color: #C7D4E3;
}}
</style>
</head>
<body>
<div class="page">
  <div class="grain"></div>

  <!-- TOP HEADER -->
  <header class="top-header">
    <img class="brand-seal" src="{logo_b64}" alt="Linpane Legal Services Seal">
    <div class="brand-text-wrap">
      <div class="brand-title">LINPANE LEGAL SERVICES</div>
      <div class="brand-sub-row">
        <span class="brand-sub">YOUR RIGHTS &nbsp;|&nbsp; OUR PRIORITY</span>
        <span class="brand-rule"></span>
      </div>
    </div>
  </header>

  <!-- HERO ZONE -->
  <section class="hero">
    <!-- Left Column -->
    <div class="hero-left">
      <div class="info-presents-wrap">
        <svg class="brush-svg-bg" viewBox="0 0 160 32" preserveAspectRatio="none">
          <path d="M4,18 Q40,6 92,8 T156,12 L152,26 Q98,29 44,27 T2,24 Z" fill="#F4C748" opacity="0.88"/>
        </svg>
        <span class="info-presents">Info Presents</span>
      </div>
      <div class="basic-law">Basic of Law</div>
      <div class="by-linpane">by Linpane Legal Services</div>
      <div class="left-motto">
        Simple Laws &nbsp;|&nbsp; Better Awareness<br>
        <span class="stronger-you">
          A Stronger You
          <svg width="16" height="15" viewBox="0 0 20 18"><path d="M10 16.5C10 16.5 1.8 11.4 1.8 5.8C1.8 3.1 3.9 1.3 6.3 1.3C7.9 1.3 9.2 2.1 10 3.4C10.8 2.1 12.1 1.3 13.7 1.3C16.1 1.3 18.2 3.1 18.2 5.8C18.2 11.4 10 16.5 10 16.5Z" fill="#DF4C4C" stroke="#0C2540" stroke-width="1.3"/></svg>
        </span>
      </div>
      <img class="lawnotes-badge" src="{lawnotes_b64}" alt="Law Notes Badge">
    </div>

    <!-- Center Focal Column -->
    <div class="hero-center">
      <!-- Sketchbook Sunburst Rays Behind Lady Justice & BNS -->
      <svg class="sunburst-bg" viewBox="0 0 390 210" fill="none">
        <line x1="195" y1="68" x2="112" y2="28" stroke="#DDA114" stroke-width="1.4" stroke-dasharray="5 5" opacity="0.55"/>
        <line x1="195" y1="68" x2="88" y2="62" stroke="#DDA114" stroke-width="1.4" stroke-dasharray="6 4" opacity="0.5"/>
        <line x1="195" y1="68" x2="104" y2="96" stroke="#0C2540" stroke-width="1.1" stroke-dasharray="4 6" opacity="0.22"/>
        <line x1="195" y1="68" x2="278" y2="28" stroke="#DDA114" stroke-width="1.4" stroke-dasharray="5 5" opacity="0.55"/>
        <line x1="195" y1="68" x2="302" y2="62" stroke="#DDA114" stroke-width="1.4" stroke-dasharray="6 4" opacity="0.5"/>
        <line x1="195" y1="68" x2="286" y2="96" stroke="#0C2540" stroke-width="1.1" stroke-dasharray="4 6" opacity="0.22"/>
      </svg>

      <img class="lady-justice" src="{justice_b64}" alt="Lady Justice">

      <div class="bns-word-wrap">
        <svg class="bns-svg-title" viewBox="0 0 300 86">
          <defs>
            <style>
              .bns-font {{
                font-family: 'Anton', Impact, sans-serif;
                font-size: 88px;
                letter-spacing: 5px;
              }}
            </style>
          </defs>
          <!-- Warm Gold Crisp Offset Emboss -->
          <text x="154" y="79" text-anchor="middle" class="bns-font" fill="#EBB220" stroke="#EBB220" stroke-width="8.5" stroke-linejoin="round">BNS</text>
          <!-- Cream Separation Halo -->
          <text x="150" y="75" text-anchor="middle" class="bns-font" fill="#FBF7EC" stroke="#FBF7EC" stroke-width="5" stroke-linejoin="round">BNS</text>
          <!-- Deep Navy Main Ink Fill -->
          <text x="150" y="75" text-anchor="middle" class="bns-font" fill="#0C2540">BNS</text>
        </svg>
      </div>

      <div class="act-title-wrap">
        <div class="act-line-wrap">
          <svg class="brush-svg-bg" viewBox="0 0 320 26" preserveAspectRatio="none">
            <path d="M5,8 Q90,3 175,6 T316,7 L312,22 Q200,25 110,23 T2,21 Z" fill="#F6C846" opacity="0.9"/>
          </svg>
          <span class="act-line-text">THE BHARATIYA NYAYA</span>
        </div>
        <div class="act-line-wrap">
          <svg class="brush-svg-bg" viewBox="0 0 210 26" preserveAspectRatio="none">
            <path d="M4,8 Q60,4 125,6 T207,8 L203,22 Q130,25 65,23 T2,20 Z" fill="#F6C846" opacity="0.9"/>
          </svg>
          <span class="act-line-text">SANHITA, 2023</span>
        </div>
      </div>

      <div class="series-pill">{{{{SERIES_MARK}}}} / BNS SERIES &nbsp;•&nbsp; SECTIONS {{{{SECTIONS_RANGE}}}}</div>

      <div class="trilingual-motto">
        <span>Know the Law</span>
        <i class="motto-dot"></i>
        <span>कानून जानें</span>
        <i class="motto-dot"></i>
        <span>कायदा जाणून घ्या</span>
      </div>
    </div>

    <!-- Right Column -->
    <div class="hero-right">
      <div class="know-right-box">
        <div class="know-top">Know the Law.</div>
        <div class="safer-wrap">
          <svg class="brush-svg-bg" viewBox="0 0 185 28" preserveAspectRatio="none">
            <path d="M4,15 Q55,5 120,8 T182,11 L179,24 Q115,27 50,25 T2,22 Z" fill="#F4C748" opacity="0.88"/>
          </svg>
          <span class="safer-text">For Safer Tomorrow.</span>
        </div>
      </div>
      <img class="gavel-books" src="{gavel_b64}" alt="Law Books and Gavel">
    </div>
  </section>

  <!-- METADATA LEDGER -->
  <section class="meta-bar">
    <div class="meta-cell">
      <svg class="meta-icon" viewBox="0 0 26 26" fill="none">
        <rect x="3" y="5" width="20" height="18" rx="3.5" fill="#FFFDF7" stroke="#0C2540" stroke-width="1.9"/>
        <path d="M3 10.5H23" stroke="#0C2540" stroke-width="1.8"/>
        <line x1="8.5" y1="3" x2="8.5" y2="7" stroke="#0C2540" stroke-width="2" stroke-linecap="round"/>
        <line x1="17.5" y1="3" x2="17.5" y2="7" stroke="#0C2540" stroke-width="2" stroke-linecap="round"/>
        <rect x="7" y="13.5" width="4" height="3" rx="0.8" fill="#E8A918"/>
        <rect x="14" y="13.5" width="5" height="3" rx="0.8" fill="#0C2540"/>
      </svg>
      <div>
        <div class="meta-text-bold">BNS is Act No. 45 of 2023</div>
        <div class="meta-text-sub">Enacted on 25 December 2023</div>
      </div>
    </div>

    <div class="meta-cell">
      <svg class="meta-icon" viewBox="0 0 26 26" fill="none">
        <path d="M13 3L21 6V12.5C21 17.5 17.4 21.5 13 23C8.6 21.5 5 17.5 5 12.5V6L13 3Z" fill="#E6F6F1" stroke="#0C2540" stroke-width="1.9" stroke-linejoin="round"/>
        <path d="M9.5 13L12 15.5L17 10.5" stroke="#186258" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <div>
        <div class="meta-text-sub">Comes into force from</div>
        <div class="meta-text-bold">1 July 2024</div>
      </div>
    </div>

    <div class="meta-cell">
      <svg class="meta-icon" viewBox="0 0 26 26" fill="none">
        <path d="M3.5 5.5C6.5 4.5 10.5 5 13 7C15.5 5 19.5 4.5 22.5 5.5V20C19.5 19 15.5 19.5 13 21.5C10.5 19.5 6.5 19 3.5 20V5.5Z" fill="#FFF7E0" stroke="#0C2540" stroke-width="1.9" stroke-linejoin="round"/>
        <line x1="13" y1="7" x2="13" y2="21.5" stroke="#0C2540" stroke-width="1.7"/>
      </svg>
      <div>
        <div class="meta-text-bold">{{{{CHAPTER_NUM}}}}</div>
        <div class="meta-text-sub">{{{{CHAPTER_NAME}}}}</div>
      </div>
    </div>
  </section>

  <!-- 3 SECTION CARDS -->
  <section class="cards-grid">
    <!-- CARD 1 -->
    <article class="card card-1">
      <div class="card-accent-strip"></div>
      <div class="card-inner">
        <div class="card-head">
          <div class="card-badge-row">
            <div class="num-seal">{{{{N1}}}}</div>
            <div class="sec-ribbon">Section {{{{S1}}}}</div>
          </div>
          <h2 class="card-title">{{{{TITLE1}}}}</h2>
          <div class="card-rule"></div>
        </div>

        <div class="card-explain-block">
          <div class="easy-pill"><span class="easy-dot"></span> Easy Explanation</div>
          <p class="card-body">{{{{EASY1}}}}</p>
          <div class="subs-row">{{{{SUBS1}}}}</div>
        </div>

        <div class="illus-panel">
          {{{{ILLUS1}}}}
        </div>

        <div class="takeaway-box">
          <div class="takeaway-tag">✓ Key Takeaway</div>
          <div class="takeaway-text">{{{{TAKE1}}}}</div>
        </div>
      </div>
    </article>

    <!-- CARD 2 -->
    <article class="card card-2">
      <div class="card-accent-strip"></div>
      <div class="card-inner">
        <div class="card-head">
          <div class="card-badge-row">
            <div class="num-seal">{{{{N2}}}}</div>
            <div class="sec-ribbon">Section {{{{S2}}}}</div>
          </div>
          <h2 class="card-title">{{{{TITLE2}}}}</h2>
          <div class="card-rule"></div>
        </div>

        <div class="card-explain-block">
          <div class="easy-pill"><span class="easy-dot"></span> Easy Explanation</div>
          <p class="card-body">{{{{EASY2}}}}</p>
          <div class="subs-row">{{{{SUBS2}}}}</div>
        </div>

        <div class="illus-panel">
          {{{{ILLUS2}}}}
        </div>

        <div class="takeaway-box">
          <div class="takeaway-tag">✓ Key Takeaway</div>
          <div class="takeaway-text">{{{{TAKE2}}}}</div>
        </div>
      </div>
    </article>

    <!-- CARD 3 -->
    <article class="card card-3">
      <div class="card-accent-strip"></div>
      <div class="card-inner">
        <div class="card-head">
          <div class="card-badge-row">
            <div class="num-seal">{{{{N3}}}}</div>
            <div class="sec-ribbon">Section {{{{S3}}}}</div>
          </div>
          <h2 class="card-title">{{{{TITLE3}}}}</h2>
          <div class="card-rule"></div>
        </div>

        <div class="card-explain-block">
          <div class="easy-pill"><span class="easy-dot"></span> Easy Explanation</div>
          <p class="card-body">{{{{EASY3}}}}</p>
          <div class="subs-row">{{{{SUBS3}}}}</div>
        </div>

        <div class="illus-panel">
          {{{{ILLUS3}}}}
        </div>

        <div class="takeaway-box">
          <div class="takeaway-tag">✓ Key Takeaway</div>
          <div class="takeaway-text">{{{{TAKE3}}}}</div>
        </div>
      </div>
    </article>
  </section>

  <!-- CTA STRIP + STICKY NOTE -->
  <section class="cta-zone">
    <div class="cta-ribbon">
      Like <span>•</span> Comment <span>•</span> Follow
    </div>
    <div class="cta-sub">to stay updated with more such legal insights!</div>
    <div class="cta-actions">
      <div class="cta-item">
        <div class="cta-icon-circle" style="background:#F7D5DC;">
          <svg width="14" height="13" viewBox="0 0 20 18"><path d="M10 16.5C10 16.5 1.8 11.4 1.8 5.8C1.8 3.1 3.9 1.3 6.3 1.3C7.9 1.3 9.2 2.1 10 3.4C10.8 2.1 12.1 1.3 13.7 1.3C16.1 1.3 18.2 3.1 18.2 5.8C18.2 11.4 10 16.5 10 16.5Z" fill="#DF4C4C" stroke="#0C2540" stroke-width="1.4"/></svg>
        </div>
        <div>
          <div class="cta-item-title">Like</div>
          <div class="cta-item-desc">Found this<br>helpful?</div>
        </div>
      </div>

      <div class="cta-item">
        <div class="cta-icon-circle" style="background:#CBECE4;">
          <svg width="14" height="14" viewBox="0 0 20 20" fill="none"><path d="M3 4.5H17V13.5H8.5L4.5 17V13.5H3V4.5Z" fill="#2B8E82" stroke="#0C2540" stroke-width="1.4" stroke-linejoin="round"/><line x1="6" y1="8" x2="14" y2="8" stroke="#FFFFFF" stroke-width="1.4" stroke-linecap="round"/><line x1="6" y1="10.5" x2="12" y2="10.5" stroke="#FFFFFF" stroke-width="1.4" stroke-linecap="round"/></svg>
        </div>
        <div>
          <div class="cta-item-title">Comment</div>
          <div class="cta-item-desc">Your thoughts<br>matter!</div>
        </div>
      </div>

      <div class="cta-item">
        <div class="cta-icon-circle" style="background:#E6DAF8;">
          <svg width="14" height="14" viewBox="0 0 20 20" fill="none"><circle cx="8.5" cy="7" r="3" stroke="#0C2540" stroke-width="1.5" fill="#FFFFFF"/><path d="M3 16C3 13 5.5 11.5 8.5 11.5C11.5 11.5 14 13 14 16" stroke="#0C2540" stroke-width="1.5" stroke-linecap="round"/><path d="M15.5 7V11M13.5 9H17.5" stroke="#4B3573" stroke-width="1.8" stroke-linecap="round"/></svg>
        </div>
        <div>
          <div class="cta-item-title">Follow</div>
          <div class="cta-item-desc">for more<br>legal updates!</div>
        </div>
      </div>
    </div>

    <div class="sticky-note">
      <div class="sticky-pin"></div>
      <div class="sticky-text">
        Better Knowledge<br>
        Better Decisions ☺
      </div>
    </div>
  </section>

  <!-- CLEAN EDITORIAL FOOTER BAR -->
  <footer class="footer-bar">
    <svg class="wheat-left" viewBox="0 0 36 74" fill="none">
      <path d="M18 70 Q16 38 22 6" stroke="#DDA114" stroke-width="1.6" stroke-linecap="round"/>
      <ellipse cx="13" cy="54" rx="4" ry="7" transform="rotate(-32 13 54)" stroke="#DDA114" stroke-width="1.4"/>
      <ellipse cx="24" cy="48" rx="4" ry="7" transform="rotate(28 24 48)" stroke="#DDA114" stroke-width="1.4"/>
      <ellipse cx="12" cy="36" rx="4" ry="7" transform="rotate(-30 12 36)" stroke="#DDA114" stroke-width="1.4"/>
      <ellipse cx="25" cy="30" rx="4" ry="7" transform="rotate(26 25 30)" stroke="#DDA114" stroke-width="1.4"/>
      <ellipse cx="14" cy="20" rx="3.5" ry="6" transform="rotate(-24 14 20)" stroke="#DDA114" stroke-width="1.4"/>
    </svg>
    <svg class="wheat-right" viewBox="0 0 36 74" fill="none">
      <path d="M18 70 Q16 38 22 6" stroke="#DDA114" stroke-width="1.6" stroke-linecap="round"/>
      <ellipse cx="13" cy="54" rx="4" ry="7" transform="rotate(-32 13 54)" stroke="#DDA114" stroke-width="1.4"/>
      <ellipse cx="24" cy="48" rx="4" ry="7" transform="rotate(28 24 48)" stroke="#DDA114" stroke-width="1.4"/>
      <ellipse cx="12" cy="36" rx="4" ry="7" transform="rotate(-30 12 36)" stroke="#DDA114" stroke-width="1.4"/>
      <ellipse cx="25" cy="30" rx="4" ry="7" transform="rotate(26 25 30)" stroke="#DDA114" stroke-width="1.4"/>
      <ellipse cx="14" cy="20" rx="3.5" ry="6" transform="rotate(-24 14 20)" stroke="#DDA114" stroke-width="1.4"/>
    </svg>

    <div class="footer-top-row">
      <span class="footer-hairline"></span>
      <div class="site-pill">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="9.5" stroke="#091E36" stroke-width="2"/>
          <ellipse cx="12" cy="12" rx="4.2" ry="9.5" stroke="#091E36" stroke-width="1.6"/>
          <line x1="2.8" y1="12" x2="21.2" y2="12" stroke="#091E36" stroke-width="1.6"/>
        </svg>
        <span>linpanelegalservices.in</span>
      </div>
      <span class="footer-hairline"></span>
    </div>

    <div class="socials-row">
      <div class="social-item">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <rect x="2.5" y="2.5" width="19" height="19" rx="5" stroke="#F4C44E" stroke-width="2"/>
          <circle cx="12" cy="12" r="4.2" stroke="#F4C44E" stroke-width="2"/>
          <circle cx="17.2" cy="6.8" r="1.3" fill="#F4C44E"/>
        </svg>
        <span>linpane_legal_services</span>
      </div>

      <div class="social-item">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="#F4C44E">
          <path d="M18.2 2H21.5L14.3 10.2L22.8 22H16.1L10.9 15.1L4.9 22H1.6L9.3 13.2L1.2 2H8.1L12.8 8.3L18.2 2ZM17 20H18.9L7.1 3.9H5.1L17 20Z"/>
        </svg>
        <span>@linpanelegal</span>
      </div>

      <div class="social-item">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <rect x="2.5" y="2.5" width="19" height="19" rx="4" stroke="#F4C44E" stroke-width="2"/>
          <text x="12" y="16.5" text-anchor="middle" font-family="Arial,sans-serif" font-weight="800" font-size="13" fill="#F4C44E">in</text>
        </svg>
        <span>linpanelegalservicess</span>
      </div>
    </div>

    <div class="footer-tagline">Law Made Simple &nbsp;|&nbsp; Knowledge Builds Confidence &nbsp;|&nbsp; Together for a Safer Tomorrow</div>
  </footer>
</div>
</body>
</html>
"""

    out_path = HERE / "locked_template_v3.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path} ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
