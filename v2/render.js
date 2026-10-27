/**
 * render.js  — Playwright renderer for locked BNS infographic template.
 *
 * Usage:
 *   node render.js                          # render all 120 posts (Sec 1–358)
 *   node render.js --resume                 # skip already-rendered posts in output/
 *   node render.js --post post-01           # render single post
 *   node render.js --start 1 --count 10     # render a specific batch
 *
 * Output: ./output/BNS_<file>.jpg (1080x1350 JPEG, high quality)
 */

const { chromium } = require('playwright');
const fs   = require('fs');
const path = require('path');

const DIR     = __dirname;
const TPL     = path.join(DIR, 'locked_template.html');
const DATA    = path.join(DIR, 'bns_posts.json');
const OUT     = path.join(DIR, 'output');
const STATE   = path.join(DIR, 'render_state.json');
const TMP_DIR = path.join(DIR, '.tmp');

// ── CLI Arguments ─────────────────────────────────────────────────────────────
const args    = process.argv.slice(2);
const RESUME  = args.includes('--resume');
const ALL     = args.includes('--all') || (!args.includes('--post') && !args.includes('--count'));
const POST_F  = (() => { const i = args.indexOf('--post'); return i >= 0 ? args[i+1] : null; })();
const START_I = (() => { const i = args.indexOf('--start'); return i >= 0 ? parseInt(args[i+1], 10) : 1; })();
const COUNT_I = (() => { const i = args.indexOf('--count'); return i >= 0 ? parseInt(args[i+1], 10) : null; })();

function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE, 'utf8')); } catch { return { done: [] }; }
}
function saveState(s) { fs.writeFileSync(STATE, JSON.stringify(s, null, 2)); }

function escapeHtml(s) {
  return String(s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function fillTemplate(tpl, post) {
  const cards = post.cards || [];
  const map = {
    SERIES_MARK:    post.series_mark,
    SECTIONS_RANGE: post.sections_range,
    CHAPTER_NUM:    post.chapter_num,
    CHAPTER_NAME:   post.chapter_name,
  };

  for (let i = 0; i < 3; i++) {
    const c = cards[i] || {};
    const idx = i + 1;
    map[`N${idx}`]     = c.n     ?? '';
    map[`S${idx}`]     = c.s     ?? '';
    map[`TITLE${idx}`] = c.title ?? '';
    map[`EASY${idx}`]  = c.easy  ?? '';
    map[`TAKE${idx}`]  = c.takeaway ?? '';
    const subs = (c.subs || []).map(s =>
      `<span class="subchip">${escapeHtml(s)}</span>`
    ).join('');
    map[`SUBS${idx}`] = subs;
  }

  let html = tpl;
  for (const [k, v] of Object.entries(map)) {
    html = html.replaceAll(`{{${k}}}`, v ?? '');
  }
  return html;
}

(async () => {
  fs.mkdirSync(OUT,     { recursive: true });
  fs.mkdirSync(TMP_DIR, { recursive: true });

  const tpl   = fs.readFileSync(TPL, 'utf8');
  const allPosts = JSON.parse(fs.readFileSync(DATA, 'utf8')).posts;
  const st    = loadState();

  // Filter posts
  let posts = allPosts;
  if (POST_F) {
    posts = allPosts.filter(p => p.file === POST_F);
  } else {
    const startIdx = Math.max(0, START_I - 1);
    const count = COUNT_I !== null ? COUNT_I : allPosts.length;
    posts = allPosts.slice(startIdx, startIdx + count);
  }

  console.log(`Starting render run: ${posts.length} post(s) queued (out of ${allPosts.length} total)...\n`);

  const browser = await chromium.launch({
    args: ['--font-render-hinting=none', '--disable-gpu']
  });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1080, height: 1350 });

  let rendered = 0;
  let skipped = 0;

  for (let i = 0; i < posts.length; i++) {
    const post = posts[i];
    const outPath = path.join(OUT, `BNS_${post.file}.jpg`);

    // In resume mode, skip if already exists on disk and in state
    if (RESUME && (fs.existsSync(outPath) || st.done.includes(post.file))) {
      skipped++;
      continue;
    }

    const html    = fillTemplate(tpl, post);
    const tmpFile = path.join(TMP_DIR, `${post.file}.html`);
    fs.writeFileSync(tmpFile, html, 'utf8');

    const fileUri = `file:///${tmpFile.replace(/\\/g, '/')}`;
    await page.goto(fileUri, { waitUntil: 'load', timeout: 30000 });
    await page.waitForTimeout(600);

    const clip = { x: 0, y: 0, width: 1080, height: 1350 };
    await page.screenshot({
      path: outPath,
      type: 'jpeg',
      quality: 94,
      clip,
    });

    const kb = Math.round(fs.statSync(outPath).size / 1024);
    rendered++;
    console.log(`[${i + 1}/${posts.length}] Saved ${path.basename(outPath)} (${kb} KB) — Sections ${post.sections_range}`);

    if (!st.done.includes(post.file)) {
      st.done.push(post.file);
      saveState(st);
    }
  }

  await browser.close();
  console.log(`\nRender completed!`);
  console.log(`Rendered: ${rendered} | Skipped: ${skipped} | Total output files: ${st.done.length}`);
})();
