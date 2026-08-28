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


def mark(x, y, size, fill, opacity=1.0, dot=True, plumb=True):
    """Archway mark scaled from its 72u viewBox, top-left at (x, y)."""
    s = size / 72.0
    p = [f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.5f})" fill="{fill}" opacity="{opacity}">',
         f'<path d="{MARK_ARCH}"/>']
    if dot:
        p.append('<circle cx="36" cy="37" r="4"/>')
    if plumb:
        p.append(f'<path d="{MARK_PLUMB}"/>')
    p.append('</g>')
    return "".join(p)


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
# ══════════════════════════════════════════════════════════════════
def w_blueprint():
    d = [dotgrid(64, 1.6, INK_600, 0.22),
         glow("gD", SIG_600, [(0, 0.13), (1, 0)])]
    s = head("".join(d))
    s += f'<rect width="{W}" height="{H}" fill="{INK_975}"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#dg64)"/>'
    # fine ruled grid
    for i in range(0, W + 1, 320):
        s += f'<line x1="{i}" y1="0" x2="{i}" y2="{H}" stroke="{INK_800}" stroke-width="1.5"/>'
    for j in range(0, H + 1, 320):
        s += f'<line x1="0" y1="{j}" x2="{W}" y2="{j}" stroke="{INK_800}" stroke-width="1.5"/>'
    s += f'<ellipse cx="{W/2}" cy="{H*0.47}" rx="{W*0.35}" ry="{H*0.45}" fill="url(#gD)"/>'

    cx, cy = W/2, H*0.53
    R = 720          # arch springing radius
    leg = 620        # leg length below the springing line
    sw = 26          # stroke weight of the arch itself
    # arch as a stroked path: left leg up, semicircle, right leg down
    arch = (f"M{cx-R},{cy+leg} L{cx-R},{cy} A{R},{R} 0 0 1 {cx+R},{cy} L{cx+R},{cy+leg}")
    # construction geometry
    s += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{SIG_600}" stroke-width="2" stroke-dasharray="18 22" opacity="0.5"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{R*1.42:.0f}" fill="none" stroke="{INK_700}" stroke-width="2" stroke-dasharray="6 30"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{R*0.42:.0f}" fill="none" stroke="{INK_700}" stroke-width="2" stroke-dasharray="6 30"/>'
    s += f'<line x1="{cx-R*1.75:.0f}" y1="{cy}" x2="{cx+R*1.75:.0f}" y2="{cy}" stroke="{INK_600}" stroke-width="2" stroke-dasharray="40 18 8 18"/>'
    s += f'<line x1="{cx}" y1="{cy-R*1.75:.0f}" x2="{cx}" y2="{cy+leg+340}" stroke="{INK_600}" stroke-width="2" stroke-dasharray="40 18 8 18"/>'
    for a in range(0, 360, 15):
        t = math.radians(a)
        r0, r1 = (R*1.42, R*1.42 + (46 if a % 45 == 0 else 24))
        s += (f'<line x1="{cx+r0*math.cos(t):.1f}" y1="{cy+r0*math.sin(t):.1f}" '
              f'x2="{cx+r1*math.cos(t):.1f}" y2="{cy+r1*math.sin(t):.1f}" '
              f'stroke="{INK_600}" stroke-width="2"/>')
    # the arch
    s += f'<path d="{arch}" fill="none" stroke="{SIG_800}" stroke-width="{sw+22}" stroke-linecap="round" opacity="0.35"/>'
    s += f'<path d="{arch}" fill="none" stroke="{SIG_400}" stroke-width="{sw}" stroke-linecap="round"/>'
    # keystone + plumb line
    s += f'<circle cx="{cx}" cy="{cy}" r="26" fill="{SIG_400}"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="72" fill="none" stroke="{SIG_400}" stroke-width="3" opacity="0.55"/>'
    for k in range(1, 9):
        s += f'<rect x="{cx-4}" y="{cy+90+k*62}" width="8" height="26" fill="{SIG_400}" opacity="{max(0.12, 0.9-k*0.1):.2f}"/>'
    # dimension line
    s += f'<line x1="{cx-R}" y1="{cy+leg+180}" x2="{cx+R}" y2="{cy+leg+180}" stroke="{INK_500}" stroke-width="2"/>'
    for e in (cx-R, cx+R):
        s += f'<line x1="{e}" y1="{cy+leg+150}" x2="{e}" y2="{cy+leg+210}" stroke="{INK_500}" stroke-width="2"/>'
    s += (f'<rect x="{cx-140}" y="{cy+leg+152}" width="280" height="56" fill="{INK_975}"/>'
          f'<text x="{cx}" y="{cy+leg+193}" text-anchor="middle" font-family="JetBrainsMono Nerd Font, monospace" '
          f'font-size="34" letter-spacing="4" fill="{SLATE_500}">SPAN 1.00</text>')
    # corner plate
    s += (f'<text x="200" y="{H-260}" font-family="JetBrainsMono Nerd Font, monospace" font-size="34" '
          f'letter-spacing="10" fill="{INK_500}">ARCHWAY · PRODUCT OBSERVABILITY</text>')
    s += (f'<text x="200" y="{H-190}" font-family="JetBrainsMono Nerd Font, monospace" font-size="34" '
          f'letter-spacing="10" fill="{INK_600}">MAKE THE INVISIBLE VISIBLE</text>')
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
def w_strata():
    d = [glow("gG", SIG_400, [(0, 0.20), (0.55, 0.05), (1, 0)])]
    s = head("".join(d))
    s += f'<rect width="{W}" height="{H}" fill="{INK_950}"/>'

    base = H * 0.845         # springing floor every arch stands on
    N, hot = 9, 4            # nine bays, the fifth carries the signal
    pitch = W / (N - 1.0)
    R = pitch * 0.295
    leg = 940.0

    def bay(cx, R, leg, stroke, width, op, cap="butt"):
        p = (f"M{cx-R:.0f},{base:.0f} L{cx-R:.0f},{base-leg:.0f} "
             f"A{R:.0f},{R:.0f} 0 0 1 {cx+R:.0f},{base-leg:.0f} L{cx+R:.0f},{base:.0f}")
        return (f'<path d="{p}" fill="none" stroke="{stroke}" stroke-width="{width}" '
                f'opacity="{op}" stroke-linecap="{cap}"/>')

    # the arcade behind: the same bays, receding
    for k, (sc, op) in enumerate(((1.30, 0.15), (1.66, 0.08))):
        for i in range(N + 1):
            s += bay(pitch * (i - 0.5), R * sc, leg * sc, INK_600, 3, op)

    s += f'<ellipse cx="{pitch*hot:.0f}" cy="{base-leg-R*0.4:.0f}" rx="{R*3.2:.0f}" ry="{R*3.0:.0f}" fill="url(#gG)"/>'

    # the arcade itself
    for i in range(N):
        cx = pitch * i
        if i == hot:
            continue
        dist = abs(i - hot) / (N - 1.0)
        s += bay(cx, R, leg, INK_600, 7, 0.85 - 0.35 * dist)
        s += f'<circle cx="{cx:.0f}" cy="{base-leg-R:.0f}" r="9" fill="{INK_500}" opacity="0.8"/>'
        for k in range(1, 7):
            s += (f'<rect x="{cx-3:.0f}" y="{base-leg-R+70+k*66:.0f}" width="6" height="22" '
                  f'fill="{INK_600}" opacity="{max(0.10, 0.55-k*0.07):.2f}"/>')

    # the one bay carrying the signal
    cx = pitch * hot
    s += bay(cx, R, leg, SIG_800, 30, 0.55, "round")
    s += bay(cx, R, leg, SIG_400, 9, 1.0, "round")
    s += f'<circle cx="{cx:.0f}" cy="{base-leg-R:.0f}" r="20" fill="{SIG_400}"/>'
    s += f'<circle cx="{cx:.0f}" cy="{base-leg-R:.0f}" r="62" fill="none" stroke="{SIG_400}" stroke-width="3" opacity="0.5"/>'
    for k in range(1, 8):
        s += (f'<rect x="{cx-5:.0f}" y="{base-leg-R+90+k*70:.0f}" width="10" height="28" '
              f'fill="{SIG_400}" opacity="{max(0.14, 0.95-k*0.12):.2f}"/>')

    # the floor
    s += f'<line x1="0" y1="{base:.0f}" x2="{W}" y2="{base:.0f}" stroke="{INK_700}" stroke-width="4"/>'
    s += f'<line x1="0" y1="{base+14:.0f}" x2="{W}" y2="{base+14:.0f}" stroke="{INK_800}" stroke-width="2"/>'

    s += lockup(W/2 - 300, H * 0.885, 600, SLATE_400, SIG_400, 0.85)
    write("5-colonnade", s)


# ══════════════════════════════════════════════════════════════════
# 6 · SUNKEN — the quiet one
# ══════════════════════════════════════════════════════════════════
def w_sunken():
    d = [dotgrid(96, 1.7, INK_700, 0.55),
         glow("gH", SIG_600, [(0, 0.075), (1, 0)])]
    s = head("".join(d))
    s += f'<rect width="{W}" height="{H}" fill="{INK_975}"/>'
    s += f'<rect width="{W}" height="{H}" fill="url(#dg96)"/>'
    s += f'<ellipse cx="{W/2}" cy="{H*0.55}" rx="{W*0.4}" ry="{H*0.5}" fill="url(#gH)"/>'
    cx, cy, R, leg = W/2, H*0.545, 1080.0, 880.0
    hair = (f"M{cx-R},{cy+leg} L{cx-R},{cy} A{R},{R} 0 0 1 {cx+R},{cy} L{cx+R},{cy+leg}")
    s += f'<path d="{hair}" fill="none" stroke="{INK_600}" stroke-width="5"/>'
    s += (f'<path d="{hair}" fill="none" stroke="{SIG_400}" stroke-width="5" opacity="0.40" '
          f'stroke-dasharray="1400 6000" stroke-dashoffset="-900"/>')
    s += f'<circle cx="{cx}" cy="{cy}" r="14" fill="{SIG_400}"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{SIG_400}" stroke-width="2.5" opacity="0.45"/>'
    for k in range(1, 12):
        s += f'<rect x="{cx-3}" y="{cy+70+k*74}" width="6" height="24" fill="{INK_600}" opacity="{max(0.1,0.7-k*0.055):.2f}"/>'
    s += lockup(W/2-330, H*0.335, 660, SLATE_300, SIG_400, 1.0)
    write("6-sunken", s)




# ══════════════════════════════════════════════════════════════════
# NEW · abstract field studies. No grid, nothing sitting on top of
# anything — the arch itself is the only subject.
# ══════════════════════════════════════════════════════════════════

def arch_path(cx, cy, R, leg, floor=None):
    """The mark's silhouette: two legs and a semicircle between them."""
    b = cy + leg if floor is None else floor
    return (f"M{cx-R:.1f},{b:.1f} L{cx-R:.1f},{cy:.1f} "
            f"A{R:.1f},{R:.1f} 0 0 1 {cx+R:.1f},{cy:.1f} L{cx+R:.1f},{b:.1f}")


def w_moire():
    """Two families of nested arches at slightly different pitch. Where the
       two spacings drift in and out of phase they beat — the banding is
       emergent, not drawn."""
    s = head(glow("gM", SIG_600, [(0, 0.20), (0.55, 0.05), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_950}"/>'
    s += f'<ellipse cx="{W/2}" cy="{H*0.52}" rx="{W*0.46}" ry="{H*0.56}" fill="url(#gM)"/>'
    # Arcs only — no legs. Legs from every ring stack into a picket fence and
    # bury the interference; the springing line does that job on its own.
    cx, cy = W / 2, H * 0.815
    for pitch, col, op0 in ((26.0, SIG_400, 0.55), (29.0, SIG_600, 0.48)):
        i = 0
        while True:
            R = 74 + i * pitch
            if R > W * 0.76:
                break
            fade = 1.0 - (R / (W * 0.76)) ** 1.5
            s += (f'<path d="M{cx-R:.1f},{cy:.1f} A{R:.1f},{R:.1f} 0 0 1 {cx+R:.1f},{cy:.1f}" '
                  f'fill="none" stroke="{col}" stroke-width="2.0" opacity="{op0*fade:.3f}"/>')
            i += 1
    s += f'<line x1="0" y1="{cy:.0f}" x2="{W}" y2="{cy:.0f}" stroke="{INK_700}" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy-232}" r="22" fill="{SLATE_50}"/>'
    s += f'<circle cx="{cx}" cy="{cy-232}" r="60" fill="none" stroke="{SIG_300}" stroke-width="2.5" opacity="0.6"/>'
    for k in range(1, 4):
        s += (f'<rect x="{cx-5}" y="{cy-192+k*46}" width="10" height="26" fill="{SIG_300}" '
              f'opacity="{max(0.14, 0.6-k*0.14):.2f}"/>')
    write("1-moire", s)


def w_contour():
    """The mark read as terrain: offset contours, every fifth one an index
       line, the way a survey sheet marks elevation."""
    s = head(glow("gT", SIG_600, [(0, 0.15), (0.6, 0.04), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_975}"/>'
    s += f'<ellipse cx="{W/2}" cy="{H*0.52}" rx="{W*0.44}" ry="{H*0.54}" fill="url(#gT)"/>'
    cx, cy0, base = W / 2, H * 0.455, H * 1.04
    for i in range(46):
        R = 120 + i * 62
        cy = cy0 - i * 7
        if R > W * 0.62:
            break
        index = (i % 5 == 0)
        t = 1.0 - (i / 46.0) ** 1.3
        s += (f'<path d="{arch_path(cx, cy, R, 0, floor=base)}" fill="none" '
              f'stroke="{SIG_400 if index else INK_600}" '
              f'stroke-width="{4.5 if index else 2.2}" '
              f'opacity="{(0.62 if index else 0.85)*t:.3f}"/>')
        if index and i and R < W * 0.55:
            s += (f'<rect x="{cx-46}" y="{cy-R-17}" width="92" height="34" fill="{INK_975}"/>'
                  f'<text x="{cx}" y="{cy-R+9}" text-anchor="middle" '
                  f'font-family="JetBrainsMono Nerd Font, monospace" font-size="24" '
                  f'letter-spacing="3" fill="{INK_500}">{i*20:03d}</text>')
    s += f'<circle cx="{cx}" cy="{cy0}" r="16" fill="{SIG_400}"/>'
    for k in range(1, 10):
        s += (f'<rect x="{cx-4}" y="{cy0+70+k*58}" width="8" height="24" fill="{SIG_400}" '
              f'opacity="{max(0.08, 0.5-k*0.05):.2f}"/>')
    write("4-contour", s)


def w_orbit():
    """An instrument dial around the mark — bearing ring, tick decades and
       measurement callouts. The crosshair language, taken further."""
    s = head(glow("gO", SIG_400, [(0, 0.16), (0.5, 0.05), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_950}"/>'
    cx, cy = W / 2, H * 0.5
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{W*0.4}" ry="{H*0.6}" fill="url(#gO)"/>'
    for r, wdt, op, dash in ((1180, 2, 0.68, "none"), (980, 1.5, 0.40, "4 26"),
                             (760, 2, 0.55, "none"), (540, 1.5, 0.36, "4 26"),
                             (1290, 3, 0.85, "none")):
        s += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK_600}" '
              f'stroke-width="{wdt}" opacity="{op}" stroke-dasharray="{dash}"/>')
    for a in range(0, 360, 2):
        t = math.radians(a - 90)
        major, mid = (a % 30 == 0), (a % 10 == 0)
        ln = 62 if major else (34 if mid else 16)
        col = SIG_400 if major else INK_500
        r0 = 1290
        s += (f'<line x1="{cx+r0*math.cos(t):.1f}" y1="{cy+r0*math.sin(t):.1f}" '
              f'x2="{cx+(r0+ln)*math.cos(t):.1f}" y2="{cy+(r0+ln)*math.sin(t):.1f}" '
              f'stroke="{col}" stroke-width="{3 if major else 2}" '
              f'opacity="{0.95 if major else (0.68 if mid else 0.38)}"/>')
        if major:
            rl = r0 + 108
            s += (f'<text x="{cx+rl*math.cos(t):.1f}" y="{cy+rl*math.sin(t)+10:.1f}" '
                  f'text-anchor="middle" font-family="JetBrainsMono Nerd Font, monospace" '
                  f'font-size="26" letter-spacing="2" fill="{SLATE_500}">{a:03d}</text>')
    for ang in (0, 90, 180, 270):
        t = math.radians(ang - 90)
        s += (f'<line x1="{cx+300*math.cos(t):.1f}" y1="{cy+300*math.sin(t):.1f}" '
              f'x2="{cx+1240*math.cos(t):.1f}" y2="{cy+1240*math.sin(t):.1f}" '
              f'stroke="{INK_600}" stroke-width="2" stroke-dasharray="46 20 8 20" opacity="0.6"/>')
    size = 900
    s += mark(cx - size/2, cy - size*0.47, size, SIG_400)
    s += f'<circle cx="{cx}" cy="{cy}" r="1290" fill="none" stroke="{SIG_400}" stroke-width="1.5" opacity="0.22"/>'
    write("7-orbit", s)


def w_dotwave():
    """The dot field again, but modulated — dot radius rides a standing wave
       radiating from the keystone. Same language as the dot logo."""
    s = head(glow("gW", SIG_600, [(0, 0.15), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_950}"/>'
    cx, cy = W / 2, H * 0.5
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{W*0.45}" ry="{H*0.55}" fill="url(#gW)"/>'
    step, parts = 30.0, []
    y = step / 2
    row = 0
    while y < H:
        x = step / 2 + (step / 2 if row % 2 else 0)
        while x < W:
            d = math.hypot(x - cx, y - cy)
            wave = math.sin(d / 108.0 - 1.2)           # concentric standing wave
            fall = math.exp(-(d / 2050.0) ** 2)         # energy decays outward
            amp = (wave * 0.5 + 0.5) * fall
            r = 1.5 + 7.2 * (amp ** 1.7)
            if r > 1.7:
                col = SIG_300 if amp > 0.80 else (SIG_400 if amp > 0.42 else INK_500)
                parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.2f}" '
                             f'fill="{col}" opacity="{0.10+0.80*amp:.3f}"/>')
            x += step
        y += step * 0.87
        row += 1
    s += "".join(parts)
    size = 660
    s += mark(cx - size/2, cy - size*0.47, size, INK_950, 1.0)   # knock the field out
    s += mark(cx - size/2, cy - size*0.47, size, SIG_400)
    write("8-dotwave", s)


def w_aperture():
    """The mark rotated about its own keystone — a rosette that only reads
       as an arch once you find one."""
    s = head(glow("gP", SIG_600, [(0, 0.17), (0.6, 0.04), (1, 0)]))
    s += f'<rect width="{W}" height="{H}" fill="{INK_975}"/>'
    cx, cy = W / 2, H * 0.5
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{W*0.42}" ry="{H*0.55}" fill="url(#gP)"/>'
    N = 30
    for i in range(N):
        a = 360.0 * i / N
        depth = abs(((i + N/4) % N) - N/2) / (N/2)     # front-to-back falloff
        op = 0.16 + 0.52 * depth
        col = SIG_400 if depth > 0.72 else INK_600
        s += (f'<g transform="rotate({a:.2f} {cx} {cy})">'
              f'<path d="{arch_path(cx, cy - 260, 640, 150)}" fill="none" '
              f'stroke="{col}" stroke-width="{4 if depth > 0.72 else 2.6}" '
              f'opacity="{op:.3f}"/></g>')
    s += f'<circle cx="{cx}" cy="{cy}" r="250" fill="{INK_975}" opacity="0.94"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="250" fill="none" stroke="{INK_700}" stroke-width="2"/>'
    size = 300
    s += mark(cx - size/2, cy - size*0.46, size, SIG_400)
    write("9-aperture", s)


if __name__ == "__main__":
    w_arch(); w_moire(); w_blueprint(); w_signal(); w_contour()
    w_strata(); w_sunken(); w_orbit(); w_dotwave(); w_aperture()
