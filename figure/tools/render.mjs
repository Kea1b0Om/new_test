// Build + render the figure to PNG (and optionally PDF), then make comparison images.
// usage: node tools/render.mjs [--name figure] [--scale 4] [--pdf] [--only part[,part]] [--region x0,y0,x1,y1 ...]
//   out/<name>.svg, out/<name>.png; with --region: out/<name>-cmp-<i>.png = original | render | 50% blend
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : d; };
const name = opt('name', 'figure');
const scale = Number(opt('scale', 4));
const regions = []; argv.forEach((a, i) => { if (a === '--region') regions.push(argv[i + 1]); });
const svgPath = path.join(root, 'out', name + '.svg');
const only = opt('only', null);
execFileSync('node', [path.join(root, 'tools/build.mjs'), svgPath, ...(only ? ['--only=' + only] : [])], { stdio: 'inherit' });
const svg = fs.readFileSync(svgPath, 'utf8');
const textOnly = argv.includes('--textonly') ? 'svg *{visibility:hidden}svg text,svg text *{visibility:visible}' : '';
const html = `<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:#fff}svg{display:block;width:732px;height:400px}${textOnly}</style></head><body>${svg.replace(/<\?xml[^>]*>/, '')}</body></html>`;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: 732, height: 400 }, deviceScaleFactor: scale });
await page.setContent(html, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
const png = path.join(root, 'out', name + '.png');
await page.screenshot({ path: png, clip: { x: 0, y: 0, width: 732, height: 400 } });
console.log('rendered', path.relative(root, png));
if (argv.includes('--pdf')) {
  const pdf = path.join(root, 'out', name + '.pdf');
  await page.pdf({ path: pdf, width: '732px', height: '400px', printBackground: true, pageRanges: '1' });
  console.log('pdf', path.relative(root, pdf));
}
await browser.close();
regions.forEach((r, i) => {
  const outCmp = path.join(root, 'out', `${name}-cmp-${i}.png`);
  execFileSync('python3', [path.join(root, 'tools/compare.py'), path.join(root, 'ref/original.jpg'), png, ...r.split(','), outCmp], { stdio: 'inherit' });
});
