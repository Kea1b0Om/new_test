#!/usr/bin/env python3
"""Side-by-side comparison of a region: original | render | 50% blend, with a light grid.
usage: compare.py ORIGINAL RENDER x0 y0 x1 y1 OUT.png   (coords in 732x400 space)"""
import sys, math
from PIL import Image, ImageDraw, ImageFont
orig, rend = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(float, sys.argv[3:7]); out = sys.argv[7]
w, h = x1 - x0, y1 - y0
scale = max(1.0, min(8.0, 620.0 / w, 700.0 / h))
W, H = round(w * scale), round(h * scale)
def crop(p):
    im = Image.open(p).convert("RGB"); k = im.width / 732.0
    return im.crop((round(x0*k), round(y0*k), round(x1*k), round(y1*k))).resize((W, H), Image.LANCZOS)
a, b = crop(orig), crop(rend)
c = Image.blend(a, b, 0.5)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
def grid(im):
    d = ImageDraw.Draw(im, "RGBA"); g = 10 if w <= 200 else 20
    gx = math.ceil(x0/g)*g
    while gx <= x1:
        px = (gx-x0)*scale; d.line([(px,0),(px,H)], fill=(255,0,0,50)); d.text((px+2,1), f"{gx:g}", fill=(200,0,0,255), font=font); gx += g
    gy = math.ceil(y0/g)*g
    while gy <= y1:
        py = (gy-y0)*scale; d.line([(0,py),(W,py)], fill=(0,0,255,50)); d.text((2,py+1), f"{gy:g}", fill=(0,0,200,255), font=font); gy += g
    return im
pad = 8
if W > H * 1.6:  # wide region: stack vertically
    canvas = Image.new("RGB", (W, H*3 + pad*2), "white")
    for i, im in enumerate((a, b, c)): canvas.paste(grid(im), (0, i*(H+pad)))
else:
    canvas = Image.new("RGB", (W*3 + pad*2, H), "white")
    for i, im in enumerate((a, b, c)): canvas.paste(grid(im), (i*(W+pad), 0))
canvas.save(out); print("compare", out, canvas.size, "(original | render | blend)")
