/**
 * Preview / Batch Renderer for BNS Infographic Template v3 (1080x1350).
 * Usage:
 *   node render_v3.js --posts=post-24,post-01 --out=preview
 * Always preserves existing v2/output/ unless explicitly passed --out=output.
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const { renderCardIllustration } = require('./legal_illustrations');

const HERE = __dirname;
const TPL_PATH = path.join(HERE, 'locked_template_v3.html');
const POSTS_PATH = path.join(HERE, 'bns_posts.json');
const TMP_DIR = path.join(HERE, '.tmp_v3');

const STOP_WORDS = new Set([
  'of', 'the', 'and', 'for', 'by', 'to', 'in', 'on', 'at', 'with', 'or', 'a', 'an', 'etc', 'etc.', 'certain'
]);

function getArg(prefix, fallback = '') {
  const hit = process.argv.find((a) => a.startsWith(prefix));
  return hit ? hit.slice(prefix.length) : fallback;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function cleanCardSubs(card) {
  const raw = Array.isArray(card.subs) ? card.subs : [];
  const kept = [];
  const seen = new Set();

  for (const s of raw) {
    const t = String(s || '').trim();
    const low = t.toLowerCase();
    if (!t || STOP_WORDS.has(low) || seen.has(low)) continue;
    seen.add(low);
    kept.push(t);
  }

  // If noisy source tags left < 3 meaningful chips, derive factual terms strictly from title words.
  if (kept.length < 3 && card.title) {
    const words = String(card.title)
      .replace(/[^a-zA-Z0-9\s-]/g, ' ')
      .split(/\s+/)
      .filter((w) => w.length > 2 && !STOP_WORDS.has(w.toLowerCase()));
    for (const w of words) {
      const cap = w.charAt(0).toUpperCase() + w.slice(1);
      if (!seen.has(cap.toLowerCase())) {
        seen.add(cap.toLowerCase());
        kept.push(cap);
      }
      if (kept.length >= 3) break;
    }
  }
  return kept.slice(0, 3);
}

function fillTemplate(tpl, post) {
  const cards = post.cards || [];
  const map = {
    SERIES_MARK: escapeHtml(post.series_mark),
    SECTIONS_RANGE: escapeHtml(post.sections_range),
    CHAPTER_NUM: escapeHtml(post.chapter_num),
    CHAPTER_NAME: escapeHtml(post.chapter_name),
  };

  for (let i = 0; i < 3; i++) {
    const c = cards[i] || {};
    const idx = i + 1;
    map[`N${idx}`] = escapeHtml(c.n ?? '');
    map[`S${idx}`] = escapeHtml(c.s ?? '');
    map[`TITLE${idx}`] = escapeHtml(c.title ?? '');
    map[`EASY${idx}`] = escapeHtml(c.easy ?? '');
    map[`TAKE${idx}`] = escapeHtml(c.takeaway ?? '');
    map[`SUBS${idx}`] = cleanCardSubs(c)
      .map((s) => `<span class="subchip">${escapeHtml(s)}</span>`)
      .join('');
    map[`ILLUS${idx}`] = renderCardIllustration(c, i, post);
  }

  return tpl.replace(/\{\{([A-Z0-9_]+)\}\}/g, (_, k) =>
    Object.prototype.hasOwnProperty.call(map, k) ? map[k] : ''
  );
}

(async () => {
  const postsArg = getArg('--posts=', '');
  const fromArg = getArg('--from=', '');
  const outArg = getArg('--out=', 'preview');
  const outDir = path.join(HERE, outArg);
  fs.mkdirSync(outDir, { recursive: true });
  fs.mkdirSync(TMP_DIR, { recursive: true });

  const tpl = fs.readFileSync(TPL_PATH, 'utf8');
  const data = JSON.parse(fs.readFileSync(POSTS_PATH, 'utf8'));
  const allPosts = data.posts || [];

  let posts = [];
  if (fromArg) {
    const fromNum = parseInt(fromArg, 10);
    posts = allPosts.filter((p) => {
      const mark = parseInt(p.series_mark || '0', 10);
      return mark >= fromNum;
    });
  } else if (postsArg === 'all') {
    posts = allPosts;
  } else {
    const requested = new Set((postsArg || 'post-24,post-01').split(',').map((s) => s.trim()).filter(Boolean));
    posts = allPosts.filter((p) => requested.has(p.file));
  }

  if (!posts.length) {
    throw new Error(`No matching posts found! (posts=${postsArg}, from=${fromArg})`);
  }

  console.log(`Starting render for ${posts.length} posts into ${outDir}...`);
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1080, height: 1350 },
    deviceScaleFactor: 1,
  });

  for (let i = 0; i < posts.length; i++) {
    const post = posts[i];
    const html = fillTemplate(tpl, post);
    const tmpFile = path.join(TMP_DIR, `${post.file}.html`);
    fs.writeFileSync(tmpFile, html, 'utf8');

    const fileUri = `file:///${tmpFile.replace(/\\/g, '/')}`;
    await page.goto(fileUri, { waitUntil: 'networkidle', timeout: 30000 });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(250);

    const suffix = outArg === 'preview' ? '_v3' : '';
    const outPath = path.join(outDir, `BNS_${post.file}${suffix}.jpg`);
    await page.screenshot({
      path: outPath,
      type: 'jpeg',
      quality: 95,
      clip: { x: 0, y: 0, width: 1080, height: 1350 },
    });

    const kb = Math.round(fs.statSync(outPath).size / 1024);
    console.log(`[${i + 1}/${posts.length}] Rendered ${path.basename(outPath)} (${kb} KB) — Sections ${post.sections_range}`);
  }

  await browser.close();
  console.log(`All ${posts.length} posts rendered successfully!`);
})();
