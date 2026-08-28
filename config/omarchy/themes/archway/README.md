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
| `vscode.json`       | Tokyo Night as the nearest shipped VS Code base             |
| `icons.theme`       | `Yaru-blue`                                                  |
| `keyboard.rgb`      | Signal-400                                                   |
| `chromium.theme`    | Ink-950 as the browser frame colour                          |
| `unlock.png`        | Plymouth boot + SDDM login mark — pixel art, 581×490          |
| `preview*.png`      | theme-switcher and boot-screen previews                      |
| `backgrounds/`      | seven 5120×2880 wallpapers (see below)                       |

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
| `0-arch`        | the mark at scale, standing on the canvas, echoed in hairlines   |
| `1-canvas`      | a service graph with one path traced in Signal                   |
| `2-blueprint`   | the mark as a construction drawing — dimensions, tangents, ticks |
| `3-signal`      | the arch resolving out of a dot field                            |
| `4-journey`     | a checkout journey traced across four swimlanes                  |
| `5-colonnade`   | an arcade of bays; one carries the signal                        |
| `6-sunken`      | the quiet one — a hairline arch on Ink-975                       |

Regenerate them with the script kept alongside this theme's source, or drop
your own into `~/.config/omarchy/backgrounds/archway/`.

## Branding

`~/.config/omarchy/branding/screensaver.txt` and `about.txt` carry the
Archway mark in block characters. The originals were backed up next to them
as `*.bak.<epoch>`; `omarchy branding screensaver reset` restores Omarchy's.


## Scoping — what reverts when you switch themes

**Everything in this directory is scoped.** `omarchy-theme-set` rebuilds
`~/.local/state/omarchy/current/theme` from scratch on every switch, so the
palette, Hyprland chrome, shell, btop, neovim, icons, keyboard, chromium and
backgrounds all revert on their own.

There is no `vscode.json` here on purpose. `omarchy-theme-set-vscode` prefers a
theme's `vscode.json` (a named third-party extension) over the theme it
generates from `colors.toml`, so shipping one would suppress the real Archway
theme in favour of somebody else's. Without it, Omarchy builds a local
extension straight from these tokens — `#0b0e14` editor, `#e0e5ec` text,
`#6b8afd` focus.

**Four things live outside this directory** and would otherwise persist after
switching away, so `hooks/theme-set.d/archway-takeover` installs them for
`archway` and hands them back to Omarchy for every other theme:

| What | On Archway | On any other theme |
|---|---|---|
| `branding/screensaver.txt` | Archway block art | `$OMARCHY_PATH/logo.txt` |
| `branding/about.txt` (fastfetch logo) | Archway mark | `$OMARCHY_PATH/icon.txt` |
| `fastfetch/config.jsonc` | logo recoloured to accent | removed → falls back to `/etc` |
| `starship.toml` | accent prompt, crit-red error glyph | Omarchy's default |
| `lazygit/config.yml` | Archway theme block | emptied (Omarchy ships it empty) |

fastfetch and starship are **derived** from Omarchy's current defaults by the
hook rather than forked, so upstream changes to either still flow through. Only
the logo takes the accent — the three fastfetch module sections keep their own
colours, because an accent used everywhere means nothing.

**Not scoped, deliberately: the boot and login screens.** They live in
`/usr/share`, need sudo, and rebuild the initramfs — far too heavy for a theme
switch. Set them once and undo them by hand:

```bash
omarchy plymouth set by theme archway
omarchy plymouth reset
```

A `plymouth` or `omarchy` package update can overwrite
`/usr/share/plymouth/themes/omarchy`; re-run the set command if the boot screen
ever reverts.
