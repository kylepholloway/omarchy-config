# Banana Blueberry

Kyle's Mac Ghostty palette, completed for Omarchy 4.5. Deep blueberry-purple
surfaces, cyan focus, lilac edges, banana-yellow highlights, and the original
orange cursor. The sixteen terminal colors are preserved exactly, including
the purple bright-red slot. Fonts, padding, and opacity stay in your terminal
preferences.

`colors.toml` drives Omarchy's generated app themes: btop, Chromium, Neovim,
Helix, VS Code, Obsidian, agent interfaces, the shell, and keyboard lighting.
The shell section overrides style controls, menus, launcher, and lock input
while retaining upstream defaults for other sections. Hyprland borders follow
the same cyan-to-lilac focus gradient.

The four terminal configs preserve the Mac ANSI black/white, selection, and
orange cursor. `ghostty.conf` is the original source. Run `python build.py`
to regenerate Alacritty, Kitty, Foot, and the three vector wallpapers.
The build needs Python 3.11+, installed Omarchy templates, and `rsvg-convert`.

## Illustrated wallpaper collection

Three original artworks generated for this palette with the built-in image
generation tool. The saved images retain their native 1672×941 resolution;
Omarchy scales them to your displays.

| File | Look |
|---|---|
| `01-midnight-snack.png` | Sculptural banana ribbons and detailed blueberries under dramatic studio lighting |
| `02-banana-moon.png` | A glowing banana moon above misty blueberry hills |
| `03-fruit-frequency.png` | Bold fruit screenprint with cobalt berries, yellow bananas, and halftone texture |

The original five backgrounds are preserved in `archive/backgrounds/`.
`build.py` regenerates the three older vector designs into that archive, keeping
this collection in the active wallpaper rotation. Their editable SVG sources
remain in `wallpaper-sources/`. Complete generation prompts are saved in
`WALLPAPER-PROMPTS.md`.

Additional personal images go in `~/.config/omarchy/backgrounds/banana-blueberry/`.

Apply with `omarchy theme set banana-blueberry`. Cycle wallpapers with
`omarchy theme bg next` or `Super+Ctrl+Space`. No global branding hook is
needed for this theme.

The repo's `50-herdr-desktop` theme-set hook also carries this palette into
Herdr Desktop's interface and terminals. Its generated Herdr theme is named
`omarchy`; the Mac's exact ANSI palette and orange cursor are preserved.
