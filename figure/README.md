# LGZGD graphical abstract — editable vector recreation

`ref/original.jpg` is the 732×400 source image. Everything here rebuilds it as an SVG whose
coordinates equal the source image's pixel coordinates (`viewBox="0 0 732 400"`).

## Files

| Path | What it is |
|---|---|
| `dist/` | Final deliverables: `LGZGD_graphical_abstract.svg` (standalone, fonts embedded), `.png` (2928×1600, 4×), `.pdf` (vector, fonts embedded), `comparison.png` (original vs recreation) |
| `main.svg` | Layout skeleton: every text line, label box, header, arrow, dashed connector, legend. Illustrations are spliced in at `<!--@include name-->` markers |
| `parts/*.svg` | One illustration each: `bowl`, `gut`, `vessel`, `heart`, `mouse_fmt`, `mouse_pagly`, `membrane`, `receptor`, `tube` |
| `fonts/fonts.css` | Source Sans 3 (SIL OFL) as base64 `@font-face` rules, embedded into the built SVG |
| `tools/` | Build, render and measurement scripts (below) |

## Editing

- Change wording, colours or positions of text/boxes/arrows in `main.svg`. Text lines carry
  `textLength` so they keep the original's widths; if you change the wording of a line, delete its
  `textLength`/`lengthAdjust` attributes (or re-run the fitter) so the new text is not squeezed.
- Each illustration is a self-contained `<g>` in `parts/` (all ids prefixed with the part name), so
  it can be moved with a `transform`, recoloured, or copied into another figure.

## Building

```sh
node tools/build.mjs dist/figure.svg                 # standalone SVG
node tools/render.mjs --name full --scale 4 --pdf    # out/full.png (2928×1600) + out/full.pdf
node tools/render.mjs --name x --region 0,0,240,230  # also writes out/x-cmp-0.png = original | render | blend
```

Rendering uses Playwright's Chromium. Measurement helpers: `tools/zoom.py` (gridded zoom),
`tools/pick.py` (colour picker), `tools/compare.py` (side-by-side), `tools/align.py` (best sub-pixel
offset of an element), `tools/textfit.py` + `tools/fittext.mjs` (fit text widths to the original),
`tools/arrow.py` (tapered arrow paths).

## Re-exporting `dist/`

```sh
node tools/build.mjs dist/LGZGD_graphical_abstract.svg
node tools/render.mjs --name full --scale 4 --pdf
cp out/full.png dist/LGZGD_graphical_abstract.png && cp out/full.pdf dist/LGZGD_graphical_abstract.pdf
```

For Illustrator / Inkscape editing, open the PDF: those apps ignore fonts embedded via CSS in an SVG
(they substitute a system font), while the PDF carries the embedded Source Sans 3 glyphs.
