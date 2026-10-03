#!/usr/bin/env python3
"""Print colours of the reference image at given points (reference coords).
usage: pick.py IMAGE x,y [x,y ...]   -> hex colour (3x3 median) per point"""
import sys
from PIL import Image
import numpy as np
im = Image.open(sys.argv[1]).convert("RGB")
k = im.width / 732.0
a = np.asarray(im)
for p in sys.argv[2:]:
    x, y = map(float, p.split(","))
    X, Y = round(x * k), round(y * k)
    r = max(1, round(k))
    patch = a[max(0, Y - r):Y + r + 1, max(0, X - r):X + r + 1].reshape(-1, 3)
    c = np.median(patch, axis=0).astype(int)
    print(f"{x:g},{y:g}  #{c[0]:02x}{c[1]:02x}{c[2]:02x}")
