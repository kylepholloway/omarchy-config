# Herdr desktop: Brands layout and Projects sidebar

Built November 16–17, 2026. Kyle's Herdr desktop app uses a personal layout, **Brands**,
whose sidebar shows **Projects** (Herdr spaces) with company logos, brand colors, and each
project's coding agents as cards. It replaces Herdr's separate Agents panel.

## What you see

- **Logos instead of letter tiles** for Holloway Network, Archway, Nessi, SoCo and Personal.
  A space matches a brand by its name, else by the folder its first terminal is in
  (`~/Work/<Workstream>/...` or a repo name such as `archway-platform`). Rockefeller and `~`
  keep Herdr's colored letter tile.
- **Brand colors.** The selected project gets a thin outline and faint tint in its brand
  color; agent cards are outlines in that color, and the focused card is a solid fill with
  dark or white text, whichever reads better.
- **Agent cards** under each project, grouped Needs you / Done / Working / Idle with
  counts, showing the program icon, the agent's title, time since its status last changed,
  and its status. Click a card to go to that pane. The project row shows the same counts
  on the right.
- **Paperclip links**: Holloway Network (HOL), Archway (ARC) and Rockefeller (ROC) have a
  line that opens that company's issues. Link only on purpose; live counts would need
  server-side keys (closed holloway-network PR #203 has that design).

## Files

| Repo path | Live path | How |
|---|---|---|
| `config/herdr-app/mods/my-spaces/` | `~/.config/herdr-app/mods/my-spaces` | symlink to the folder |
| `config/herdr-app/layouts/brands.json` | `~/.config/herdr-app/layouts/brands.json` | copy (Herdr rewrites it) |

- `mods/my-spaces/brands.js` is the one place to edit: each brand's name, logo, color,
  matching words, folder and Paperclip link. Edits apply live.
- `mods/my-spaces/brands/*.png` are 72px rounded tiles, made with `rsvg-convert` and
  ImageMagick from each repo's own favicon or logo (Nessi's is the "n" cut from its
  wordmark).
- Herdr writes `gpui-kit.d.ts` and `jsconfig.json` into every mod folder on start; they are
  git-ignored.
- The layout is a copy, not a symlink: Herdr writes layout files itself (a theme pick,
  for example), which would replace a symlink with a plain file. After changing the layout
  on purpose, copy it back into the repo.
- Theme colors come from the Omarchy `50-herdr-desktop` hook (see the README), not from
  these files.

## Restore on a new machine

```sh
ln -s ~/Work/Personal/omarchy-config/config/herdr-app/mods/my-spaces ~/.config/herdr-app/mods/my-spaces
cp ~/Work/Personal/omarchy-config/config/herdr-app/layouts/brands.json ~/.config/herdr-app/layouts/
herdr-app check ~/.config/herdr-app/mods/my-spaces
herdr-app do layout.switch --name brands
```

`ctrl-shift-l` cycles back to Herdr's own `main` layout; `ctrl-alt-shift-escape` always
resets to it.

## After Herdr updates

`my-spaces` is a clone of Herdr's shipped `spaces` mod (version 0.1.16) and `brands.json`
of its `main` layout. Herdr never updates clones, so they miss later fixes to the
originals. If the sidebar misbehaves after an update, clone the new `spaces` mod and
re-apply the changes (logos, cards, segments, counts, colors, Paperclip links, the
"Projects" header) from this folder's `main.js`.
