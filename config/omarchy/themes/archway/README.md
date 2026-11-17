# Archway · Omarchy theme

Built from `archway-design-system/src/tokens.css`. Every colour in this
theme is a design-system token; nothing here was picked by eye.

| Role      | Token family                     | Values                                    |
|-----------|----------------------------------|-------------------------------------------|
| Surfaces  | Ink (cool near-blacks)           | `#07090d → #6a7488`                       |
| Text      | Slate (near-whites, blue hue)    | `#8d98ab → #fafbfc`                       |
| Accent    | **Signal-400 `#6b8afd`**         | one accent, never decorative              |
| Status    | ok / warn / crit / info          | `#4fb39a #e2b14a #c86b6b #7aa0c4`         |
| Extended  | teal / plum / code / orange      | `#4aa39d #b07ed9 #d97757 #dc8742`         |

Signal-400 is the dark-theme accent (`#3b5bdb` is its light-theme twin, unused
here — Omarchy runs the product-side palette). It is reserved for primary
action, active state, links, focus rings and selection. Everything else is Ink
and Slate.

## Files

| File                | What it covers                                              |
|---------------------|-------------------------------------------------------------|
| `colors.toml`       | the palette every other config is generated from            |
| `hyprland.lua`      | window borders and group bars — border only, no shadow      |
| `shell.toml`        | bar, menus, launcher, notifications, polkit, lock screen    |
| `btop.theme`        | meters follow ok→warn→crit; load follows the Signal ramp    |
| `neovim.lua`        | tokyonight remapped onto Archway tokens (no new plugin)     |
| `takeover/`         | assets the `theme-set` hook swaps in and out (see below)     |
| `backgrounds.py`    | generator for the eight wallpapers                             |
| `vscode.json`       | Tokyo Night as the nearest shipped VS Code base             |
| `icons.theme`       | `Yaru-blue`                                                  |
| `keyboard.rgb`      | Signal-400                                                   |
| `chromium.theme`    | Ink-950 as the browser frame colour                          |
| `unlock.png`        | Plymouth boot + SDDM login mark — pixel art, 581×490          |
| `preview*.png`      | theme-switcher and boot-screen previews                      |
| `backgrounds/`      | eight 5120×2880 wallpapers (see below)                       |

Terminal configs (`alacritty.toml`, `foot.ini`, `kitty.conf`, `ghostty.conf`)
are generated from `colors.toml` by Omarchy's own templates, so they stay in
sync automatically.

The system mono stays **JetBrainsMono Nerd Font** — Archway's DM Mono has no
Nerd Font glyphs and is not used anywhere in this theme.

## Boot and login

`unlock.png` is the same block art as the screensaver and the fastfetch logo,
converted to an exact pixel grid (`pixelart.py`) rather than drawn as vectors,
so the boot mark, the screensaver and `fastfetch` all read as one thing. The
mark half of the grid is mirrored about its centre column, because the ASCII
transcode's antialiasing does not produce a symmetric arch on its own.

Apply it with:

```bash
omarchy plymouth set by theme archway   # needs sudo; rebuilds the initramfs
omarchy plymouth reset                  # back to Omarchy's default
```

## Backgrounds

Each one is drawn from the Archway mark or the product canvas. No stock
photography, no illustration, no glowing orbs — per `archway-brain/brand/DESIGN_LANGUAGE.md`.

| File            | What it is                                                       |
|-----------------|------------------------------------------------------------------|
| `0-arch`        | the mark at scale, echoed outward in construction hairlines      |
| `1-halo`        | the mark and four echoes of it — that is the whole picture       |
| `2-blueprint`   | the mark as a construction drawing: springing circle, bearing ring, datum crosshair, span dimension |
| `3-signal`      | the arch resolving out of a dot field                            |
| `4-veil`        | the mark as one soft vertical wash, no stroke and nothing else   |
| `5-drift`       | eight widely spaced arcs, barely there, mark at the centre       |
| `6-eclipse`     | one soft bloom, the mark low-contrast inside it, near-black edges |
| `7-plumb`       | inverted emphasis — the arch whispers, the plumb line takes the accent |

All eight are abstractions of the mark. No charts, no diagrams, and nothing
sitting on a visible grid competing with the windows in front of it. They are
deliberately low-contrast and sparse: a wallpaper that wins a staring contest
with your terminal is a wallpaper doing its job badly.

### The mark's geometry is not guessed

`mark()` draws the shipped path from `src/assets/logo_mark-dm.svg`, and
`mark_geo()` reports that path's real measurements so anything drawn *around*
the mark measures the mark rather than an approximation of it:

| | |
|---|---|
| springing centre | `(36, 35)` in the 72u viewBox |
| radii | 23.8 inner · 26.0 centreline · 28.2 outer |
| leg length | 30.2 — i.e. **1.162 x** the centreline radius |
| centre dot | `r=4` at `y=37` — **0.154 x** R, sitting 2u below the springing line |
| plumb dashes | `w=1.5` — **0.058 x** R |

An earlier `2-blueprint` hand-drew its arch instead and got the legs 26% short
(0.861 x R), the dot 4x too small and the dashes 5x too thin. The treatment
looked right; the logo did not. Draw through `mark()` and that cannot recur.

Only `0-arch` carries the lockup; `2-blueprint` uses a drawing title block
instead. The other six are unsigned — a wordmark on every one reads as branding
applied to wallpaper rather than wallpaper that is on-brand.

Format is whichever encodes smaller per image (JPEG q92 for the dot field,
PNG for the flat ones). Omarchy accepts both. The whole set is 3.1 MB.

Regenerate with `backgrounds.py` (writes SVG; render at 5120x2880 with
`rsvg-convert`), or drop your own into `~/.config/omarchy/backgrounds/archway/`.

## Branding and switching back

The `archway-takeover` theme-set hook applies the original block-art
screensaver, About mark, lazygit colors, a Signal-blue prompt, and fastfetch
logo color. It snapshots your existing files under
`~/.local/state/omarchy/archway-takeover/` before changing them and restores
those exact files when leaving Archway. Files that did not exist are removed.
Edits you make while Archway is active are kept. Reapplying is idempotent,
and a delayed hook for an older selection is ignored.

The prompt is derived from your saved user configuration, retaining your
modules and layout. The hook never resets another theme to stock settings.

All other theme files are scoped by Omarchy's normal theme staging. Terminal
configs, Helix, VS Code, Obsidian, and agent colors are generated from
`colors.toml`; no VS Code marketplace extension is needed. The custom
Neovim colors use the already installed Tokyo Night plugin.

The boot/login mark and previews are included as assets. System boot and
login settings are separate from desktop theme switching.

Switch with `omarchy theme set archway`; cycle the eight wallpapers with
`omarchy theme bg next` or `Super+Ctrl+Space`.

The repo's `50-herdr-desktop` theme-set hook also updates Herdr Desktop's
interface and terminal colors automatically, using the generated `omarchy`
Herdr theme. It works alongside the scoped Archway branding hook.
