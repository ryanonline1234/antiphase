#!/usr/bin/env python3
"""Mood-board render for Antiphase.

Runs a small 2D acoustic FDTD (two galleries joined by a doorway), drives a
steady "drill" tone, tunes a second emitter so the two tones cancel at a
guard's ear, and renders the result in the game's intended look.

This is a design tool for docs/01-inspiration.md, written by Claude. It is
NOT game code; nothing in the game depends on it.

Run from the repo root:
  uv run --no-project --with numpy --with pillow python docs/inspiration/render_fringes.py
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- world ------------------------------------------------------------------
DX = 0.1                                  # metres per cell
W, H = 320, 240                           # 32 m x 24 m
C = 34.3                                  # m/s, the game's slowed speed of sound
DT = 0.7 * DX / (C * math.sqrt(2))        # CFL 0.7
LAMBDA = 4.0                              # m, the drill's wavelength in the sim
FREQ = C / LAMBDA
OMEGA = 2 * math.pi * FREQ
MARGIN_DB = 4.5                           # drill level over the guard's threshold

solid = np.ones((H, W), bool)


def carve(x0, y0, x1, y1):
    solid[int(y0 / DX):int(y1 / DX), int(x0 / DX):int(x1 / DX)] = False


carve(2.0, 3.0, 15.0, 21.0)       # west gallery
carve(15.4, 3.0, 30.0, 21.0)      # east gallery (0.4 m wall between)
carve(14.8, 10.0, 15.8, 13.0)     # 3 m doorway
solid[int(16.5 / DX):int(18.5 / DX), int(23 / DX):int(25 / DX)] = True  # a plinth
air = ~solid


def cell(x, y):
    return (int(y / DX), int(x / DX))


DRILL = cell(6.0, 12.0)
EMITTER = cell(19.0, 6.5)
GUARD = cell(24.0, 14.5)
PATROL = (cell(19.5, 14.5), cell(29.0, 14.5))

# damping: strong in a 3-cell band along walls (soft materials), weak in air
near = solid.copy()
for _ in range(3):
    near |= (np.roll(near, 1, 0) | np.roll(near, -1, 0)
             | np.roll(near, 1, 1) | np.roll(near, -1, 1))
damp = np.where(near & air, 0.985, 0.9998).astype(np.float32)
damp[solid] = 0.0
mvx = (~(solid[:, :-1] | solid[:, 1:])).astype(np.float32)   # rigid-wall face masks
mvy = (~(solid[:-1, :] | solid[1:, :])).astype(np.float32)


def run(src, T=6.0, lock_from=4.0):
    """Leapfrog FDTD on a staggered grid. Returns the complex steady field at OMEGA."""
    p = np.zeros((H, W), np.float32)
    vx = np.zeros((H, W - 1), np.float32)
    vy = np.zeros((H - 1, W), np.float32)
    I = np.zeros_like(p)
    Q = np.zeros_like(p)
    div = np.zeros_like(p)
    n = 0
    for k in range(int(T / DT)):
        t = k * DT
        vx -= (DT / DX) * (p[:, 1:] - p[:, :-1]); vx *= mvx
        vy -= (DT / DX) * (p[1:, :] - p[:-1, :]); vy *= mvy
        div[:] = 0
        div[:, :-1] += vx; div[:, 1:] -= vx
        div[:-1, :] += vy; div[1:, :] -= vy
        p -= (C * C * DT / DX) * div
        ramp = 0.5 - 0.5 * math.cos(math.pi * min(1.0, t / 0.3))
        p[src] += 0.05 * ramp * math.sin(OMEGA * t)
        p *= damp
        if t >= lock_from:
            I += p * math.cos(OMEGA * t); Q += p * math.sin(OMEGA * t); n += 1
    return (2.0 / n) * (I - 1j * Q)


print(f"grid {W}x{H} @ {DX} m, dt={DT*1e3:.3f} ms ({1/DT:.0f} steps/s), lambda={LAMBDA} m, f_sim={FREQ:.2f} Hz")
Gd = run(DRILL)
Ge = run(EMITTER)
coeff = -Gd[GUARD] / Ge[GUARD]                       # exact null at the guard's ear
gain = abs(coeff)
phase = math.degrees(math.atan2(coeff.imag, coeff.real)) % 360
thr = abs(Gd[GUARD]) * 10 ** (-MARGIN_DB / 20)


def field(phi_deg, g=gain):
    return Gd + g * np.exp(1j * math.radians(phi_deg)) * Ge


F_after = field(phase)

# ---- measurements (crude preview of the days-1-2 kill test) -----------------
def run_len(A, c0, axis):
    i, j = c0
    if A[i, j] >= thr:
        return 0.0
    lo = hi = (j if axis == 1 else i)
    def ok(k):
        ii, jj = (i, k) if axis == 1 else (k, j)
        return 0 <= k < (W if axis == 1 else H) and air[ii, jj] and A[ii, jj] < thr
    while ok(lo - 1): lo -= 1
    while ok(hi + 1): hi += 1
    return (hi - lo + 1) * DX


A_after = np.abs(F_after)
east = air.copy(); east[:, :int(15.4 / DX)] = False
row = GUARD[0]; j0, j1 = PATROL[0][1], PATROL[1][1]
patrol_cov = np.mean(A_after[row, j0:j1 + 1] < thr)
centres = []
for phi in range(0, 360, 5):
    Aphi = np.abs(field(phi))[row, j0:j1 + 1]
    centres.append((j0 + int(np.argmin(Aphi))) * DX)
print(f"emitter gain needed: {gain:.2f}x drill, phase {phase:.0f} deg; guard ear {20*math.log10(A_after[GUARD]/thr+1e-9):.1f} dB vs threshold")
print(f"silence band at guard: {run_len(A_after, GUARD, 1):.1f} m along patrol, {run_len(A_after, GUARD, 0):.1f} m across (free-field estimate 0.16*lambda = {0.16*LAMBDA:.2f} m)")
print(f"patrol line below threshold: {patrol_cov*100:.0f}% of {(j1-j0+1)*DX:.1f} m")
print(f"phase wheel slides the band centre along the patrol between x={min(centres):.1f} m and x={max(centres):.1f} m")
print(f"east gallery below threshold: drill only {np.mean(np.abs(Gd)[east] < thr)*100:.0f}%, tuned {np.mean(A_after[east] < thr)*100:.0f}% (if this is near 100%, cancellation is global = trivial)")

# ---- rendering --------------------------------------------------------------
BG = np.array([10, 11, 16], np.float32)
RED = np.array([255, 74, 60], np.float32)
BLUE = np.array([60, 124, 255], np.float32)
LINE = (230, 232, 240)
CONTOUR = (200, 205, 220)
ORANGE = (255, 150, 40)
NORM = float(np.percentile(np.abs(Gd)[air], 92))


def font(px):
    try:
        return ImageFont.load_default(size=int(px))
    except TypeError:                      # Pillow < 10.1
        return ImageFont.load_default()


def render(F, t, scale=4, title=None):
    A = np.abs(F)
    p = (F * np.exp(1j * OMEGA * t)).real
    inten = np.tanh(np.abs(p) / NORM * 1.4)
    col = np.where((p > 0)[..., None], RED, BLUE)
    img = BG + (col - BG) * inten[..., None] * 0.95
    img[solid] = BG * 0.75
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((W * scale, H * scale), Image.BICUBIC)
    glow = np.asarray(im.filter(ImageFilter.GaussianBlur(radius=3 * scale)), np.float32)
    arr = np.asarray(im, np.float32) + 0.55 * (glow - BG)
    # silence: black where the steady amplitude is under the guard's threshold
    Ahi = np.asarray(Image.fromarray(A.astype(np.float32), mode="F").resize(im.size, Image.BICUBIC))
    airimg = Image.fromarray((air * 255).astype(np.uint8)).resize(im.size, Image.NEAREST)
    airhi = np.asarray(airimg) > 0
    sil = (Ahi < thr) & airhi
    arr[sil] *= 0.10
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    # line art: wall outlines, then the silence contour (kept off the walls)
    edges = airimg.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
    im.paste(Image.new("RGB", im.size, LINE), mask=edges)
    inner = np.asarray(airimg.filter(ImageFilter.MinFilter(7))) > 0
    cont = Image.fromarray(((sil & inner) * 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
    cont = Image.fromarray((np.asarray(cont) * inner).astype(np.uint8))
    im.paste(Image.new("RGB", im.size, CONTOUR), mask=cont)

    draw = ImageDraw.Draw(im, "RGBA")
    P = lambda c: ((c[1] + 0.5) * scale, (c[0] + 0.5) * scale)
    lw = max(1, scale // 2)
    a, b = PATROL
    draw.line([P(a), P(b)], fill=LINE + (70,), width=lw)
    gx, gy = P(GUARD); r = 2.2 * scale
    draw.polygon([(gx, gy), (gx - 9 * scale, gy - 5 * scale), (gx - 9 * scale, gy + 5 * scale)], fill=LINE + (22,))
    ring = ORANGE if A[GUARD] >= thr else (70, 72, 84)
    draw.ellipse([gx - 2.6 * r, gy - 2.6 * r, gx + 2.6 * r, gy + 2.6 * r], outline=ring + (255,), width=max(2, scale))
    draw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(225, 226, 235, 255))
    dx_, dy_ = P(DRILL); s = 1.6 * scale
    draw.rectangle([dx_ - s, dy_ - s, dx_ + s, dy_ + s], outline=(255, 120, 110, 255), width=lw)
    ex, ey = P(EMITTER)
    draw.polygon([(ex, ey - 2 * scale), (ex + 2 * scale, ey + 1.5 * scale), (ex - 2 * scale, ey + 1.5 * scale)], outline=(120, 170, 255, 255), width=lw)
    f = font(max(10, 4.5 * scale))
    draw.text((dx_ + 3 * scale, dy_ - 2 * scale), "DRILL", fill=(255, 150, 140, 230), font=f)
    draw.text((ex + 3 * scale, ey - 2 * scale), "EMITTER", fill=(150, 190, 255, 230), font=f)
    draw.text((gx + 3.5 * scale, gy - 6 * scale), "GUARD", fill=(225, 226, 235, 230), font=f)
    if title:
        draw.text((3 * scale, 1.2 * scale), title, fill=(200, 205, 220, 255), font=font(max(10, 4 * scale)))
    return im


render(Gd, 0.0, title="ANTIPHASE  |  drill on, emitter off: the guard hears it").save(os.path.join(OUT, "before.png"))
render(F_after, 0.0, title=f"ANTIPHASE  |  emitter at {gain:.2f}x, phase {phase:.0f} deg: a band of silence rides on the guard").save(os.path.join(OUT, "after.png"))

frames = []
NF = 48
for k in range(NF):
    phi = (phase + 360 * k / NF) % 360
    im = render(field(phi), k / (6 * FREQ), scale=2, title=f"phase wheel {phi:5.1f} deg")
    frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=128))
frames[0].save(os.path.join(OUT, "phase-sweep.gif"), save_all=True, append_images=frames[1:], duration=70, loop=0)
for name in ("before.png", "after.png", "phase-sweep.gif"):
    print(f"wrote {name}: {os.path.getsize(os.path.join(OUT, name))/1e6:.2f} MB")
