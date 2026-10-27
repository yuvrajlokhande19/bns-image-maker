"""
gen_posts.py  — Generate bns_posts.json from data/bns_sections.json for all 358 sections.

Usage:
  python gen_posts.py                    # generate all 120 posts (Sec 1–358)
  python gen_posts.py --start 1 --count 10 # generate first 10 posts
"""
import json, argparse, re
from pathlib import Path

HERE  = Path(__file__).parent
DATA  = HERE.parent / "data" / "bns_sections.json"
OUT   = HERE / "bns_posts.json"

def roman_series(n: int) -> str:
    return f"{n:02d}"

def infer_subs(sec: dict) -> list[str]:
    """Generate or retrieve sub-chip tags."""
    if "subs" in sec and sec["subs"]:
        return sec["subs"][:3]
    title = sec.get("title", "")
    easy  = sec.get("easy", "")
    subs  = []
    m = re.search(r"(\d+)\s+(?:defined terms?|definitions?|clauses?|explanations?|sub-sections?)", easy, re.I)
    if m:
        subs.append(f"{m.group(1)} {m.group(0).split(m.group(1))[1].strip().split('.')[0].strip()}")
    cm = re.search(r"[Cc]lauses?\s+[\w()\-–]+", easy)
    if cm:
        subs.append(cm.group(0).replace("clause", "Clause").replace("clauses", "Clauses"))
    if not subs:
        words = title.split()
        if len(words) >= 2:
            subs.append(" ".join(words[:2]))
        if len(words) >= 4:
            subs.append(" ".join(words[2:4]))
    return subs[:3]

def make_posts(sections: list, start: int, end: int) -> list:
    by_n = {s["n"]: s for s in sections}
    posts = []
    batch_idx = (start - 1) // 3 + 1
    n = start

    while n <= end:
        if n + 2 <= end:
            trio = [by_n.get(n), by_n.get(n+1), by_n.get(n+2)]
            range_str = f"{n}–{n+2}"
            step = 3
        elif n + 1 <= end:
            trio = [by_n.get(n), by_n.get(n+1)]
            range_str = f"{n}–{n+1}"
            step = 2
        else:
            trio = [by_n.get(n)]
            range_str = f"{n}"
            step = 1

        if None in trio:
            n += 1
            continue

        chaps  = [s["chapter_short"] for s in trio]
        topics = [s["chapter_topic"] for s in trio]
        if len(set(chaps)) == 1:
            ch_num  = chaps[0]
            ch_name = topics[0]
        else:
            ch_num  = f"{chaps[0]}–{chaps[-1]}"
            ch_name = topics[0]

        if len(trio) == 3:
            cards = []
            for s in trio:
                cards.append({
                    "n":        f"{s['n']:02d}",
                    "s":        str(s['n']),
                    "title":    s["title"],
                    "easy":     s["easy"],
                    "takeaway": s["takeaway"],
                    "subs":     infer_subs(s),
                })
        else:
            # Final post with Section 358 + BNS Summary
            cards = [
                {
                    "n":        f"{trio[0]['n']:02d}",
                    "s":        str(trio[0]['n']),
                    "title":    trio[0]["title"],
                    "easy":     trio[0]["easy"],
                    "takeaway": trio[0]["takeaway"],
                    "subs":     infer_subs(trio[0]),
                },
                {
                    "n":        "✦",
                    "s":        "BNS",
                    "title":    "BNS, 2023 Overview & Architecture",
                    "easy":     "Bharatiya Nyaya Sanhita, 2023 comprises 20 Chapters and 358 Sections, modernizing Indian criminal justice with community service, electronic records, and victim-centric protections.",
                    "takeaway": "Complete modern criminal code replacing the 163-year-old IPC 1860.",
                    "subs":     ["20 Chapters", "358 Sections", "Modern Justice"]
                },
                {
                    "n":        "★",
                    "s":        "Summary",
                    "title":    "Citizen Legal Awareness & Rights",
                    "easy":     "Understanding the BNS empowers every citizen to know their rights, legal duties, and protections under Indian law for a safer and more confident tomorrow.",
                    "takeaway": "Knowledge builds confidence — Know the law, protect your rights.",
                    "subs":     ["Citizen Rights", "Legal Awareness", "Safer Tomorrow"]
                }
            ]

        posts.append({
            "file":           f"post-{batch_idx:02d}",
            "series_mark":    roman_series(batch_idx),
            "sections_range": range_str,
            "chapter_num":    ch_num,
            "chapter_name":   ch_name,
            "cards":          cards,
        })
        batch_idx += 1
        n += step

    return posts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start",  type=int, default=1,   help="First section number (default 1)")
    ap.add_argument("--end",    type=int, default=358, help="Last section number (default 358)")
    ap.add_argument("--count",  type=int, default=None,help="Number of batches to generate")
    args = ap.parse_args()

    sections = json.loads(DATA.read_text(encoding="utf-8"))
    end = args.end
    if args.count is not None:
        end = min(args.start + args.count * 3 - 1, args.end)

    posts = make_posts(sections, args.start, end)
    payload = {"posts": posts}
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK Generated {len(posts)} post(s) -> {OUT}")

if __name__ == "__main__":
    main()
