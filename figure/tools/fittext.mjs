// Fit each tagged <text data-k> in main.svg so its ink extents match the original.
// Needs out/textfit.json (from textfit.py on a --textonly render of the CURRENT main.svg). Rewrites x / textLength in main.svg.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const skip = new Set((process.argv[2] || 'A,B,b2ar,ISO').split(','));
const fit = JSON.parse(fs.readFileSync(path.join(root, 'out/textfit.json'), 'utf8'));
import { execFileSync } from 'node:child_process';
execFileSync('node', [path.join(root, 'tools/build.mjs'), path.join(root, 'out/fit.svg'), '--only=none']);
const svg = fs.readFileSync(path.join(root, 'out/fit.svg'), 'utf8');
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport: { width: 732, height: 400 } });
await page.setContent(`<!doctype html><body style="margin:0">${svg}</body>`);
await page.evaluate(() => document.fonts.ready);
const info = await page.evaluate(() => Object.fromEntries([...document.querySelectorAll('text[data-k]')].map(t => [t.dataset.k, {
  x: parseFloat(t.getAttribute('x')), anchor: t.getAttribute('text-anchor') || 'start',
  len: t.getAttribute('textLength') ? parseFloat(t.getAttribute('textLength')) : t.getComputedTextLength() }])));
await browser.close();
let main = fs.readFileSync(path.join(root, 'main.svg'), 'utf8');
for (const [k, m] of Object.entries(fit)) {
  if (skip.has(k) || !info[k]) continue;
  const [Lo, Ro] = m.o, [Lr, Rr] = m.r, t = info[k];
  const ratio = (Ro - Lo) / (Rr - Lr);
  const len = +(t.len * ratio).toFixed(2);
  let x;
  if (t.anchor === 'middle') x = (Lo + Ro) / 2 - ((Lr + Rr) / 2 - t.x) * ratio;
  else x = Lo - (Lr - t.x) * ratio;
  x = +x.toFixed(2);
  const re = new RegExp(`<text data-k="${k}"([^>]*)>`);
  main = main.replace(re, (_, attrs) => {
    attrs = attrs.replace(/ x="[^"]*"/, ` x="${x}"`).replace(/ textLength="[^"]*"/, '').replace(/ lengthAdjust="[^"]*"/, '');
    return `<text data-k="${k}"${attrs} textLength="${len}" lengthAdjust="spacingAndGlyphs">`;
  });
  console.log(k.padEnd(8), 'ratio', ratio.toFixed(3), 'x', t.x, '->', x, 'len', t.len.toFixed(1), '->', len);
}
fs.writeFileSync(path.join(root, 'main.svg'), main);
