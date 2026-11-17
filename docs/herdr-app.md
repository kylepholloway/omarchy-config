# Herdr desktop: Brands layout and Projects sidebar

Built November 16–17, 2026. Kyle's Herdr desktop app uses a personal layout, **Brands**,
whose sidebar shows **Projects** (Herdr spaces) with company logos, brand colors, and each
project's coding agents as cards. It replaces Herdr's separate Agents panel.

## What you see

- **Logos instead of letter tiles** for Holloway Network, Archway, Rockefeller, Nessi, SoCo,
  Personal and Omarchy. Omarchy is the all-purpose home space (named "Omarchy" on November
  17, 2026; it also matches when Herdr calls it `~`), for system setup and Claude sessions
  that aren't tied to a project.
  A space matches a brand by its name, else by the folder its first terminal is in
  (`~/Work/<Workstream>/...` or a repo name such as `archway-platform`). Anything unmatched
  keeps Herdr's colored letter tile.
- **Brand colors.** The selected project gets a thin outline and faint tint in its brand
  color; agent cards are outlines in that color, and the focused card is a solid fill with
  dark or white text, whichever reads better.
- **Agent cards** under each project, grouped Needs you / Done / Working / Idle with
  counts, showing the program icon, the agent's title, time since its status last changed,
  and its status. Click a card to go to that pane. The project row shows the same counts
  on the right.
- **Home tabs**: every project's first tab (`ctrl-1`) is the `Home` mod. It shows the logo,
  name, folder and agent counts; buttons for New Claude Code, Terminal and Paperclip;
  **recent Claude sessions** (AI titles, newest first; click to resume with
  `claude --resume` in the folder it ran in, or to jump to it when it is already open);
  the project's **repos** (branch when not main, changed files, ahead/behind; click for
  lazygit); and **open pull requests** (checks, review state; people's first, bots' last;
  click to open on GitHub). Sessions and repos refresh every 30 seconds, pull requests every
  5 minutes. Claude Code's own `.claude/settings.local.json` and worktrees don't count as
  changes. A mod pane never exits, so the project stays when all its terminals close.
  Close the Home tab to let a project go.
- **Notes** on each Home tab: a markdown box that autosaves to `NOTES.md` in the project
  folder (Omarchy: `~/Documents/omarchy-notes.md`), so Claude sessions there can read it.
  Edits made elsewhere load in when you aren't typing; if both change at once, yours wins
  and it says so.
- **Notifications** (`my-toast`, a clone of Herdr's `toast`, set as the layout's `toast`):
  while Herdr isn't the focused window, an agent's done or needs-you alert also goes to
  Omarchy's notification center. Clicking it runs the alert's action (go to the agent) and
  focuses Herdr. In-app toasts are unchanged.
- **Window title** names the active project ("Archway · Herdr") for the window switcher.
- **Tab bar** (`my-tabs`, a clone of Herdr's `tabs`): the active tab has the project's brand
  outline and tint; the Home tab shows the project logo.
- **Paperclip links**: Holloway Network (HOL), Archway (ARC) and Rockefeller (ROC) have a
  line that opens that company's issues. Link only on purpose; live counts would need
  server-side keys (closed holloway-network PR #203 has that design).

## Files

| Repo path | Live path | How |
|---|---|---|
| `config/herdr-app/mods/my-spaces/` | `~/.config/herdr-app/mods/my-spaces` | copy (see below) |
| `config/herdr-app/mods/Home/` | `~/.config/herdr-app/mods/Home` | copy |
| `config/herdr-app/mods/my-tabs/` | `~/.config/herdr-app/mods/my-tabs` | copy |
| `config/herdr-app/mods/my-toast/` | `~/.config/herdr-app/mods/my-toast` | copy |
| `config/herdr-app/layouts/brands.json` | `~/.config/herdr-app/layouts/brands.json` | copy (Herdr rewrites it) |

- `mods/my-spaces/brands.js` is the one place to edit: each brand's name, logo, color,
  matching words, folder and Paperclip link. Edits to the live copy apply at once.
- `mods/my-spaces/brands/*.png` are 72px rounded tiles, made with `rsvg-convert` and
  ImageMagick from each repo's own favicon or logo (Nessi's is the "n" cut from its
  wordmark, white on its primary-400 green; Rockefeller's is the public website's favicon;
  Omarchy's is the bold O from its wordmark: the system icon's thin pixel lines broke up at
  sidebar size).
- Herdr writes `gpui-kit.d.ts` and `jsconfig.json` into every mod folder on start; they are
  git-ignored.
- **Both are copies, not symlinks.** Herdr's hot reload does not see edits made through a
  symlinked mod folder (tested November 17, 2026: the change only showed after replacing
  the link), and Herdr rewrites layout files itself (a theme pick, for example), which would
  replace a symlink with a plain file. Edit the live files, then copy them back:

```sh
for m in my-spaces Home my-tabs my-toast; do rsync -a --exclude gpui-kit.d.ts --exclude jsconfig.json --exclude __pycache__ ~/.config/herdr-app/mods/$m/ ~/Work/Personal/omarchy-config/config/herdr-app/mods/$m/; done
cp ~/.config/herdr-app/layouts/brands.json ~/Work/Personal/omarchy-config/config/herdr-app/layouts/
```
- Theme colors come from the Omarchy `50-herdr-desktop` hook (see the README), not from
  these files.

## Restore on a new machine

```sh
for m in my-spaces Home my-tabs my-toast; do rsync -a ~/Work/Personal/omarchy-config/config/herdr-app/mods/$m/ ~/.config/herdr-app/mods/$m/; herdr-app check ~/.config/herdr-app/mods/$m; done
cp ~/Work/Personal/omarchy-config/config/herdr-app/layouts/brands.json ~/.config/herdr-app/layouts/
herdr-app do layout.switch --name brands
```

Spaces and tabs live in herdr-core, not in files. Name each project space explicitly
(`herdr-app do space.rename --id <space id> --name Archway`): an unnamed space is named
after its first terminal's folder and falls back to the folder it was created in once its
terminals close. To give a project its Home tab again (space id from `herdr-app ls`,
folder is the project's; Omarchy's props add `"exact": true` so only sessions started in
`~` itself show, and `"repos": "/home/kyle/Work/Personal"`):

```sh
herdr-app do tab.new '{"space":"<space id>","name":"Home","mod":"Home","props":{"space":"<space id>","folder":"/home/kyle/Work/Archway"},"focus":false}'
herdr-app do tab.move '{"id":"<tab id it printed>","index":0}'
```

Write a new mod's `mod.json` (`{"place": "none"}`) before or with its `main.js` (stage the
folder elsewhere and move it in whole): the first time Herdr sees a mod folder without one,
it docks a copy into the shown layout. A mod pane's header shows the mod's folder name,
which is why the Home mod's folder is called `Home`.

`ctrl-shift-l` cycles back to Herdr's own `main` layout; `ctrl-alt-shift-escape` always
resets to it.

## Checkpoint

Git tag `herdr-very-pleased` (November 17, 2026) marks the look Kyle approved before the
second wave (session resume, repos and pull requests on Home, branded tab bar).

## After Herdr updates

`my-spaces` is a clone of Herdr's shipped `spaces` mod (version 0.1.16), `my-tabs` of its
`tabs` mod, `my-toast` of its `toast` mod, and `brands.json` of its `main` layout. Herdr never updates clones, so they miss later fixes to the
originals. If the sidebar misbehaves after an update, clone the new `spaces` mod and
re-apply the changes (logos, cards, segments, counts, colors, Paperclip links, the
"Projects" header) from this folder's `main.js`.
