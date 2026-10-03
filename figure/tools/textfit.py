#!/usr/bin/env python3
"""Measure ink extents of each text line in the original vs a render (skeleton-only render recommended).
usage: textfit.py RENDER.png   -> table of left/right/top/bottom in both + deltas"""
import sys
from PIL import Image
import numpy as np
ITEMS = [  # key, x0, x1, y0, y1, threshold
 ("hdrA", 36,152,12,31,90,(36,170)), ("A", 6,30,11,30,90,(4,32)),
 ("lg1", 293,432,48,61,90), ("lg2", 293,432,62,72,90),
 ("plink", 180,262,101,114,90), ("pcontr", 440,560,101,114,90),
 ("gut1", 14,168,151,164.5,90), ("gut2", 14,168,165,177,90),
 ("vess", 282,440,151,167,90),
 ("heart1", 540,713,151,163.5,90), ("heart2", 542,712,164.5,174.5,70),
 ("fmt1", 171,328,194,205.5,70), ("fmt2", 171,328,206,218,70),
 ("pex1", 477,644,194,206,70), ("pex2", 477,644,206.5,219,70),
 ("hdrB", 36,316,242,261,90,(36,332)), ("B", 6,30,240,261,90,(4,32)),
 ("ISO", 20,46,268,282,90), ("b2ar", 100,140,266,279.5,90),
 ("ac1", 45,150,327,338,45), ("ac2", 45,150,338.5,348,45),
 ("camp1", 240,321,310,321,90), ("camp2", 240,321,322,333,90),
 ("pka1", 408,508,310,321,90), ("pka2", 408,508,322,333.5,90),
 ("b2sig", 290,465,340,351,90),
 ("adrb1", 248,492,354,365,70), ("adrb2", 248,492,365.5,376,70),
 ("paglyL", 328,367,245,259,90,(332,372)),
 ("sup1", 300,455,281.5,291.5,60), ("sup2", 300,455,292.5,302,60),
 ("serum", 522,705,246,260,90),
 ("part1", 486,600,276,287.5,45), ("part2", 486,600,288,299,45),
 ("foot", 1,420,380,394,60),
 ("leg1", 584,726,372,382,60), ("leg2", 584,725,383.5,393,60),
]
def load(p):
    im = Image.open(p).convert("RGB")
    if im.width != 732: im = im.resize((732, 400), Image.LANCZOS)
    return np.asarray(im).astype(int)
def ext(a, x0, x1, y0, y1, T):
    X0, X1, Y0, Y1 = int(x0), int(np.ceil(x1)), int(y0), int(np.ceil(y1))
    reg = a[Y0:Y1, X0:X1]
    bg = np.percentile(reg, 85, axis=1, keepdims=True)
    d = np.abs(reg - bg).max(axis=2)
    ink = d > T
    cols = np.where(ink.sum(0) >= 1)[0]; rows = np.where(ink.sum(1) >= 2)[0]
    if len(cols) == 0: return None
    return (X0 + cols[0], X0 + cols[-1] + 1, Y0 + rows[0], Y0 + rows[-1] + 1)
o = load("ref/original.jpg"); r = load(sys.argv[1])
import json; OUT = {}
PAD = 14  # render is text-only, so its window can be wider
print(f"{'key':8s} {'orig L..R (w)':>18s} {'rend L..R (w)':>18s}  dL    dR   ratio | orig T..B   rend T..B")
for k, x0, x1, y0, y1, T, *rw in ITEMS:
    rx0, rx1 = rw[0] if rw else (max(0, x0 - PAD), min(732, x1 + PAD))
    eo, er = ext(o, x0, x1, y0, y1, T), ext(r, rx0, rx1, y0, y1, 60)
    if not eo or not er: print(k, eo, er); continue
    wo, wr = eo[1]-eo[0], er[1]-er[0]
    OUT[k] = {"o": [int(v) for v in eo], "r": [int(v) for v in er]}
    print(f"{k:8s} {eo[0]:4d}..{eo[1]:4d} ({wo:3d})   {er[0]:4d}..{er[1]:4d} ({wr:3d})  {er[0]-eo[0]:+4d} {er[1]-eo[1]:+4d}  {wo/wr:5.3f} | {eo[2]:3d}..{eo[3]:3d}   {er[2]:3d}..{er[3]:3d}")

if len(sys.argv) > 2: json.dump(OUT, open(sys.argv[2], "w"), indent=0)
