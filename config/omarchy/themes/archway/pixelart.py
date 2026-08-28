#!/usr/bin/env python3
"""Turn Omarchy block art into an exact pixel grid, then into SVG rects.

Each character cell holds two square sub-pixels stacked vertically:
  █ = both   ▀ = top only   ▄ = bottom only   (space) = neither

Rendering the grid as rects (rather than as text) means the blocks tile
seamlessly at any scale — no font metrics, no seams between rows.
"""
import sys

TOP    = {"█", "▀"}
BOTTOM = {"█", "▄"}


def to_grid(text):
    rows = [r.rstrip("\n") for r in text.split("\n")]
    while rows and not rows[0].strip():
        rows.pop(0)
    while rows and not rows[-1].strip():
        rows.pop()
    w = max(len(r) for r in rows)
    grid = []
    for r in rows:
        r = r.ljust(w)
        grid.append([c in TOP for c in r])
        grid.append([c in BOTTOM for c in r])
    # crop to ink
    cols = [x for x in range(w) if any(g[x] for g in grid)]
    lines = [y for y in range(len(grid)) if any(grid[y])]
    x0, x1 = min(cols), max(cols)
    y0, y1 = min(lines), max(lines)
    return [row[x0:x1 + 1] for row in grid[y0:y1 + 1]]


def to_svg(grid, px, color, pad=0):
    h, w = len(grid), len(grid[0])
    W, H = (w + pad * 2) * px, (h + pad * 2) * px
    parts = []
    # merge horizontal runs so the SVG stays small and the edges stay crisp
    for y, row in enumerate(grid):
        x = 0
        while x < w:
            if row[x]:
                run = x
                while run < w and row[run]:
                    run += 1
                parts.append(f'<rect x="{(x+pad)*px}" y="{(y+pad)*px}" '
                             f'width="{(run-x)*px}" height="{px}"/>')
                x = run
            else:
                x += 1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" shape-rendering="crispEdges">'
            f'<g fill="{color}">' + "".join(parts) + "</g></svg>"), W, H


if __name__ == "__main__":
    src, out, px, color = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    g = to_grid(open(src).read())
    svg, W, H = to_svg(g, px, color, pad=int(sys.argv[5]) if len(sys.argv) > 5 else 0)
    open(out, "w").write(svg)
    print(f"{len(g[0])}x{len(g)} pixels -> {W}x{H}px")
