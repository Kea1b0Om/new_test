#!/usr/bin/env python3
"""Crop a region of an image (coords in the 732x400 reference space), upscale it,
and overlay a labelled grid so positions can be read off in reference coordinates.

usage: zoom.py IMAGE x0 y0 x1 y1 [scale=4] [grid=10] OUT.png
IMAGE may be any size; it is resized to 732x400 first if needed (so renders at 4x work too).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

img_path, x0, y0, x1, y1 = sys.argv[1], *map(float, sys.argv[2:6])
rest = sys.argv[6:]
out = rest[-1]
scale = float(rest[0]) if len(rest) > 1 else 4
grid = float(rest[1]) if len(rest) > 2 else 10

im = Image.open(img_path).convert("RGB")
k = im.width / 732.0
crop = im.crop((round(x0 * k), round(y0 * k), round(x1 * k), round(y1 * k)))
W, H = round((x1 - x0) * scale), round((y1 - y0) * scale)
crop = crop.resize((W, H), Image.LANCZOS)
d = ImageDraw.Draw(crop, "RGBA")
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
except Exception:
    font = ImageFont.load_default()
g = grid
import math
gx = math.ceil(x0 / g) * g
while gx <= x1:
    px = (gx - x0) * scale
    major = abs(gx / (g * 5) - round(gx / (g * 5))) < 1e-6
    d.line([(px, 0), (px, H)], fill=(255, 0, 0, 110 if major else 45), width=1)
    if major or (x1 - x0) / g < 30:
        d.text((px + 2, 1), f"{gx:g}", fill=(200, 0, 0, 255), font=font)
    gx += g
gy = math.ceil(y0 / g) * g
while gy <= y1:
    py = (gy - y0) * scale
    major = abs(gy / (g * 5) - round(gy / (g * 5))) < 1e-6
    d.line([(0, py), (W, py)], fill=(0, 0, 255, 110 if major else 45), width=1)
    if major or (y1 - y0) / g < 30:
        d.text((2, py + 1), f"{gy:g}", fill=(0, 0, 200, 255), font=font)
    gy += g
crop.save(out)
print(out, crop.size)
