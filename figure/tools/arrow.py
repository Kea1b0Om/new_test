#!/usr/bin/env python3
"""Generate a tapered arrow (shaft + head) as a single SVG path 'd'.
Centre line = Catmull-Rom spline through points; width varies linearly w0 -> w1; head of length L and half-width H at the end
(with a small notch N). Usage (python): from arrow import arrow; arrow(points, w0, w1, L, H, N)"""
import math
def catmull(pts, n=12):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    out.append(pts[-1]); return out
def arrow(pts, w0, w1, L, H, N=1.5, tip=None):
    c = catmull(pts)
    # cumulative length
    s = [0.0]
    for i in range(1, len(c)): s.append(s[-1] + math.dist(c[i], c[i - 1]))
    tot = s[-1]
    left, right = [], []
    for i, p in enumerate(c):
        a, b = c[max(0, i - 1)], c[min(len(c) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        w = (w0 + (w1 - w0) * s[i] / tot) / 2
        left.append((p[0] + nx * w, p[1] + ny * w)); right.append((p[0] - nx * w, p[1] - ny * w))
    end = c[-1]; a = c[-3]
    dx, dy = end[0] - a[0], end[1] - a[1]; d = math.hypot(dx, dy); ux, uy = dx / d, dy / d; nx, ny = -uy, ux
    T = tip or (end[0] + ux * (L - N), end[1] + uy * (L - N))
    if tip:
        ux, uy = T[0] - end[0], T[1] - end[1]; d = math.hypot(ux, uy); ux, uy = ux / d, uy / d; nx, ny = -uy, ux
    base = (T[0] - ux * L, T[1] - uy * L)
    wl = (base[0] + nx * H, base[1] + ny * H); wr = (base[0] - nx * H, base[1] - ny * H)
    f = lambda p: f"{p[0]:.2f} {p[1]:.2f}"
    d = "M" + f(left[0]) + "".join(" L" + f(p) for p in left[1:]) + " L" + f(wl) + " L" + f(T) + " L" + f(wr) + "".join(" L" + f(p) for p in reversed(right)) + " Z"
    return d
if __name__ == "__main__":
    import json, sys
    spec = json.loads(sys.argv[1]); print(arrow(**spec))
