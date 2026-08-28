# omarchy-config

<!-- LAST-UPDATED -->
**Last captured:** 2026-08-28 13:49 MDT

My [Omarchy](https://omarchy.org/) configuration — everything on this machine that
differs from a stock Omarchy install.

Omarchy layers packaged defaults (`/usr/share/omarchy/`, read-only, restored on every
update) underneath user overrides in `~/.config/`. This repo tracks only that override
layer, so it stays small and survives Omarchy upgrades cleanly.

## Restore onto a new machine

```bash
# 1. Install Omarchy normally, then:
git clone <this-repo> ~/Work/omarchy-config
cd ~/Work/omarchy-config
./install.sh <machine-name>          # e.g. ./install.sh dell-latitude

omarchy restart shell
hyprctl reload
```

`install.sh` is idempotent. Any real file it would overwrite is moved to
`~/.omarchy-config-backup/<timestamp>/` first — it never clobbers.

Flags: `--no-packages`, `--no-plugins`, `--help`.

## Layout

| Path | What |
|---|---|
| `config/` | Symlinked into `~/.config/` |
| `local/applications/` | Web app + handler `.desktop` entries → `~/.local/share/applications/` |
| `machines/<name>/` | Machine-specific config, applied only when named on the command line |
| `packages/repo.txt` | `pacman -Qqen` — explicitly installed repo packages |
| `packages/aur.txt` | `pacman -Qqem` — AUR packages |
| `packages/omarchy-plugins.txt` | Shell plugin git URLs (cloned, not vendored) |
| `scripts/capture.sh` | Re-capture package + plugin lists after changes |

## Staying in sync

Three layers, so nothing gets missed when you change things on the fly:

**1. Symlinks — automatic.** `install.sh` symlinks rather than copies, so editing
`~/.config/hypr/bindings.lua` *is* editing this repo. No copying step, no forgetting.
You only have to commit.

**2. `scripts/check.sh` — the safety net.** Reports anything on this machine not
captured here: uncommitted changes, package drift, plugin drift, and — most usefully —
config files you customized but never added to the repo.

```bash
./scripts/check.sh          # exit 0 = in sync, 1 = drift
```

**3. Boot notification — the reminder.** `config/omarchy/hooks/post-boot.d/omarchy-config-drift`
runs the check at every boot and sends a desktop notification *only* if there's drift.
Click it to see what changed. Silent when clean.

### When you've changed something

```bash
cd ~/Work/omarchy-config
./scripts/capture.sh        # refresh package/plugin lists + README stamp
git add -A && git commit -m "..." && git push
```

`capture.sh` is only needed for things that can't symlink — packages and plugins.
Config edits are already here.

### Intentionally untracked

`.driftignore` lists files that differ from stock on purpose but must not be tracked —
currently everything written by the `archway-takeover` theme hook (`starship.toml`,
`lazygit/config.yml`, `fastfetch/config.jsonc`, `omarchy/branding/*`). Those are
*derived*; their source of truth is `config/omarchy/themes/archway/takeover/`.
Tracking them would fight the hook and freeze out upstream improvements.

## Machine-specific config

`hypr/monitors.lua` is the one file that genuinely does not transfer — it is tuned to a
specific panel and display layout. It lives under `machines/` and is applied only when
you pass a machine name.

Current machines:

- **dell-latitude** — Dell laptop, `eDP-1` + 2× Apple Studio Display (5120x2880 @ scale 2)

To add one: `mkdir -p machines/<name>/hypr && cp ~/.config/hypr/monitors.lua machines/<name>/hypr/`

## What this repo deliberately does NOT contain

Restoring these is manual, by design:

- Browser profiles and session state (`~/.config/chromium` — ~300MB, contains auth tokens)
- The Apple Music plugin's dedicated Chromium profile / Apple login
- SSH keys, GPG keys, `gh` auth, gnome-keyring
- Anything under `~/.local/share/` other than `.desktop` entries

## Notes

- Omarchy plugins are cloned from their upstream git URLs rather than vendored, so they
  update independently via `omarchy plugin update`.
- `omarchy install preinstalls` restores the stock Omarchy app set if you ever want the
  removed defaults back.
