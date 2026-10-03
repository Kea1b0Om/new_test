#!/usr/bin/env python3
"""Find the (dx,dy) shift of the render that best matches the original in each region (reference px, 0.25 px steps).
usage: align.py RENDER.png name:x0,y0,x1,y1 ...   (positive dx => render content should move RIGHT by dx)"""
import sys
from PIL import Image
import numpy as np
from scipy.ndimage import shift as nd_shift
o = np.asarray(Image.open("ref/original.jpg").convert("L")).astype(float)
R = Image.open(sys.argv[1]).convert("L"); S = R.width / 732
r4 = np.asarray(R).astype(float)
for spec in sys.argv[2:]:
    name, box = spec.split(":"); x0, y0, x1, y1 = map(int, box.split(","))
    tgt = o[y0:y1, x0:x1]
    best = None
    for dy in np.arange(-2, 2.01, 0.25):
        for dx in np.arange(-2, 2.01, 0.25):
            # render content moved by (dx,dy): sample render at (x-dx, y-dy)
            X0, Y0 = int(round((x0 - dx) * S)), int(round((y0 - dy) * S))
            crop = Image.fromarray(r4[Y0:Y0 + (y1 - y0) * int(S), X0:X0 + (x1 - x0) * int(S)].astype(np.uint8)).resize((x1 - x0, y1 - y0), Image.BOX)
            e = np.abs(np.asarray(crop).astype(float) - tgt).mean()
            if best is None or e < best[0]: best = (e, dx, dy)
    X0, Y0 = int(x0 * S), int(y0 * S)
    e0 = np.abs(np.asarray(Image.fromarray(r4[Y0:Y0 + (y1 - y0) * int(S), X0:X0 + (x1 - x0) * int(S)].astype(np.uint8)).resize((x1 - x0, y1 - y0), Image.BOX)).astype(float) - tgt).mean()
    print(f"{name:12s} err@0 {e0:5.2f}  best dx={best[1]:+.2f} dy={best[2]:+.2f} err {best[0]:5.2f}")
