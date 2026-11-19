# omarchy-config

<!-- LAST-UPDATED -->
**Last captured:** 2026-11-19 09:58 MST

My [Omarchy](https://omarchy.org/) configuration — everything on this machine that
differs from a stock Omarchy install.

Omarchy layers packaged defaults (`/usr/share/omarchy/`, read-only, restored on every
update) underneath user overrides in `~/.config/`. This repo tracks only that override
layer, so it stays small and survives Omarchy upgrades cleanly.

## Restore onto a new machine

```bash
# 1. Install Omarchy normally, then:
git clone https://github.com/kylepholloway/omarchy-config ~/Work/Personal/omarchy-config
cd ~/Work/Personal/omarchy-config
./install.sh

omarchy restart shell
hyprctl reload
```

`install.sh` is idempotent. Any real file it would overwrite is moved to
`~/.omarchy-config-backup/<timestamp>/` first — it never clobbers.

Flags: `--no-packages`, `--no-plugins`, `--help`.

## Layout

| Path | What |
|---|---|
| `config/` | Symlinked into `~/.config/`, including the local Slack-normalized tray plugin |
| `local/applications/` | Web app + handler `.desktop` entries → `~/.local/share/applications/` |
| `machines/<name>/` | Machine-specific config, applied only when named on the command line |
| `packages/repo.txt` | `pacman -Qqen` — explicitly installed repo packages |
| `packages/aur.txt` | `pacman -Qqem` — AUR packages |
| `packages/omarchy-plugins.txt` | Shell plugin git URLs (cloned, not vendored) |
| `scripts/capture.sh` | Re-capture package + plugin lists after changes |

## Desktop themes

- **Banana Blueberry** — completed Mac Ghostty palette, matching colors in all four
  terminals, cyan/lilac window borders and shell controls, and three illustrated fruit wallpapers (the five original backgrounds are archived).
  Run `omarchy theme set banana-blueberry`.
- **Archway** — restored Ink/Slate/Signal palette, eight original 5K wallpapers,
  custom shell, Neovim and btop colors, and scoped Archway branding.
  Run `omarchy theme set archway`.

Cycle backgrounds with `omarchy theme bg next` (`Super+Ctrl+Space`). Theme READMEs
under `config/omarchy/themes/` describe the assets and regeneration commands.
Run `python scripts/verify-themes.py` to build and validate the installed themes in
temporary homes and exercise the branding hook without altering your desktop.

The Archway hook saves your existing prompt, lazygit, fastfetch, and branding
files before activation and restores them when leaving. It preserves edits made
while Archway is active. Saved originals live under
`~/.local/state/omarchy/archway-takeover/` until you switch away.

Herdr Desktop follows the selected Omarchy theme through the `50-herdr-desktop`
theme-set hook. It generates `~/.config/herdr-app/themes/omarchy.json` from the
active palette and terminal config, then selects it through Herdr's supported
command. This updates the interface and existing terminals live, preserves other
Herdr preferences, and works for stock themes as well as these two custom themes.
The original standalone Banana Blueberry Herdr theme is retained.
Run `python scripts/verify-herdr-theme-sync.py` for isolated bridge checks.

Herdr's **Brands** layout (Projects sidebar with company logos, brand colors and
agent cards) lives in `config/herdr-app/`; see [docs/herdr-app.md](docs/herdr-app.md).

Apple Music is [Sidra](https://github.com/wimpysworld/sidra) (`sidra-bin`, AUR), a native
client with Widevine. Omarchy's built-in Media bar widget (`omarchy.media`) shows and controls
it over MPRIS, so no Chromium is needed. Sign in to Apple Music inside Sidra once.

Old School RuneScape (Bolt, RuneLite, the synced profile, and the QMK macropad
keymap) is covered in [docs/osrs.md](docs/osrs.md).

The `60-agent-colors` hook keeps Prismantis's prompt frame, label, text, and
fill on the terminal palette, preserving its framed layout and other options.
It also installs a custom `omarchy` Codex theme for code, Markdown, links, and
UI accents. Both use ANSI palette references, so after the first activation
they follow future terminal theme changes without regenerating fixed RGB values.
For already running sessions, use `/reload-plugins` in Claude and select
`omarchy` through `/theme` in Codex once. Codex retains its native prompt layout;
the Prismantis chat bubble layout is Claude-specific. New sessions load the
saved settings automatically. Run `python scripts/verify-agent-colors.py` to
validate the integrations in a temporary home.

## Staying in sync

Two layers, so nothing gets missed when you change things on the fly:

**1. Symlinks — automatic.** `install.sh` symlinks rather than copies, so editing
`~/.config/hypr/bindings.lua` *is* editing this repo. No copying step, no forgetting.
You only have to commit.

**2. `scripts/check.sh` — the safety net.** Reports anything on this machine not
captured here: uncommitted changes, package drift, plugin drift, and — most usefully —
config files you customized but never added to the repo.

```bash
./scripts/check.sh          # exit 0 = in sync, 1 = drift
```

### When you've changed something

```bash
cd ~/Work/Personal/omarchy-config
./scripts/capture.sh        # refresh package/plugin lists + README stamp
git add -A && git commit -m "..." && git push
```

`capture.sh` is only needed for things that can't symlink — packages and plugins.
Config edits are already here.

### Intentionally untracked

`.driftignore` lists files that differ from stock on purpose but must not be tracked —
currently everything written by the `archway-takeover` theme hook (`starship.toml`,
`lazygit/config.yml`, `fastfetch/config.jsonc`, `omarchy/branding/*`). Those are
*derived* while Archway is active; branding assets come from
`config/omarchy/themes/archway/takeover/`, and the prompt is derived from your
saved user configuration. The hook restores your previous files on exit.

## Machine-specific config

`config/hypr/monitors.lua` is shared: it scales the laptop panel at 1x and the
Apple Studio Displays at 2x, matched per display, so it carries to the next
laptop. `machines/<name>/` still works for anything that truly can't transfer
(`./install.sh <name>`); there are no machines in it today. Captured from the
Dell Inspiron 16 7620 (Nov 2026).

## Dev workstation

Repos live in `~/Work/<Workstream>/` (Archway, Holloway Network, Nessi, SoCo,
Personal, Rockefeller); `config/user-dirs.dirs` points `XDG_PROJECTS_DIR` there.

- `config/mise/config.toml` — global toolchain (node, pnpm, supabase, vercel,
  doppler, temporal, uv, gh). Repo pins go in git-excluded `mise.local.toml` files.
- `config/ghostty/kyle.conf` — terminal preferences on top of Omarchy's config.
- `config/environment.d/` — Omarchy's gcr SSH agent and Superwhisper's
  accessibility setting for the session.
- `local/bin/ssh-unlock` + `config/hypr/autostart.lua` — asks for the SSH key
  passphrase once per login; nothing is stored on disk.
- `system/docker/daemon.json` — copy to `/etc/docker/daemon.json` (not linked).

Manual steps after `install.sh`: sign in to `gh`, Doppler, Supabase, Vercel and
ngrok (`ngrok config add-authtoken`), restore `~/.ssh` (keys + host list), clone
the repos, then sign in to the Claude Code MCP servers (`/mcp`).

## What this repo deliberately does NOT contain

Restoring these is manual, by design:

- Browser profiles and session state (`~/.config/google-chrome`, contains auth tokens)
- SSH keys and `~/.ssh/config` (LAN host list — this repo is public), GPG keys, `gh` auth, gnome-keyring
- `~/.config/link-router/profiles.conf` and `~/.config/a7-studio/` (private; see docs/comms.md)
- CLI logins (Doppler, Supabase, Vercel, ngrok) and Claude Code / Codex config
- Anything under `~/.local/share/` other than `.desktop` entries

## Notes

- Third-party Omarchy plugins are cloned from their upstream git URLs, so they update
  independently via `omarchy plugin update`.
- `omarchy install preinstalls` restores the stock Omarchy app set if you ever want the
  removed defaults back.
