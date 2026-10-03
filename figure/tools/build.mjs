// Assemble main.svg + parts/*.svg + embedded fonts into a standalone SVG.
// usage: node tools/build.mjs [outPath=out/figure.svg] [--nofonts] [--only=part1,part2]
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const args = process.argv.slice(2);
const out = path.resolve(root, args.find(a => !a.startsWith('--')) || 'out/figure.svg');
const noFonts = args.includes('--nofonts');
const onlyArg = args.find(a => a.startsWith('--only='));
const only = onlyArg ? onlyArg.slice(7).split(',') : null;
let svg = fs.readFileSync(path.join(root, 'main.svg'), 'utf8');
svg = svg.replace(/<!--@include ([\w-]+)-->/g, (_, name) => {
  const p = path.join(root, 'parts', name + '.svg');
  if (only && !only.includes(name)) return `<!-- skipped part: ${name} -->`;
  return fs.existsSync(p) ? fs.readFileSync(p, 'utf8').replace(/<\?xml[^>]*>/, '').trim() : `<!-- missing part: ${name} -->`;
});
const css = noFonts ? '' : fs.readFileSync(path.join(root, 'fonts/fonts.css'), 'utf8');
svg = svg.replace('<!--@fonts-->', `<style>${css}</style>`);
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, svg);
console.log('built', path.relative(root, out), svg.length, 'bytes');
