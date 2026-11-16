# Comms setup: Slack, Chrome profiles, Zoom, mail, calendar

Set up on November 16, 2026. One Chrome profile per organization keeps each
org's logins apart, so Zoom and Outlook (which hold one login per browser) can
be signed in to every account at once.

| Profile | Chrome dir | Accounts | Color |
|---|---|---|---|
| Personal | `Default` | Personal Gmail | neutral gray |
| Archway | `Profile 1` | Google Workspace | `#6B8AFD` |
| CAVA | `Profile 2` | Microsoft 365 (Outlook), Slack | `#F9D000` |
| TRF | `Profile 3` | Microsoft 365 (Outlook, Teams) | `#005F5D` |

## Pieces

| Path in repo | Installed to | What |
|---|---|---|
| `local/bin/webapp-profile` | `~/.local/bin/` | Opens a web app or meeting link in the right profile; picker when ambiguous |
| `local/bin/cal-sync` | `~/.local/bin/` | Merges every profile's calendar into `~/.cache/cal-sync/events.json` (uv script) |
| `local/applications/*.desktop` | `~/.local/share/applications/` | Gmail, Google Calendar, Outlook, Outlook Calendar, Teams, Chrome Profile, Zoom |
| `local/icons/` | `~/.local/share/icons/` | Launcher icons |
| `config/hypr/chrome-profiles.lua` | `~/.config/hypr/` | Web app window borders in each profile's brand color (required from `hyprland.lua`) |
| `config/systemd/user/cal-sync.*` | `~/.config/systemd/user/` | Refreshes the calendar every 5 minutes |
| `system/chrome-policies/bitwarden.json` | `/etc/opt/chrome/policies/managed.d/` | Force-installs and pins Bitwarden in every profile |
| `scripts/setup-comms.sh` | run once | Creates the profiles, policies and timer |

## New machine

1. `./install.sh <machine>` (links the files above), then `yay -S slack-desktop`.
2. Quit Chrome, run `./scripts/setup-comms.sh`.
3. In each profile: log in to Bitwarden (self-hosted Vaultwarden), then the org's accounts.
4. Paste private calendar addresses into `~/.config/cal-sync/feeds.conf`
   (template: `docs/feeds.conf.example`; never commit the real file).

## Things that can't be captured as files

- **Slack menu bar:** Window > uncheck "Always Show Menu Bar" (Alt shows it).
  The setting syncs from Slack, so editing its state file doesn't stick.
- **Bookmarks:** Archway and Rockefeller folders were copied from Personal into
  their profiles. Personal's bookmarks sync to Google; delete there in Chrome, never
  by editing the file.
- **Profile pictures:** Chrome only allows built-in avatars for profiles that aren't
  signed in to Google, so brand logos can't be used. The toolbar color identifies them.
- **Omarchy's Chrome theme:** the policy folder is a symlink so Omarchy's theme changes
  don't override the brand colors. If Chrome turns one color again after an Omarchy
  update, re-run `setup-comms.sh`.
