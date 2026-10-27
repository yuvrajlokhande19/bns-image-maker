"""
build_template.py  — Creates the master locked_template.html with all assets embedded.

Fixes applied:
1. Header: Locked, clean, full-width with big logo and brand name.
2. Lady Justice: Mounted directly ON the top curve of the 'S' in BNS (bns-s-wrapper),
   properly sized, positioned, and never colliding with the header.
3. Gavel & Books: Uses the authentic, full-color illustrated gavel resting on the
   round soundblock plate on top of the books stack from the reference.
4. Cards: Uses justify-content: space-between and balanced groups so there are
   no awkward blank spaces at the bottom.
5. Subchip tags: Fully styled with dashed borders.
"""
import base64
from pathlib import Path

HERE  = Path(__file__).parent
ROOT  = HERE.parent
HTML  = ROOT / "html"

def b64(path: Path) -> str:
    raw  = path.read_bytes()
    data = base64.b64encode(raw).decode()
    ext  = path.suffix.lstrip(".")
    mime = "image/jpeg" if ext in ("jpg","jpeg") else f"image/{ext}"
    return f"data:{mime};base64,{data}"

LOGO      = b64(HTML / "logo.png")
LAWNOTES  = b64(HTML / "lawnotes.png")
LADY      = b64(HERE / "lady_justice_trimmed.png")
GAVEL_BKS = b64(HERE / "gavel_books_final.png")

TEMPLATE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Linpane Legal Services — BNS Series</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Caveat+Brush&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Mukta:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --paper:   #FAF6EE;
  --paper2:  #FBF7EC;
  --navy:    #0B2444;
  --navy2:   #0E3A5D;
  --gold:    #F3C64D;
  --yellow:  #F5C94A;
  --teal:    #2D8C82;
  --mint:    #CBE8DF;
  --lav:     #D8C8F0;
  --pink:    #F5D0D8;
  --ink:     #1E293B;
  --muted:   #475569;
  --border1: #1A365D;
  --border2: #1E6B52;
}}

*, *::before, *::after {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  background: #aca495;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
}}

/* ── 1080x1350 CANVAS ── */
.page {{
  width: 1080px;
  height: 1350px;
  background: var(--paper);
  overflow: hidden;
  position: relative;
  font-family: 'Poppins', Arial, sans-serif;
  color: var(--ink);
  display: flex;
  flex-direction: column;
}}

/* Subtle paper texture */
.grain {{
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 200;
  opacity: .35;
}}

/* ═══════════════════════════════════════════════════════════════════
   ZONE 1 — LOCKED TOP HEADER (Corner to Corner)
   ═══════════════════════════════════════════════════════════════════ */
.top-header {{
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 20px 8px 20px;
  border-bottom: 3.5px solid var(--gold);
  background: var(--paper);
}}
.brand-seal {{
  width: 78px;
  height: 78px;
  flex: 0 0 78px;
  border-radius: 50%;
  border: 3px solid var(--gold);
  object-fit: cover;
  background: var(--navy);
  box-shadow: 0 3px 8px rgba(11,36,68,.25);
}}
.brand-info {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}}
.brand-svg {{
  width: 100%;
  height: 52px;
  display: block;
}}
.brand-sub {{
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 3px;
  color: #556270;
  margin-top: 2px;
}}

/* ═══════════════════════════════════════════════════════════════════
   ZONE 2 — LOCKED UPPER HERO (3 Columns)
   ═══════════════════════════════════════════════════════════════════ */
.hero-row {{
  flex: 0 0 auto;
  display: grid;
  grid-template-columns: 255px 1fr 245px;
  gap: 0;
  padding: 10px 20px 6px 20px;
  align-items: start;
}}

/* ── Left Column: Info Presents + Law Notes ── */
.hero-left {{
  display: flex;
  flex-direction: column;
  gap: 3px;
}}
.ribbon-info {{
  display: inline-block;
  background: var(--yellow);
  color: var(--navy);
  font-family: 'Caveat Brush', cursive;
  font-size: 22px;
  padding: 2px 16px 3px;
  transform: rotate(-3deg);
  border-radius: 14px 4px 16px 5px;
  box-shadow: 1px 2px 0 rgba(11,36,68,.14);
  width: fit-content;
}}
.heading-basic {{
  font-family: 'Caveat Brush', cursive;
  font-size: 36px;
  color: #1a1a1a;
  line-height: 1.0;
  margin-top: 6px;
}}
.byline-sub {{
  font-size: 12.5px;
  color: #4a545e;
}}
.tagline-simple {{
  margin-top: 6px;
  font-size: 12px;
  color: var(--navy);
  font-weight: 500;
  line-height: 1.5;
}}
.tagline-simple b {{
  font-family: 'Caveat Brush', cursive;
  font-size: 18px;
  font-weight: 400;
}}
.lawnotes-badge {{
  width: 96px;
  height: auto;
  margin-top: 10px;
  object-fit: contain;
  background: transparent;
  filter: drop-shadow(0 2px 5px rgba(0,0,0,.15));
  display: block;
}}

/* ── Center Column: BNS Title Block + Lady Justice on N ── */
.hero-center {{
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding-top: 110px; /* Ample space above BNS for Lady Justice to stand on N */
}}

.bns-word-container {{
  position: relative;
  display: inline-flex;
  align-items: baseline;
  justify-content: center;
  line-height: 1.0;
}}

.bns-letter {{
  font-family: 'Anton', sans-serif;
  font-size: 136px;
  line-height: 1.0;
  letter-spacing: 4px;
  background: linear-gradient(180deg, #185f94 0%, #0E3A5D 45%, #0B2444 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-stroke: 3px var(--yellow);
  filter:
    drop-shadow(3px 3px 0px rgba(245,201,74,1))
    drop-shadow(6px 6px 0px rgba(245,201,74,.5))
    drop-shadow(8px 8px 12px rgba(11,36,68,.3));
  position: relative;
  z-index: 3;
}}

/* The N wrapper holds the letter 'N' and locks Lady Justice right on top of it */
.bns-n-wrapper {{
  position: relative;
  display: inline-block;
  overflow: visible;
}}

/*
   Lady Justice sits directly on top of the middle letter 'N':
   - bottom: calc(100% - 16px) aligns statue pedestal with the top apex/edge of 'N'
   - left: 50% centers her symmetrically in the center of BNS
   - height: 130px ensures a strong, bold presence with no empty gap above BNS
   - z-index: 5 ensures she is crisp and fully in front
*/
.lady-on-n {{
  position: absolute;
  bottom: calc(100% - 16px);
  left: 50%;
  transform: translateX(-50%);
  height: 130px;
  width: auto;
  object-fit: contain;
  z-index: 5;
  filter: drop-shadow(0 3px 6px rgba(0,0,0,.22));
}}

.act-title-brush {{
  margin-top: 6px;
  position: relative;
  display: inline-block;
  padding: 0 10px;
}}
.act-title-brush span {{
  font-weight: 800;
  font-size: 23px;
  line-height: 1.35;
  letter-spacing: .5px;
  color: var(--navy);
  background: linear-gradient(transparent 42%, var(--yellow) 42%, var(--yellow) 88%, transparent 88%);
}}

.series-badge-pill {{
  margin-top: 8px;
  background: var(--navy);
  color: var(--yellow);
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 2px;
  padding: 6px 20px;
  border: 2px dashed var(--yellow);
  border-radius: 12px;
  text-align: center;
  white-space: nowrap;
}}

.trilingual-motto {{
  margin-top: 5px;
  font-family: 'Mukta', 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 12.5px;
  color: var(--navy);
}}
.trilingual-motto .dot {{
  color: var(--gold);
  padding: 0 6px;
}}

/* ── Right Column: Quote + Gavel on Books ── */
.hero-right {{
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right;
  gap: 4px;
  padding-top: 8px;
}}
.quote-newlaw {{
  font-family: 'Caveat Brush', cursive;
  font-size: 21px;
  line-height: 1.22;
  color: #1a1a1a;
}}
.quote-newlaw u {{
  text-decoration-color: var(--yellow);
  text-decoration-thickness: 3px;
}}
.gavel-books-graphic {{
  width: 220px;
  height: auto;
  object-fit: contain;
  margin-top: 4px;
  filter: drop-shadow(2px 4px 8px rgba(0,0,0,.15));
}}

/* ═══════════════════════════════════════════════════════════════════
   ZONE 3 — DYNAMIC MIDDLE (Metadata Bar + 3 Cards)
   ═══════════════════════════════════════════════════════════════════ */
#middle-bns-zone {{
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  padding: 4px 20px 6px 20px;
}}

/* Full-width metadata bar */
.metadata-strip {{
  flex: 0 0 58px;
  background: var(--paper2);
  border: 2px solid #b9a77e;
  border-radius: 14px 6px 16px 6px;
  display: flex;
  align-items: stretch;
  margin-bottom: 8px;
}}
.strip-cell {{
  flex: 1;
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: center;
  padding: 4px 10px;
}}
.strip-cell + .strip-cell {{
  border-left: 2px solid #b9a77e;
}}
.strip-cell svg {{
  width: 36px;
  height: 36px;
  flex: 0 0 36px;
}}
.cell-t1 {{
  font-weight: 700;
  color: var(--navy);
  font-size: 13.5px;
  line-height: 1.3;
}}
.cell-t2 {{
  font-size: 12px;
  color: #4a545e;
  line-height: 1.3;
}}

/* ── 3 Section Cards ── */
.cards-container {{
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  min-height: 0;
}}

.section-card {{
  background: #FFFDF7;
  border: 2.5px solid var(--border1);
  border-radius: 20px;
  padding: 16px 14px 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  height: 100%;
}}
.section-card.card-alt {{
  border-color: var(--border2);
}}

/* Card Top Row */
.card-head {{
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 0 0 auto;
}}
.num-circle {{
  width: 54px;
  height: 54px;
  flex: 0 0 54px;
  border-radius: 50%;
  background: var(--navy);
  color: #fff;
  font-family: 'Anton', sans-serif;
  font-size: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.section-badge-pill {{
  flex: 1;
  background: var(--yellow);
  text-align: center;
  font-weight: 700;
  color: var(--navy);
  font-size: 16px;
  padding: 6px 4px;
  border-radius: 4px 16px 5px 14px;
  transform: rotate(-.5deg);
}}

/* Card Title */
.card-title {{
  font-weight: 700;
  color: var(--navy);
  font-size: 17.5px;
  line-height: 1.25;
  text-align: center;
  margin: 8px 0 6px;
  flex: 0 0 auto;
}}

/* Easy Explanation Pill */
.pill-easy {{
  align-self: center;
  font-weight: 600;
  font-size: 13px;
  color: var(--navy);
  padding: 4px 22px;
  border-radius: 14px;
  margin-bottom: 6px;
  flex: 0 0 auto;
}}
.pill-easy.pink {{ background: var(--pink); }}
.pill-easy.mint {{ background: var(--mint); }}

/* Easy Text */
.card-body-text {{
  font-size: 13px;
  line-height: 1.48;
  color: #2b3542;
  flex: 0 0 auto;
}}

/* Subchip Tags */
.tags-row {{
  display: flex;
  gap: 6px;
  justify-content: center;
  flex-wrap: wrap;
  margin: 6px 0 4px;
  flex: 0 0 auto;
}}
.subchip {{
  font-size: 11px;
  font-weight: 600;
  color: var(--navy);
  background: #EDF3FA;
  border: 1.5px dashed #2e7f76;
  border-radius: 10px;
  padding: 2.5px 11px;
  white-space: nowrap;
}}

/* Illustration Box */
.card-illustration {{
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80px;
  max-height: 135px;
  margin: 4px 0;
  overflow: hidden;
}}
.card-illustration svg {{
  width: 100%;
  height: 100%;
}}

/* Key Takeaway */
.pill-takeaway {{
  align-self: center;
  font-weight: 600;
  font-size: 12.5px;
  color: var(--navy);
  padding: 3.5px 20px;
  border-radius: 14px;
  margin: 4px 0 3px;
  flex: 0 0 auto;
}}
.pill-takeaway.lav {{ background: var(--lav); }}
.pill-takeaway.mint {{ background: var(--mint); }}

.card-takeaway-text {{
  font-size: 13px;
  line-height: 1.42;
  color: #2b3542;
  text-align: center;
  flex: 0 0 auto;
}}

/* ═══════════════════════════════════════════════════════════════════
   ZONE 4 — LOCKED CTA + FOOTER
   ═══════════════════════════════════════════════════════════════════ */
.cta-zone {{
  flex: 0 0 auto;
  position: relative;
  padding: 4px 20px 6px 20px;
}}
.cta-brush-bar {{
  background: var(--navy);
  color: #fff;
  text-align: center;
  font-family: 'Caveat Brush', cursive;
  font-size: 24px;
  padding: 3px 0;
  border-radius: 8px 30px 10px 32px;
  letter-spacing: 1px;
}}
.cta-brush-bar b {{
  color: var(--yellow);
  font-weight: 400;
}}
.cta-subtitle {{
  text-align: center;
  font-size: 12.5px;
  color: #4a545e;
  margin: 2px 0 4px;
}}
.engagement-row {{
  display: flex;
  justify-content: center;
  gap: 34px;
  align-items: flex-start;
}}
.eng-item {{
  display: flex;
  gap: 7px;
  align-items: center;
  font-size: 11.5px;
  color: #2f3844;
  line-height: 1.3;
}}
.eng-item svg {{
  width: 36px;
  height: 36px;
  flex: 0 0 36px;
}}
.eng-item b {{
  display: block;
  color: var(--navy);
  font-size: 12.5px;
}}

/* Sticky note on right */
.sticky-note {{
  position: absolute;
  right: 22px;
  top: 32px;
  width: 140px;
  background: #FBD47B;
  padding: 8px 8px 10px;
  font-family: 'Caveat Brush', cursive;
  font-size: 18px;
  line-height: 1.15;
  color: #3a2f10;
  text-align: center;
  transform: rotate(4deg);
  box-shadow: 2px 3px 8px rgba(0,0,0,.2);
}}
.sticky-note::before {{
  content: '';
  position: absolute;
  top: -10px;
  left: 50%;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #c0392b;
  transform: translateX(-50%);
  box-shadow: 0 2px 3px rgba(0,0,0,.3);
}}

/* Navy Footer */
.footer-bar {{
  background: var(--navy);
  color: #fff;
  text-align: center;
  padding: 4px 20px 8px 20px;
  flex: 0 0 auto;
  position: relative;
}}
.footer-bar .wave {{
  display: block;
  width: 100%;
  height: 15px;
  margin: 0;
}}
.actions-row {{
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 2px 0;
}}
.action-link {{
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 1px;
}}
.action-link svg {{
  width: 24px;
  height: 24px;
  flex: 0 0 24px;
}}
.website-pill-center {{
  text-align: center;
  margin: 3px 0;
}}
.sitepill {{
  background: var(--yellow);
  border-radius: 38px 44px 36px 42px;
  padding: 6px 20px;
  font-weight: 700;
  color: var(--navy);
  font-size: 16px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 2px 2px 0 rgba(11,36,68,.15);
}}
.socials-row {{
  display: flex;
  justify-content: center;
  gap: 22px;
  margin: 3px 0 2px;
}}
.soc-item {{
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
}}
.soc-item svg {{
  width: 24px;
  height: 24px;
  flex: 0 0 24px;
}}
.disclaimer-line {{
  font-size: 11px;
  color: #c8d4de;
  margin-top: 3px;
}}
.wheat-leaf {{
  position: absolute;
  bottom: 6px;
  width: 60px;
  height: 96px;
  opacity: .88;
}}
.wheat-leaf.left {{ left: 14px; }}
.wheat-leaf.right {{ right: 14px; transform: scaleX(-1); }}
</style>
</head>
<body>
<div class="page">

  <!-- Grain texture -->
  <svg class="grain" width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
    <filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".82" numOctaves="2"/>
    <feColorMatrix values="0 0 0 0 .52 0 0 0 0 .47 0 0 0 0 .38 0 0 0 .05 0"/></filter>
    <rect width="1080" height="1350" filter="url(#g)"/>
  </svg>

  <!-- ══════════════════════════════════════════
       ZONE 1 — LOCKED TOP HEADER (Corner to Corner)
       ══════════════════════════════════════════ -->
  <div class="top-header">
    <img class="brand-seal" src="{LOGO}" alt="Linpane Seal">
    <div class="brand-info">
      <svg class="brand-svg" viewBox="0 0 940 52" preserveAspectRatio="none">
        <text x="0" y="44" font-family="'Anton', sans-serif" font-size="52" fill="#0B2444" letter-spacing="1.2" textLength="940" lengthAdjust="spacingAndGlyphs">LINPANE LEGAL SERVICES</text>
      </svg>
      <div class="brand-sub">YOUR RIGHTS &nbsp;|&nbsp; OUR PRIORITY</div>
    </div>
  </div>

  <!-- ══════════════════════════════════════════
       ZONE 2 — LOCKED UPPER HERO
       ══════════════════════════════════════════ -->
  <div class="hero-row">

    <!-- LEFT COLUMN -->
    <div class="hero-left">
      <span class="ribbon-info">Info Presents</span>
      <div class="heading-basic">Basic of Law</div>
      <div class="byline-sub">by Linpane Legal Services</div>
      <div class="tagline-simple">Simple Laws &nbsp;|&nbsp; Better Awareness<br><b>A Stronger You ♡</b></div>
      <img class="lawnotes-badge" src="{LAWNOTES}" alt="Law Notes">
    </div>

    <!-- CENTER COLUMN -->
    <div class="hero-center">
      <!-- BNS WORD with Lady Justice locked directly on the letter 'N' -->
      <div class="bns-word-container">
        <span class="bns-letter">B</span>
        <span class="bns-letter bns-n-wrapper">
          N
          <img class="lady-on-n" src="{LADY}" alt="Lady Justice">
        </span>
        <span class="bns-letter">S</span>
      </div>

      <div class="act-title-brush">
        <span>THE BHARATIYA NYAYA<br>SANHITA, 2023</span>
      </div>

      <!-- 🟡 Dynamic series badge -->
      <div class="series-badge-pill" id="series-stamp-badge">
        {{{{SERIES_MARK}}}} / BNS SERIES &bull; SECTIONS {{{{SECTIONS_RANGE}}}}
      </div>
      <div class="trilingual-motto">
        Know the Law<span class="dot">•</span>कानून जानें<span class="dot">•</span>कायदा जाणून घ्या
      </div>
    </div>

    <!-- RIGHT COLUMN -->
    <div class="hero-right">
      <div class="quote-newlaw">Know the Law.<br><u>For Safer Tomorrow.</u></div>
      <!-- Authentic illustrated gavel on soundblock on books -->
      <img class="gavel-books-graphic" src="{GAVEL_BKS}" alt="Justice Fairness Equality">
    </div>

  </div><!-- /hero-row -->

  <!-- ══════════════════════════════════════════
       ZONE 3 — DYNAMIC MIDDLE (Cards)
       ══════════════════════════════════════════ -->
  <div id="middle-bns-zone">

    <!-- Metadata bar -->
    <div class="metadata-strip">
      <div class="strip-cell">
        <svg viewBox="0 0 46 46"><rect x="7" y="10" width="32" height="28" rx="4" fill="none" stroke="#0B2444" stroke-width="2.8"/><line x1="7" y1="18" x2="39" y2="18" stroke="#0B2444" stroke-width="2.8"/><rect x="12" y="8" width="4" height="7" fill="#0B2444"/><rect x="30" y="8" width="4" height="7" fill="#0B2444"/><g fill="#0B2444"><rect x="13" y="23" width="5" height="5"/><rect x="21" y="23" width="5" height="5"/><rect x="29" y="23" width="5" height="5"/><rect x="13" y="30" width="5" height="5"/><rect x="21" y="30" width="5" height="5"/></g></svg>
        <div><div class="cell-t1">BNS is Act No. 45 of 2023</div><div class="cell-t2">Enacted on 25 December 2023</div></div>
      </div>
      <div class="strip-cell">
        <svg viewBox="0 0 46 46"><path d="M23 5 L37 11 V22 C37 32 30 38 23 41 C16 38 9 32 9 22 V11 Z" fill="none" stroke="#0B2444" stroke-width="2.8"/><path d="M17 22 l5 5 8 -10" fill="none" stroke="#0B2444" stroke-width="3.2" stroke-linecap="round"/></svg>
        <div><div class="cell-t2">Comes into force from</div><div class="cell-t1">1 July 2024</div></div>
      </div>
      <div class="strip-cell">
        <svg viewBox="0 0 46 46"><path d="M23 8 Q14 3 6 7 V34 Q14 30 23 35 Q32 30 40 34 V7 Q32 3 23 8" fill="none" stroke="#0B2444" stroke-width="2.8"/><line x1="23" y1="8" x2="23" y2="35" stroke="#0B2444" stroke-width="2.8"/></svg>
        <div>
          <div class="cell-t1" id="chapter-number">{{{{CHAPTER_NUM}}}}</div>
          <div class="cell-t2" id="chapter-name">{{{{CHAPTER_NAME}}}}</div>
        </div>
      </div>
    </div>

    <!-- 3 SECTION CARDS -->
    <div class="cards-container">

      <!-- CARD 1 -->
      <div class="section-card" id="bns-card-1">
        <div class="card-top-group">
          <div class="card-head">
            <div class="num-circle">{{{{N1}}}}</div>
            <div class="section-badge-pill">Section {{{{S1}}}}</div>
          </div>
          <div class="card-title">{{{{TITLE1}}}}</div>
          <div style="display:flex; justify-content:center;">
            <div class="pill-easy pink">Easy Explanation</div>
          </div>
          <div class="card-body-text">{{{{EASY1}}}}</div>
          <div class="tags-row">{{{{SUBS1}}}}</div>
        </div>

        <div class="card-illustration">
          <svg viewBox="0 0 280 120" xmlns="http://www.w3.org/2000/svg">
            <!-- BNS Book -->
            <g transform="rotate(-7,72,75)">
              <rect x="14" y="10" width="88" height="106" rx="6"
                fill="#0E3A5D" stroke="#092B45" stroke-width="3"/>
              <rect x="22" y="18" width="72" height="90" rx="3"
                fill="none" stroke="#F5C94A" stroke-width="2"/>
              <rect x="14" y="10" width="10" height="106" rx="3"
                fill="#173F35" stroke="#092B45" stroke-width="1.5"/>
              <text x="58" y="50" text-anchor="middle"
                fill="#F5C94A" font-size="19" font-weight="700" font-family="Poppins">BNS</text>
              <text x="58" y="70" text-anchor="middle"
                fill="#fff" font-size="16" font-weight="700" font-family="Poppins">2023</text>
              <g stroke="#F5C94A" stroke-width="1.8" fill="none" transform="translate(36,76)">
                <line x1="10" y1="0" x2="34" y2="0"/>
                <line x1="22" y1="0" x2="22" y2="18"/>
                <line x1="10" y1="0" x2="3" y2="12"/>
                <line x1="10" y1="0" x2="17" y2="12"/>
                <line x1="34" y1="0" x2="27" y2="12"/>
                <line x1="34" y1="0" x2="41" y2="12"/>
              </g>
            </g>
            <!-- Pillar -->
            <g transform="translate(162,8)">
              <rect x="2" y="0" width="68" height="14" rx="4"
                fill="#c9b896" stroke="#092B45" stroke-width="2.2"/>
              <g stroke="#092B45" stroke-width="2">
                <rect x="8" y="14" width="10" height="76" fill="#e8dcc8"/>
                <rect x="24" y="14" width="10" height="76" fill="#ddd0b6"/>
                <rect x="40" y="14" width="10" height="76" fill="#e8dcc8"/>
                <rect x="56" y="14" width="10" height="76" fill="#ddd0b6"/>
              </g>
              <rect x="0" y="88" width="72" height="12" rx="3"
                fill="#c9b896" stroke="#092B45" stroke-width="2.2"/>
            </g>
            <text x="250" y="72" text-anchor="end"
              font-family="Caveat Brush" font-size="13" fill="#22303C">One Law.</text>
            <text x="250" y="88" text-anchor="end"
              font-family="Caveat Brush" font-size="13" fill="#22303C">Wide Application.</text>
          </svg>
        </div>

        <div class="card-bottom-group">
          <div style="display:flex; justify-content:center;">
            <div class="pill-takeaway lav">✔ Key Takeaway</div>
          </div>
          <div class="card-takeaway-text">{{{{TAKE1}}}}</div>
        </div>
      </div>

      <!-- CARD 2 -->
      <div class="section-card card-alt" id="bns-card-2">
        <div class="card-top-group">
          <div class="card-head">
            <div class="num-circle">{{{{N2}}}}</div>
            <div class="section-badge-pill">Section {{{{S2}}}}</div>
          </div>
          <div class="card-title">{{{{TITLE2}}}}</div>
          <div style="display:flex; justify-content:center;">
            <div class="pill-easy mint">Easy Explanation</div>
          </div>
          <div class="card-body-text">{{{{EASY2}}}}</div>
          <div class="tags-row">{{{{SUBS2}}}}</div>
        </div>

        <div class="card-illustration">
          <svg viewBox="0 0 280 120" xmlns="http://www.w3.org/2000/svg">
            <g transform="rotate(-3,95,70)">
              <path d="M28 16 Q58 12 96 16 L96 116 Q58 112 28 116 Z"
                fill="#fbf4e2" stroke="#092B45" stroke-width="2.5"/>
              <path d="M96 16 Q134 12 164 16 L164 116 Q134 112 96 116 Z"
                fill="#f5eed8" stroke="#092B45" stroke-width="2.5"/>
              <line x1="96" y1="16" x2="96" y2="116"
                stroke="#092B45" stroke-width="3"/>
              <text x="52" y="34" text-anchor="middle"
                font-size="11" font-weight="700" fill="#092B45" font-family="Poppins">DEFINITIONS</text>
              <g stroke="#9aa4ad" stroke-width="1.6">
                <line x1="36" y1="46" x2="88" y2="46"/>
                <line x1="36" y1="58" x2="88" y2="58"/>
                <line x1="36" y1="70" x2="88" y2="70"/>
                <line x1="36" y1="82" x2="88" y2="82"/>
                <line x1="36" y1="94" x2="88" y2="94"/>
                <line x1="36" y1="104" x2="88" y2="104"/>
              </g>
              <g font-family="Poppins" font-size="11" fill="#2c3e50">
                <text x="104" y="48">Words</text>
                <text x="104" y="64">Terms</text>
                <text x="104" y="80">Meanings</text>
                <text x="104" y="96">Clarity</text>
                <text x="104" y="110">Scope</text>
              </g>
            </g>
            <circle cx="204" cy="74" r="34"
              fill="#dbe9f5" opacity=".88" stroke="#092B45" stroke-width="3.5"/>
            <circle cx="204" cy="74" r="24"
              fill="none" stroke="#8fb4d6" stroke-width="1.8"/>
            <line x1="229" y1="98" x2="254" y2="120"
              stroke="#092B45" stroke-width="10" stroke-linecap="round"/>
            <line x1="229" y1="98" x2="254" y2="120"
              stroke="#1c5d8a" stroke-width="4.5" stroke-linecap="round"/>
          </svg>
        </div>

        <div class="card-bottom-group">
          <div style="display:flex; justify-content:center;">
            <div class="pill-takeaway mint">✔ Key Takeaway</div>
          </div>
          <div class="card-takeaway-text">{{{{TAKE2}}}}</div>
        </div>
      </div>

      <!-- CARD 3 -->
      <div class="section-card" id="bns-card-3">
        <div class="card-top-group">
          <div class="card-head">
            <div class="num-circle">{{{{N3}}}}</div>
            <div class="section-badge-pill">Section {{{{S3}}}}</div>
          </div>
          <div class="card-title">{{{{TITLE3}}}}</div>
          <div style="display:flex; justify-content:center;">
            <div class="pill-easy pink">Easy Explanation</div>
          </div>
          <div class="card-body-text">{{{{EASY3}}}}</div>
          <div class="tags-row">{{{{SUBS3}}}}</div>
        </div>

        <div class="card-illustration">
          <svg viewBox="0 0 280 120" xmlns="http://www.w3.org/2000/svg">
            <line x1="40" y1="18" x2="240" y2="18"
              stroke="#0B2444" stroke-width="3.8" stroke-linecap="round"/>
            <line x1="140" y1="18" x2="140" y2="68"
              stroke="#0B2444" stroke-width="3.8"/>
            <circle cx="140" cy="12" r="6" fill="#8a5a2e" stroke="#5d3a17" stroke-width="2"/>
            <line x1="80" y1="18" x2="54" y2="58" stroke="#0B2444" stroke-width="2.4"/>
            <line x1="80" y1="18" x2="106" y2="58" stroke="#0B2444" stroke-width="2.4"/>
            <path d="M46 58 h68 l-6 12 h-56 Z" fill="#c9a24a" stroke="#7a5c1a" stroke-width="2.2"/>
            <line x1="200" y1="18" x2="174" y2="58" stroke="#0B2444" stroke-width="2.4"/>
            <line x1="200" y1="18" x2="226" y2="58" stroke="#0B2444" stroke-width="2.4"/>
            <path d="M166 58 h68 l-6 12 h-56 Z" fill="#c9a24a" stroke="#7a5c1a" stroke-width="2.2"/>
            <rect x="72" y="70" width="136" height="28" rx="5"
              fill="#0E3A5D" stroke="#092B45" stroke-width="2.2"/>
            <text x="140" y="82" text-anchor="middle"
              fill="#F5C94A" font-size="10.5" font-weight="700" font-family="Poppins">LAW</text>
            <text x="140" y="94" text-anchor="middle"
              fill="#fff" font-size="9" font-weight="600" font-family="Poppins">INTERPRETATION</text>
            <g font-family="Poppins" font-size="10.5" font-weight="600">
              <rect x="14" y="100" width="66" height="20" rx="4"
                fill="#F5C94A" transform="rotate(-3,47,110)"/>
              <text x="47" y="113" text-anchor="middle"
                fill="#092B45" transform="rotate(-3,47,110)">Interpret</text>
              <rect x="106" y="102" width="60" height="20" rx="4" fill="#bfe3ef"/>
              <text x="136" y="115" text-anchor="middle" fill="#092B45">Apply</text>
              <rect x="186" y="100" width="80" height="20" rx="4"
                fill="#F2B6C8" transform="rotate(2,226,110)"/>
              <text x="226" y="113" text-anchor="middle"
                fill="#092B45" transform="rotate(2,226,110)">Understand</text>
            </g>
          </svg>
        </div>

        <div class="card-bottom-group">
          <div style="display:flex; justify-content:center;">
            <div class="pill-takeaway lav">✔ Key Takeaway</div>
          </div>
          <div class="card-takeaway-text">{{{{TAKE3}}}}</div>
        </div>
      </div>

    </div><!-- /cards-container -->
  </div><!-- /#middle-bns-zone -->

  <!-- ══════════════════════════════════════════
       ZONE 4 — LOCKED CTA + FOOTER
       ══════════════════════════════════════════ -->
  <div class="cta-zone">
    <div class="cta-brush-bar">Like &nbsp;•&nbsp; <b>Comment</b> &nbsp;•&nbsp; Follow</div>
    <div class="cta-subtitle">to stay updated with more such legal insights!</div>
    <div class="engagement-row">
      <div class="eng-item">
        <svg viewBox="0 0 56 56"><circle cx="28" cy="28" r="24" fill="#F2B6C8"/>
        <path d="M28 41 C17 32 13 27 15.5 21 C17.5 16 24 16.5 28 22 C32 16.5 38.5 16 40.5 21 C43 27 39 32 28 41"
          fill="#e94f7a" stroke="#0B2444" stroke-width="2.2"/></svg>
        <div><b>Like</b>Found this<br>helpful?</div>
      </div>
      <div class="eng-item">
        <svg viewBox="0 0 56 56"><circle cx="28" cy="28" r="24" fill="#74C9C1"/>
        <rect x="14" y="16" width="28" height="20" rx="10" fill="#fff" stroke="#0B2444" stroke-width="2.2"/>
        <path d="M20 36 l-2 7 8 -7" fill="#fff" stroke="#0B2444" stroke-width="2"/>
        <g stroke="#0B2444" stroke-width="2" stroke-linecap="round">
          <line x1="20" y1="24" x2="36" y2="24"/><line x1="20" y1="30" x2="32" y2="30"/>
        </g></svg>
        <div><b>Comment</b>Your thoughts<br>matter!</div>
      </div>
      <div class="eng-item">
        <svg viewBox="0 0 56 56"><circle cx="28" cy="28" r="24" fill="#F2B6C8"/>
        <circle cx="26" cy="22" r="7" fill="#fff" stroke="#0B2444" stroke-width="2.2"/>
        <path d="M13 40 Q15 31 26 31 Q37 31 39 40" fill="#fff" stroke="#0B2444" stroke-width="2.2"/>
        <circle cx="40" cy="36" r="7" fill="#fff" stroke="#0B2444" stroke-width="2"/>
        <path d="M40 33 v6 M37 36 h6" stroke="#0B2444" stroke-width="2"/></svg>
        <div><b>Follow</b>for more<br>legal updates!</div>
      </div>
    </div>
    <div class="sticky-note">Better Knowledge<br>Better Decisions<br>☺</div>
  </div>

  <div class="footer-bar">
    <svg class="wave" viewBox="0 0 1080 15" preserveAspectRatio="none">
      <defs><linearGradient id="fw" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#0B2444" stop-opacity="0"/>
        <stop offset="1" stop-color="#0B2444"/>
      </linearGradient></defs>
      <path d="M0 20 Q135 5 270 12 T540 10 T810 13 T1080 6 L1080 20 Z" fill="url(#fw)"/>
    </svg>
    <div class="actions-row">
      <span class="action-link"><svg viewBox="0 0 24 24"><path d="M7 11V21M7 11l4-7c1.6 0 2.4 1.2 1.8 2.8L11.5 12H19a2 2 0 012 2.4l-1.4 6A2 2 0 0118 22H9a2 2 0 01-2-2v-9z" fill="none" stroke="#F5C94A" stroke-width="2" stroke-linejoin="round"/></svg>Like</span>
      <span class="action-link"><svg viewBox="0 0 24 24"><circle cx="6" cy="12" r="2.6" fill="none" stroke="#F5C94A" stroke-width="2"/><circle cx="17" cy="5.5" r="2.6" fill="none" stroke="#F5C94A" stroke-width="2"/><circle cx="17" cy="18.5" r="2.6" fill="none" stroke="#F5C94A" stroke-width="2"/><line x1="8.3" y1="10.8" x2="14.7" y2="6.7" stroke="#F5C94A" stroke-width="2"/><line x1="8.3" y1="13.2" x2="14.7" y2="17.3" stroke="#F5C94A" stroke-width="2"/></svg>Share</span>
      <span class="action-link"><svg viewBox="0 0 24 24"><path d="M4 6h16v10H9l-5 4z" fill="none" stroke="#F5C94A" stroke-width="2" stroke-linejoin="round"/><line x1="8" y1="10.5" x2="16" y2="10.5" stroke="#F5C94A" stroke-width="2" stroke-linecap="round"/></svg>Comment</span>
    </div>
    <div class="website-pill-center"><span class="sitepill">🌐 linpanelegalservices.in</span></div>
    <div class="socials-row">
      <span class="soc-item"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5.5" fill="none" stroke="#F5C94A" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="#F5C94A" stroke-width="2"/><circle cx="17.2" cy="6.8" r="1.5" fill="#F5C94A"/></svg>linpane_legal_services</span>
      <span class="soc-item"><svg viewBox="0 0 24 24"><path d="M4 4L20 20M20 4L4 20" stroke="#F5C94A" stroke-width="3" stroke-linecap="round"/></svg>@linpanelegal</span>
      <span class="soc-item"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="4.5" fill="none" stroke="#F5C94A" stroke-width="2"/><text x="12" y="16.6" text-anchor="middle" font-family="Anton" font-size="10.5" fill="#F5C94A">in</text></svg>linpanelegalservicess</span>
    </div>
    <div class="disclaimer-line">Law Made Simple &nbsp;|&nbsp; Knowledge Builds Confidence &nbsp;|&nbsp; Together for a Safer Tomorrow</div>
    <svg class="wheat-leaf left" viewBox="0 0 70 110"><g stroke="#E5A91A" stroke-width="2.2" fill="none"><path d="M35 105 Q30 70 38 20"/><path d="M36 80 Q22 72 16 58 M36 80 Q48 72 54 58 M37 60 Q26 52 22 40 M37 60 Q48 52 52 40 M38 40 Q30 32 28 22 M38 40 Q46 32 48 22"/></g></svg>
    <svg class="wheat-leaf right" viewBox="0 0 70 110"><g stroke="#E5A91A" stroke-width="2.2" fill="none"><path d="M35 105 Q30 70 38 20"/><path d="M36 80 Q22 72 16 58 M36 80 Q48 72 54 58 M37 60 Q26 52 22 40 M37 60 Q48 52 52 40"/></g></svg>
  </div>

</div>
</body>
</html>"""

OUT = HERE / "locked_template.html"
OUT.write_text(TEMPLATE, encoding="utf-8")
print(f"OK  Written {OUT}  ({OUT.stat().st_size:,} bytes)")
