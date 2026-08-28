#!/usr/bin/env python3
"""Archway wallpaper generator for Omarchy.

Every colour below is an Archway design-system token value. Nothing is
invented: Ink = surfaces, Signal = the one accent, Slate = text,
status quartet = semantic. Geometry is the Archway mark and the product
canvas (dot grid, nodes, journeys, traces).
"""
import math, os, sys

W, H = 5120, 2880
OUT = os.path.dirname(os.path.abspath(__file__))

# ── Archway tokens ────────────────────────────────────────────────
INK_975 = "#07090d"; INK_950 = "#0b0e14"; INK_900 = "#0f1319"
INK_800 = "#161c26"; INK_700 = "#283044"; INK_600 = "#454d5f"; INK_500 = "#6a7488"
SIG_300 = "#8ba0f9"; SIG_400 = "#6b8afd"; SIG_500 = "#4a6bdc"
SIG_600 = "#3b5bdb"; SIG_800 = "#24378c"
SLATE_50 = "#fafbfc"; SLATE_300 = "#e0e5ec"; SLATE_400 = "#b9c3d4"; SLATE_500 = "#8d98ab"
OK = "#4fb39a"; WARN = "#e2b14a"; CRIT = "#c86b6b"; INFO = "#7aa0c4"
PLUM = "#b07ed9"; TEAL = "#4aa39d"; CODE = "#d97757"

# Archway mark, viewBox 0 0 72 72 (arch + centre dot + plumb dashes)
MARK_ARCH = ("M62,65.2c-1.2,0-2.2-1-2.2-2.2v-28c0-13.1-10.7-23.8-23.8-23.8s-23.8,10.7-23.8,23.8v28"
             "c0,1.2-1,2.2-2.2,2.2s-2.2-1-2.2-2.2v-28c0-15.6,12.7-28.2,28.2-28.2s28.2,12.7,28.2,28.2v28"
             "c0,1.2-1,2.2-2.2,2.2Z")
MARK_PLUMB = ("M36.8,60h-1.5v-2h1.5v2ZM36.8,55h-1.5v-2h1.5v2ZM36.8,50h-1.5v-2h1.5v2ZM36.8,45h-1.5v-2h1.5v2Z")

# Lowercase "archway" wordmark, viewBox 0 0 160 44, glyphs start x≈45
WORD = [
 "M49.6,18c1-1.3,2.7-1.9,5.1-1.9s3,.3,4.2.9c1.2.6,1.8,1.8,1.8,3.5v6.6c0,.5,0,1,0,1.7,0,.5.1.8.2,1s.3.3.6.4v.6h-4.1c-.1-.3-.2-.6-.2-.8,0-.3,0-.5-.1-.9-.5.6-1.1,1-1.8,1.4-.8.5-1.7.7-2.7.7s-2.4-.4-3.2-1.1c-.8-.7-1.3-1.8-1.3-3.2s.7-3,2-3.8c.7-.4,1.8-.7,3.3-.9l1.3-.2c.7,0,1.2-.2,1.5-.3.5-.2.8-.6.8-1.1s-.2-1-.6-1.2c-.4-.2-1-.3-1.8-.3s-1.5.2-1.9.7c-.3.3-.4.8-.5,1.3h-3.6c0-1.3.4-2.3,1.1-3.1ZM52.4,28.1c.4.3.8.4,1.3.4.8,0,1.6-.2,2.2-.7.7-.5,1-1.3,1.1-2.6v-1.4c-.2.2-.5.3-.7.4-.2,0-.6.2-1,.3l-.8.2c-.8.1-1.4.3-1.7.5-.6.3-.9.9-.9,1.6s.2,1.1.5,1.4Z",
 "M70.6,19.9c-1.5,0-2.5.5-3,1.5-.3.6-.4,1.4-.4,2.6v6.9h-3.8v-14.4h3.6v2.5c.6-1,1.1-1.6,1.5-2,.7-.6,1.6-.9,2.7-.9s.1,0,.2,0,.2,0,.3,0v3.9c-.2,0-.4,0-.6,0-.2,0-.3,0-.4,0Z",
 "M85.7,21.6h-3.9c0-.5-.3-1-.5-1.5-.4-.6-1.1-.9-2-.9-1.3,0-2.1.6-2.6,1.9-.2.7-.4,1.6-.4,2.7s.1,1.9.4,2.5c.4,1.2,1.3,1.8,2.5,1.8s1.5-.2,1.9-.7c.4-.5.6-1.1.7-1.8h3.8c0,1.1-.5,2.2-1.2,3.2-1.2,1.6-2.9,2.5-5.2,2.5s-4-.7-5.1-2.1c-1.1-1.4-1.6-3.2-1.6-5.3s.6-4.4,1.7-5.8c1.2-1.4,2.8-2.1,4.8-2.1s3.2.4,4.3,1.2c1.1.8,1.8,2.2,2,4.2Z",
 "M100.6,22.3v8.4h-3.8v-8.7c0-.8-.1-1.4-.4-1.9-.3-.7-1-1-2-1s-1.7.3-2.3,1-.8,1.6-.8,2.8v7.8h-3.7V11.4h3.7v6.9c.5-.8,1.2-1.4,1.9-1.7.7-.3,1.5-.5,2.3-.5s1.7.2,2.4.5c.7.3,1.3.8,1.8,1.4.4.5.6,1.1.7,1.7s.1,1.5.1,2.8Z",
 "M114.3,30.8l-2.3-10.5-2.3,10.5h-3.9l-4-14.4h4l2.2,10.3,2.1-10.3h3.8l2.2,10.4,2.2-10.4h3.9l-4.2,14.4h-3.9Z",
 "M124.3,18c1-1.3,2.7-1.9,5.1-1.9s3,.3,4.2.9,1.8,1.8,1.8,3.5v6.6c0,.5,0,1,0,1.7,0,.5.1.8.2,1,.1.2.3.3.6.4v.6h-4.1c-.1-.3-.2-.6-.2-.8,0-.3,0-.5-.1-.9-.5.6-1.1,1-1.8,1.4-.8.5-1.7.7-2.7.7s-2.4-.4-3.2-1.1-1.3-1.8-1.3-3.2.7-3,2-3.8c.7-.4,1.8-.7,3.3-.9l1.3-.2c.7,0,1.2-.2,1.5-.3.5-.2.8-.6.8-1.1s-.2-1-.6-1.2c-.4-.2-1-.3-1.8-.3s-1.5.2-1.9.7c-.3.3-.4.8-.5,1.3h-3.6c0-1.3.4-2.3,1.1-3.1ZM127.1,28.1c.4.3.8.4,1.3.4.8,0,1.6-.2,2.2-.7.7-.5,1-1.3,1.1-2.6v-1.4c-.2.2-.5.3-.7.4-.2,0-.6.2-1,.3l-.8.2c-.8.1-1.4.3-1.7.5-.6.3-.9.9-.9,1.6s.2,1.1.5,1.4Z",
 "M144,27l3-10.6h4l-4.9,14.1c-.9,2.7-1.7,4.4-2.3,5.1-.6.7-1.7,1-3.3,1s-.6,0-.8,0c-.2,0-.5,0-.9,0v-3h.5c.4,0,.7,0,1.1,0,.3,0,.6-.1.8-.3.2-.1.4-.5.6-.9.2-.5.3-.8.2-.9l-5.3-15h4.2l3.1,10.6Z",
]
# Lockup mark (no centre dot), viewBox 0 0 160 44
LOCK_ARCH = "M37.4,38.7c-.7,0-1.3-.6-1.3-1.3v-16c0-7.5-6.1-13.6-13.6-13.6s-13.6,6.1-13.6,13.6v16c0,.7-.6,1.3-1.3,1.3s-1.3-.6-1.3-1.3v-16c0-8.9,7.2-16.1,16.1-16.1s16.1,7.2,16.1,16.1v16c0,.7-.6,1.3-1.3,1.3Z"
LOCK_PLUMB = "M23,35.7h-.9v-1.1h.9v1.1ZM23,32.8h-.9v-1.1h.9v1.1ZM23,30h-.9v-1.1h.9v1.1ZM23,27.1h-.9v-1.1h.9v1.1Z"


def mark(x, y, size, fill, opacity=1.0, dot=True, plumb=True, arch=True):
    """Archway mark scaled from its 72u viewBox, top-left at (x, y)."""
    s = size / 72.0
    p = [f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.5f})" fill="{fill}" opacity="{opacity}">']
    if arch:
        p.append(f'<path d="{MARK_ARCH}"/>')
    if dot:
        p.append('<circle cx="36" cy="37" r="4"/>')
    if plumb:
        p.append(f'<path d="{MARK_PLUMB}"/>')
    p.append('</g>')
    return "".join(p)


def mark_geo(x, y, size):
    """The mark's real measurements, read off the shipped path rather than
       guessed, so anything drawn around it stays true to the logo.

       In the 72u viewBox: springing centre (36, 35); radii 23.8 inner,
       26.0 centreline, 28.2 outer; legs run to y=65.2, i.e. 1.162 x the
       centreline radius; the dot is r=4 at y=37 (0.154 x R)."""
    s = size / 72.0
    return {"cx": x + 36*s, "cy": y + 35*s,
            "r_in": 23.8*s, "r_mid": 26.0*s, "r_out": 28.2*s,
            "foot": y + 65.2*s, "dot_y": y + 37*s, "dot_r": 4*s, "s": s}


def lockup(x, y, width, fill_word, fill_mark, opacity=1.0):
    """Archway horizontal lockup from its 160x44 viewBox, top-left at (x, y)."""
    s = width / 160.0
    g = [f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.5f})" opacity="{opacity}">']
    g.append(f'<g fill="{fill_word}">' + "".join(f'<path d="{d}"/>' for d in WORD) + '</g>')
    g.append(f'<g fill="{fill_mark}"><path d="{LOCK_ARCH}"/><circle cx="22.4" cy="21.4" r="2.3"/>'
             f'<path d="{LOCK_PLUMB}"/></g>')
    g.append('</g>')
    return "".join(g)


def dotgrid(step, r, color, opacity, w=W, h=H, ox=0, oy=0):
    """The product canvas dot grid, emitted as a tiled <pattern>."""
    return (f'<pattern id="dg{step}" x="{ox}" y="{oy}" width="{step}" height="{step}" '
            f'patternUnits="userSpaceOnUse">'
            f'<circle cx="{step/2}" cy="{step/2}" r="{r}" fill="{color}" opacity="{opacity}"/>'
            f'</pattern>')


def head(defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}"><defs>{defs}</defs>')


def glow(idx, color, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{color}" stop-opacity="{a}"/>' for o, a in stops)
    return f'<radialGradient id="{idx}">{s}</radialGradient>'


def write(name, body):
    path = os.path.join(OUT, name + ".svg")
    open(path, "w").write(body + "</svg>")
    print(name, "->", path)


# ══════════════════════════════════════════════════════════════════
# 0 · THE ARCH — the mark, at scale, on the canvas
# ══════════════════════════════════════════════════════════════════
def w_arch():
    d = [dotgrid(80, 2.0, INK_600, 0.30),
         glow("gA", SIG_400, [(0, 0.20), (0.45, 0.06), (1, 0)]),
         glow("gB", SIG_600, [(0, 0.14), (1, 0)]),
         f'<linearGradient id="bedA" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{INK_950}"/><stop offset="0.62" stop-color="{INK_950}"/>'
         f'<stop offset="1" stop-color="{INK_975}"/></linearGradient>']
    s = head("".join(d))
    s += f'<rect width="{W}" height="{H}" fill="url(#bedA)"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#dg80)"/>'
    s += f'<ellipse cx="{W/2}" cy="{H*0.46}" rx="{W*0.42}" ry="{H*0.52}" fill="url(#gA)"/>'
    # horizon rule the arch stands on
    s += (f'<line x1="{W*0.14}" y1="{H*0.795}" x2="{W*0.86}" y2="{H*0.795}" '
          f'stroke="{INK_700}" stroke-width="2"/>')
    size = 1560
    mx, my = W/2 - size/2, H*0.795 - size*0.905
    s += f'<ellipse cx="{W/2}" cy="{my + size*0.48}" rx="{size*0.85}" ry="{size*0.85}" fill="url(#gB)"/>'
    s += mark(mx, my, size, SIG_400)
    # echoes: the same structure receding, drawn as construction hairlines
    base = H*0.795
    for k, (rr, op, wdt) in enumerate(((1.34, 0.55, 4), (1.78, 0.34, 3), (2.30, 0.20, 3),
                                       (2.94, 0.12, 2.5))):
        AR = size * 0.436 * rr
        legk = base - (H*0.795 - size*0.905) - AR*1.02
        s += (f'<path d="M{W/2-AR:.0f},{base:.0f} L{W/2-AR:.0f},{base-legk*0.62:.0f} '
              f'A{AR:.0f},{AR:.0f} 0 0 1 {W/2+AR:.0f},{base-legk*0.62:.0f} '
              f'L{W/2+AR:.0f},{base:.0f}" fill="none" stroke="{INK_600}" '
              f'stroke-width="{wdt}" opacity="{op}"/>')
    s += lockup(W/2 - 300, H*0.862, 600, SLATE_400, SIG_400, 0.85)
    write("0-arch", s)


# ══════════════════════════════════════════════════════════════════
# 1 · CANVAS — the product's node graph, traced
# ══════════════════════════════════════════════════════════════════
# 2 · BLUEPRINT — the mark as a construction drawing
#
# The logo here is the shipped path via mark(); every tick, tangent and
# dimension measures THAT via mark_geo(). An earlier version hand-drew the
# arch and got the legs 26% short, the dot 4x too small and the plumb dashes
# 5x too thin — a bastardised logo under a nice treatment.
# ══════════════════════════════════════════════════════════════════
def w_blueprint():
    d = [dotgrid(64, 1.6, INK_600, 0.16), glow("gD", SIG_600, [(0, 0.11), (1, 0)])]
    s = head("".join(d))
    s += f'<rect width="{W}" height="{H}" fill="{INK_975}"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#dg64)"/>'
    for i in range(0, W + 1, 320):
        s += f'<line x1="{i}" y1="0" x2="{i}" y2="{H}" stroke="{INK_800}" stroke-width="1.2" opacity="0.65"/>'
    for j in range(0, H + 1, 320):
        s += f'<line x1="0" y1="{j}" x2="{W}" y2="{j}" stroke="{INK_800}" stroke-width="1.2" opacity="0.65"/>'

    size = 1620
    mx, my = W/2 - size/2, H*0.465 - 35*(size/72.0)
    g = mark_geo(mx, my, size)
    cx, cy = g["cx"], g["cy"]
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{W*0.32}" ry="{H*0.42}" fill="url(#gD)"/>'

    s += (f'<circle cx="{cx}" cy="{cy}" r="{g["r_mid"]:.0f}" fill="none" stroke="{SIG_600}" '
          f'stroke-width="2" stroke-dasharray="16 20" opacity="0.38"/>')
    ring = g["r_out"] * 1.48
    s += f'<circle cx="{cx}" cy="{cy}" r="{ring:.0f}" fill="none" stroke="{INK_700}" stroke-width="1.8" opacity="0.85"/>'
    s += (f'<circle cx="{cx}" cy="{cy}" r="{g["r_out"]*0.46:.0f}" fill="none" stroke="{INK_700}" '
          f'stroke-width="1.6" stroke-dasharray="5 26" opacity="0.7"/>')
    for a in range(0, 360, 15):
        t = math.radians(a)
        ln = 40 if a % 45 == 0 else 20
        s += (f'<line x1="{cx+ring*math.cos(t):.1f}" y1="{cy+ring*math.sin(t):.1f}" '
              f'x2="{cx+(ring+ln)*math.cos(t):.1f}" y2="{cy+(ring+ln)*math.sin(t):.1f}" '
              f'stroke="{INK_600}" stroke-width="1.8" opacity="0.75"/>')
    s += (f'<line x1="{cx-ring-160:.0f}" y1="{cy}" x2="{cx+ring+160:.0f}" y2="{cy}" '
          f'stroke="{INK_600}" stroke-width="1.6" stroke-dasharray="40 16 6 16" opacity="0.7"/>')
    s += (f'<line x1="{cx}" y1="{cy-ring-160:.0f}" x2="{cx}" y2="{g["foot"]+300:.0f}" '
          f'stroke="{INK_600}" stroke-width="1.6" stroke-dasharray="40 16 6 16" opacity="0.7"/>')

    s += mark(mx, my, size, SIG_400)

    dy = g["foot"] + 150
    x0, x1 = cx - g["r_out"], cx + g["r_out"]
    s += f'<line x1="{x0:.0f}" y1="{dy:.0f}" x2="{x1:.0f}" y2="{dy:.0f}" stroke="{INK_500}" stroke-width="1.8"/>'
    for e in (x0, x1):
        s += f'<line x1="{e:.0f}" y1="{dy-28:.0f}" x2="{e:.0f}" y2="{dy+28:.0f}" stroke="{INK_500}" stroke-width="1.8"/>'
    s += (f'<rect x="{cx-130:.0f}" y="{dy-27:.0f}" width="260" height="54" fill="{INK_975}"/>'
          f'<text x="{cx:.0f}" y="{dy+11:.0f}" text-anchor="middle" '
          f'font-family="JetBrainsMono Nerd Font, monospace" font-size="30" letter-spacing="4" '
          f'fill="{SLATE_500}">SPAN 1.00</text>')

    s += (f'<text x="200" y="{H-256}" font-family="JetBrainsMono Nerd Font, monospace" font-size="30" '
          f'letter-spacing="9" fill="{INK_500}">ARCHWAY · PRODUCT OBSERVABILITY</text>')
    s += (f'<text x="200" y="{H-192}" font-family="JetBrainsMono Nerd Font, monospace" font-size="30" '
          f'letter-spacing="9" fill="{INK_600}">MAKE THE INVISIBLE VISIBLE</text>')
    write("2-blueprint", s)


# ══════════════════════════════════════════════════════════════════
# 3 · SIGNAL — the arch resolved out of a dot field
# ══════════════════════════════════════════════════════════════════
def w_signal():
    s = head(glow("gE", SIG_600, [(0, 0.16), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_950}"/>'
    s += f'<ellipse cx="{W/2}" cy="{H*0.5}" rx="{W*0.4}" ry="{H*0.5}" fill="url(#gE)"/>'

    cx, cy, R, leg = W/2, H*0.485, 880.0, 1000.0
    step = 30.0

    def dist_to_arch(px, py):
        """Distance from (px,py) to the arch skeleton: semicircle + two legs."""
        best = 1e9
        if py <= cy:
            best = abs(math.hypot(px-cx, py-cy) - R)
        for lx in (cx-R, cx+R):
            if cy <= py <= cy+leg:
                best = min(best, abs(px-lx))
            elif py > cy+leg:
                best = min(best, math.hypot(px-lx, py-(cy+leg)))
        if py > cy:
            best = min(best, min(math.hypot(px-(cx-R), py-cy), math.hypot(px-(cx+R), py-cy)))
        return best

    parts = []
    y = step/2
    row = 0
    while y < H:
        x = step/2 + (step/2 if row % 2 else 0)
        while x < W:
            dd = dist_to_arch(x, y)
            if dd < 230:
                t = 1.0 - dd/230.0
                r = 1.7 + 8.6 * (t ** 2.4)
                op = 0.10 + 0.90 * (t ** 2.0)
                col = SIG_300 if t > 0.86 else SIG_400
                parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.2f}" fill="{col}" opacity="{op:.3f}"/>')
            else:
                fade = max(0.0, 1.0 - (dd-230)/1700.0)
                op = 0.06 + 0.22 * fade
                if op > 0.065:
                    parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.9" fill="{SLATE_500}" opacity="{op:.3f}"/>')
            x += step
        y += step * 0.87
        row += 1
    s += "".join(parts)
    s += f'<circle cx="{cx}" cy="{cy-R*0.0}" r="0" fill="none"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="20" fill="{SLATE_50}"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="54" fill="none" stroke="{SIG_300}" stroke-width="3" opacity="0.6"/>'
    write("3-signal", s)


# ══════════════════════════════════════════════════════════════════
# 4 · JOURNEY — a traced user journey across the system
# ══════════════════════════════════════════════════════════════════
# 5 · COLONNADE — an arcade of arches, one carrying the signal


# ══════════════════════════════════════════════════════════════════
# QUIET SET — few lines, low contrast, mark always at true proportion.
# Every one of these draws the shipped path through mark() and measures
# with mark_geo(); none re-derives the geometry by eye.
# ══════════════════════════════════════════════════════════════════

def echo_arch(g, k, stroke, width, op):
    """One hairline echo of the mark, k x its radius, standing on its feet
       and keeping the mark's own 1.162 leg-to-radius ratio."""
    R = g["r_mid"] * k
    cy = g["foot"] - R * 1.162
    return (f'<path d="M{g["cx"]-R:.1f},{g["foot"]:.1f} L{g["cx"]-R:.1f},{cy:.1f} '
            f'A{R:.1f},{R:.1f} 0 0 1 {g["cx"]+R:.1f},{cy:.1f} L{g["cx"]+R:.1f},{g["foot"]:.1f}" '
            f'fill="none" stroke="{stroke}" stroke-width="{width}" opacity="{op}"/>')


def w_halo():
    """The mark and four echoes of it. That is the whole picture."""
    s = head(glow("gH", SIG_600, [(0, 0.15), (0.55, 0.04), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_950}"/>'
    size = 1180
    mx, my = W/2 - size/2, H*0.50 - 35*(size/72.0)
    g = mark_geo(mx, my, size)
    s += f'<ellipse cx="{g["cx"]}" cy="{g["cy"]}" rx="{W*0.30}" ry="{H*0.40}" fill="url(#gH)"/>'
    for k, op in ((1.38, 0.50), (1.82, 0.30), (2.32, 0.17), (2.88, 0.09)):
        s += echo_arch(g, k, INK_700, 3, op)
    s += mark(mx, my, size, SIG_400)
    write("1-halo", s)


def w_veil():
    """The mark as a single soft wash — no stroke, no field, nothing else."""
    s = head(f'<linearGradient id="veil" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{SIG_300}" stop-opacity="0.80"/>'
             f'<stop offset="0.45" stop-color="{SIG_400}" stop-opacity="0.38"/>'
             f'<stop offset="1" stop-color="{SIG_600}" stop-opacity="0.04"/>'
             f'</linearGradient>' + glow("gV", SIG_600, [(0, 0.12), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_950}"/>'
    size = 1620
    mx, my = W/2 - size/2, H*0.50 - 35*(size/72.0)
    g = mark_geo(mx, my, size)
    s += f'<ellipse cx="{g["cx"]}" cy="{g["cy"]}" rx="{W*0.34}" ry="{H*0.46}" fill="url(#gV)"/>'
    s += mark(mx, my, size, "url(#veil)")
    write("4-veil", s)


def w_drift():
    """Eight arcs, widely spaced and barely there, with the mark at the
       centre. The calm relative of an interference field."""
    s = head(glow("gR", SIG_600, [(0, 0.12), (0.6, 0.03), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_950}"/>'
    cx, cy = W/2, H*0.70
    s += f'<ellipse cx="{cx}" cy="{cy-420}" rx="{W*0.40}" ry="{H*0.44}" fill="url(#gR)"/>'
    for i in range(8):
        R = 640 + i * 310
        op = 0.28 * (1.0 - i / 8.0) ** 1.2
        s += (f'<path d="M{cx-R},{cy:.0f} A{R},{R} 0 0 1 {cx+R},{cy:.0f}" fill="none" '
              f'stroke="{INK_600}" stroke-width="2.4" opacity="{op:.3f}"/>')
    s += f'<line x1="0" y1="{cy:.0f}" x2="{W}" y2="{cy:.0f}" stroke="{INK_800}" stroke-width="2"/>'
    size = 800
    s += mark(cx - size/2, cy - 65.2*(size/72.0), size, SIG_400)
    write("5-drift", s)


def w_eclipse():
    """Almost nothing: one soft bloom with the mark low-contrast inside it.
       Near-black at the edges."""
    s = head(glow("gE2", SIG_500, [(0, 0.26), (0.35, 0.08), (0.7, 0.015), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_975}"/>'
    size = 1320
    mx, my = W/2 - size/2, H*0.50 - 35*(size/72.0)
    g = mark_geo(mx, my, size)
    s += f'<ellipse cx="{g["cx"]}" cy="{g["cy"]}" rx="{W*0.30}" ry="{W*0.30}" fill="url(#gE2)"/>'
    s += mark(mx, my, size, SIG_400, 0.32)
    s += mark(mx, my, size, SIG_300, 0.80, arch=False)     # dot + plumb stay crisp
    write("6-eclipse", s)


def w_plumb():
    """Inverted emphasis: the arch recedes to a whisper and the plumb line —
       the part of the mark that measures — carries the accent."""
    s = head(glow("gPL", SIG_600, [(0, 0.13), (0.6, 0.03), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_950}"/>'
    size = 1520
    mx, my = W/2 - size/2, H*0.50 - 35*(size/72.0)
    g = mark_geo(mx, my, size)
    s += f'<ellipse cx="{g["cx"]}" cy="{g["cy"]}" rx="{W*0.26}" ry="{H*0.40}" fill="url(#gPL)"/>'
    s += mark(mx, my, size, INK_700, 0.90, dot=False, plumb=False)
    s += (f'<line x1="{g["cx"]}" y1="{g["dot_y"]:.0f}" x2="{g["cx"]}" y2="{g["foot"]-60:.0f}" '
          f'stroke="{SIG_600}" stroke-width="2" opacity="0.28"/>')
    s += mark(mx, my, size, SIG_400, 1.0, arch=False)
    write("7-plumb", s)


if __name__ == "__main__":
    w_arch(); w_halo(); w_blueprint(); w_signal()
    w_veil(); w_drift(); w_eclipse(); w_plumb()
