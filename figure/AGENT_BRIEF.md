# Brief for illustration agents

You are helping recreate a scientific graphical abstract (a 732x400 px JPEG at /home/user/new_test/figure/ref/original.jpg) as a faithful, editable vector SVG.
The whole figure is assembled from /home/user/new_test/figure/main.svg (a skeleton with all text, label boxes, arrows, headers, legend — already done) plus
illustration fragments in /home/user/new_test/figure/parts/<name>.svg that are spliced in at "<!--@include name-->" markers. The SVG viewBox is "0 0 732 400",
i.e. SVG user units == pixel coordinates of the reference image. All coordinates below are in that space.

TOOLS (run from /home/user/new_test/figure; view any PNG with the Read tool):
- python3 tools/zoom.py ref/original.jpg X0 Y0 X1 Y1 SCALE GRID out/<name>-z.png   -> zoomed crop of the ORIGINAL with a labelled grid (reference coords). e.g. SCALE 8 GRID 5.
  (It also works on a render: python3 tools/zoom.py out/part-<name>.png ... )
- python3 tools/pick.py ref/original.jpg x,y x,y ...   -> sampled colours of the original at those points.
- node tools/render.mjs --name part-<name> --scale 6 --only <name> --region X0,Y0,X1,Y1
    -> builds the figure (skeleton + ONLY your part), renders out/part-<name>.png, and writes out/part-<name>-cmp-0.png = ORIGINAL | RENDER | 50% BLEND of that region with grid.
    Use the blend panel to check alignment (misalignment shows as ghosting). You may pass several --region flags (outputs -cmp-0, -cmp-1, ...).

RULES:
- Write ONLY /home/user/new_test/figure/parts/<name>.svg (and scratch files named out/<name>-* or out/part-<name>*). Do NOT edit main.svg, tools/, or other parts.
- The part file is an SVG fragment: exactly one top-level <g id="<name>"> ... </g>, which may contain its own <defs>. No <svg> root, no XML declaration.
  Prefix EVERY id you define with "<name>-" (gradients, filters, clipPaths, symbols) so parts never collide.
- Do not add <text> (all labels already exist in the skeleton) unless the spec says so.
- Pure SVG 1.1 features only (paths, gradients, filters like feGaussianBlur, clipPath, mask, opacity). No external images, no <image>, no embedded rasters, no scripts.
- Style target: the original is a polished, glossy medical/scientific illustration (BioRender / AI-rendered look): smooth gradients, specular highlights,
  soft shading, thin slightly darker outlines, soft drop shadows. Match the SHAPES, PROPORTIONS, COLOURS and EXACT POSITION/SIZE of the original as closely
  as you can — the goal is that the blend panel shows almost no ghosting. Use many small shapes where needed for detail; keep the file under ~80 KB.
- Before drawing, zoom the original at high scale (e.g. SCALE 8-10, GRID 2-5) and study it carefully; sample colours with pick.py.
- Iterate render -> compare -> fix at least 4 times. Check the compare image every time. Stop when further changes would not visibly improve fidelity.
- The figure is rendered in Chromium; test that your part renders (no XML errors: if render fails, fix the markup).


# Part specs


## bowl
compare region: --region 296,0,432,50
BOWL OF HERBAL DECOCTION (Linggui Zhugan Decoction), top centre of panel A, region x 296..432, y 0..48 (the label box at y>=45 is drawn above your part by the skeleton, so you may extend slightly under it).
- A white/light-grey glossy ceramic bowl seen slightly from above: elliptical rim roughly x 312..388, top y≈3, rim thickness visible (light grey inner rim band),
  dark brown decoction liquid inside the rim (deep brown #3d2410 centre to warmer #7a4a22 edges, with a soft sheen), bowl body tapering down to a foot at y≈45
  (approx x 330..372), body shaded white->light grey (#f4f4f4 -> #c9cdd2) with a subtle highlight; soft grey shadow beneath.
- Pile of dried herbal slices (tan/beige #d9b27f, #c79a63, light #ecd3a8 with darker brown edges/spots — like sliced Poria cocos, Atractylodes, Cinnamon twig, Licorice)
  to the right/front of the bowl: irregular flat slices roughly x 357..418, y 17..46, overlapping the lower right of the bowl. One slice lies at the front lower-left (≈x 357..380, y 33..46).
- Note the teal arrows in the skeleton start at (298,34) and (428,34); the bowl/herbs sit between them.


## gut
compare region: --region 14,46,172,150
GUT + MICROBIOTA MAGNIFIER, left of panel A, region x 18..172, y 48..150 (label box below starts at y=148, drawn over you).
- Human intestines in salmon/coral pink, glossy: LARGE INTESTINE (colon) forms a frame — ascending colon on the left (≈x 22..44, from y≈62 down to ≈140),
  transverse colon across the top (≈y 52..82, from x≈25 to ≈120, rising toward the upper right, highest at right ≈y 52), descending colon down the right side
  (≈x 100..118, partly hidden behind the magnifier). The colon is made of rounded bulges (haustra) — draw as rows of overlapping rounded lobes with
  gradient shading (#f6a08f light, #e9716a mid, #c94e4f shadow) and thin darker outlines; a pale longitudinal band (taenia) runs along it.
- SMALL INTESTINE: densely coiled lighter pink loops (#f7b3b8 / #ee8f99 / outline #d2707c) filling ≈x 42..108, y 80..142.
- A thin tube (appendix / rectum) hangs down near x≈42..47 from y≈118 to ≈145.
- MAGNIFIER CIRCLE: centre ≈(133,112), radius ≈34, dark grey outline (#454a55, ~1.6 px), interior very pale lavender/white (#f7f2fc) with soft radial
  gradient. Inside: colourful bacteria — capsule/rod-shaped bacilli (purple #8b5ccf, magenta-pink #e46aa3, cyan #4fc0db, blue #5a8de0, violet), some
  slightly curved, with glossy highlights, plus small round cocci dots (teal #6fc6c6, purple) scattered. ~14 rods and ~15 dots. Study the zoom to place them.
- ZOOM LEADER: thin black dashed lines from a point on the intestine (≈(86,118)) to the left edge of the circle, forming a narrow wedge (study the zoom).
- The teal arrow from the skeleton ends at ≈(147,75) above the circle.


## vessel
compare region: --region 276,84,444,152
BLOOD VESSEL WITH PAGly, centre of panel A, region x 278..440, y 86..152 (label box below starts y=148).
- A horizontal cylindrical blood vessel segment shown in slight perspective. LEFT END: open cut end — an ellipse ≈x 280..300, y 92..143, showing the vessel
  wall thickness (pink/red ring) and the darker red lumen inside. BODY: tube extending right to ≈x 436 where it fades out softly (feathered/soft right edge,
  use a gradient mask). Top edge ≈y 92 at left rising/curving to ≈y 90-95, bottom edge ≈y 143 at left to ≈y 139 at right — check the zoom.
- Colours: wall red/salmon (#e2585d, #ef7f7b, light #f6b1a8 highlight band near the top, darker #c13e46 along the bottom), with faint longitudinal streaks.
  Interior (seen through the translucent wall) lighter pink/peach (#f7b3a5).
- Inside: glossy PURPLE spheres (PAGly) radius ≈3.5-4 (radial gradient light #e2c8ff -> #9a5fd8 -> #6a35a8, small white highlight) at roughly
  (309,112), (321,123), (330,107), (347,118), (353,104)?, (360,120), (372,124), (378,110)?, (393,119)? ... — zoom in and place every sphere exactly;
  plus small pale pink rings/circles (RBC-like, r≈2.5, #f08a8a outline lighter centre) scattered in between.


## heart
compare region: --region 552,40,720,152
ANATOMICAL HEART + MAGNIFIED CARDIAC TISSUE, right of panel A, region x 556..718, y 42..150 (label box below starts y=148).
- Glossy anatomical heart (front view, apex pointing down-right): body ≈x 560..652, y 78..148. Myocardium red/pink (#e8495a, #f07a7f, highlights #fbb0b0,
  shadows #b9243a), with yellow-orange coronary fat and branching coronary vessels (#f2b84b / #e59a2e) running down the front (anterior interventricular sulcus).
  Right atrium/auricle on the left side (pinkish-red). AORTIC ARCH: red, rising at top centre (≈x 590..625, up to y≈46) with 3 branches pointing up.
  PULMONARY TRUNK + branches: BLUE (#3a7fd8, highlight #7fb6f0) — a blue vessel crossing to the right at ≈(610..650, 70..95);
  SUPERIOR VENA CAVA: blue, top-left (≈x 573..592, y 48..100) with a branch; INFERIOR VENA CAVA: blue stub at the bottom-left (≈x 571..578, y 126..148).
  Also red pulmonary veins stub at the right (≈x 643..652, y 80..90). Study the zoom closely for every vessel.
- MAGNIFIER CIRCLE: centre ≈(678,100), radius ≈35, thick dark outline (#2b2b33, ~1.8 px). Interior: pink striated cardiac muscle fibres running diagonally
  (lower-left to upper-right, #f4b6c2 / #e98fa3 with thin darker lines), with 4-5 spindle-shaped BLUE fibroblast cells (#5c96d8 with darker nuclei #2f62a8)
  lying along the fibres.
- LEADER: a small dark red open circle marker on the heart at ≈(627,131) (r≈2.5) and a thin black dashed line from it to the circle edge (≈(651,118)),
  plus a thin solid line from the marker up toward the circle (check the zoom).
- The teal arrow from the skeleton ends at ≈(564,75) at the upper left of the heart.


## mouse_fmt
compare region: --region 78,178,170,226
FMT VIGNETTE, panel A lower left, region x 78..168, y 180..224 (a pale blue sub-panel background is already drawn by the skeleton).
- Small brown POOP pile (stool, glossy brown #8a5a2a / #b07a3c / dark #5a3714, like the emoji) at ≈x 83..100, y 199..213.
- Curved black ARROW (#1d2433, ~1.6px) arcing from just above the poop (≈(97,197)) up and over to the right, ending with an arrowhead pointing down-right at ≈(132,197).
- Dark grey MOUSE (side view, facing right), glossy: body ≈x 112..150, y 197..219, charcoal (#4a4a4f -> #6b6b70, highlight #8c8c92), pink ear (#e7a3ad) at ≈(136,201),
  pink nose at ≈(149,209), small black eye, whiskers optional, pink feet at the bottom, long thin pink-grey tail curling back left to ≈x 101, y 219.
- DROPPER / PIPETTE: diagonal, from upper right (blue rubber bulb ≈(158,184)) down-left to the glass tip near the mouse's head (≈(146,198)); glass shaft light grey/blue.


## mouse_pagly
compare region: --region 386,178,474,226
PAGly EXPOSURE VIGNETTE, panel A lower right-centre, region x 386..472, y 180..224 (a pale blue sub-panel background is already drawn by the skeleton).
- Dark grey MOUSE (side view, facing right), glossy, same style as a lab mouse icon: body ≈x 407..447, y 197..220, charcoal (#4a4a4f -> #6b6b70, highlight #8c8c92),
  pink ear (#e7a3ad) at ≈(434,201), pink nose at ≈(447,208), small black eye, pink feet, long thin pink-grey tail curling back to the left to ≈x 395..400, y 216..220.
- SYRINGE: diagonal from upper right (plunger end ≈(470,183)) down-left to the needle tip near the mouse's face (≈(452,207)); barrel lavender/purple translucent
  (#b9a3ea with #8a6cd0 outline and purple liquid), white/grey plunger and finger flange, thin grey needle.


## membrane
compare region: --region 4,260,720,380
CELL OUTLINE, panel B, region x 6..716, y 262..378. Draw the big elongated cardiomyocyte cell (it sits BEHIND all panel-B text, boxes and the receptor).
- Shape: a long rounded capsule-like outline. TOP edge: from the far left (≈x 10, y≈330) the outline curves up steeply (≈(30,305), (60,297)) then runs
  rightward very gently rising: ≈(100,293), (150,288), (250,276), (350,273), (450,272), (520,268), (600,270), (660,280); RIGHT END rounds at ≈x 712 around
  y≈320-330; BOTTOM edge returns leftward ≈(690,352), (620,362), (500,368), (400,372), (300,374), (240,375) ... and on the LEFT lower side ≈(80,365), (30,350),
  back to (10,330). Zoom on the original and trace the outline exactly — especially the left end (which is a tighter curve, ≈x 8..20 at y≈325-335)
  and the right end (≈x 700..714).
- The membrane is a lipid-bilayer BAND ≈5-6 px wide: lavender (#cbb8f0) with a darker purple outer and inner edge line (#9a85cf, ~0.8 px) and a fine dotted /
  beaded texture between (phospholipid heads; small light dots #e8defc or a fine dash pattern), slightly translucent, with a soft outer glow.
- Interior fill: very light lavender, slightly darker toward the edges (#efe6fd near the membrane -> #f7f2fe centre), use a gradient.
- Note: the receptor (separate part) sits on the top membrane at x≈103..147; the white page background shows outside the cell.


## receptor
compare region: --region 96,274,152,324
β2-ADRENERGIC RECEPTOR (GPCR), panel B, region x 98..150, y 276..322. It is drawn on top of the cell membrane band (membrane top edge passes ≈y 290-298 here).
- Seven vertical glossy BLUE transmembrane helices (capsule/cylinder shapes, ≈5.5 px wide, ≈22-26 px tall) side by side spanning ≈x 105..146, ≈y 287..312,
  with cylindrical shading (gradient #0d6fc4 edge -> #3aa0ec -> #8fd3ff highlight -> #1b7fd0), thin darker blue outline (#0b5aa6) and a soft cyan glow.
- Loops: extracellular loops as blue rounded arches on top connecting adjacent helices (≈y 280-288), intracellular loops as rounded arches/rings below (≈y 311-319).
  N-terminus: a short squiggle at the top-left (≈(103..107, 279..286)). C-terminus: a small curl at the bottom-right (≈(141..146, 313..320)).
- Study the zoom (SCALE 10) very carefully: the arrangement of helices and loops is distinctive.


## tube
compare region: --region 498,234,524,272
BLOOD SERUM TUBE (LGZGD-medicated serum), panel B top right, region x 502..520, y 236..270.
- A small vertical blood-collection tube: ORANGE screw cap on top (≈x 506..518, y 238..246; gradient #f0a04a -> #d46a12 with horizontal ridges and a highlight),
  a clear glass tube below (≈x 507..517, y 246..268) with a rounded bottom at y≈268, containing amber/orange serum (light yellow-orange #f8d29a at top
  -> orange #f0a54e lower, darker #d9822c at the bottom), a white glossy highlight stripe down the left side, thin grey glass outline. Soft shadow.
