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
| `config/omarchy/plugins/kph.calendar/` | `~/.config/omarchy/plugins/` | Bar widget: next meeting + countdown; click for a 3-day agenda with Join buttons; middle-click refreshes, right-click joins |
| `local/bin/cal-notify` + `config/systemd/user/cal-notify.*` | `~/.local/bin/`, user timer | Alert 10 minutes before each meeting, with a Join button |
| `local/bin/cal-join-next` | `~/.local/bin/` | **Super + Ctrl + J** (in `bindings.lua`): join the meeting on now or starting within 15 min |
| `scripts/setup-comms.sh` | run once | Creates the profiles, policies, timers and bar widget |

## New machine

1. `./install.sh <machine>` (links the files above), then `yay -S slack-desktop`.
2. Quit Chrome, run `./scripts/setup-comms.sh`.
3. In each profile: log in to Bitwarden (self-hosted Vaultwarden), then the org's accounts.
4. Paste private calendar addresses into `~/.config/cal-sync/feeds.conf`
   (template: `docs/feeds.conf.example`; never commit the real file).

## Calendar

`cal-sync` merges every feed in `~/.config/cal-sync/feeds.conf` every 5 minutes into
`~/.cache/cal-sync/events.json`. The bar widget, the alerts and Super + Ctrl + J all
read that file, and every Join goes through `webapp-profile join <profile> <link>`, so
Zoom, Meet and Teams open in the profile the calendar belongs to.

OmaCal (`omacal-bin`, AUR) is the full calendar app for week and month views; the
widget's "Open calendar" link starts it.

Status on November 16, 2026: Personal feed connected. Archway, CAVA and TRF still need
their addresses; publishing the CAVA and TRF Outlook calendars is Kyle's call (it
creates an unauthenticated link to client calendars).

## Link router

`local/bin/link-router` handles every `https` link (set in `config/hyprland-mimeapps.list`,
which Omarchy reads before `mimeapps.list`; `http` stays on Chrome so Omarchy's browser
detection is unchanged). A Zoom, Meet, Teams or Webex link that belongs to an OmaCal or
cal-sync event opens in that calendar's Chrome profile; other Zoom links get the profile
picker; everything else goes to `omarchy-launch-browser` as before. So OmaCal's Join and
meeting links clicked in Slack land in the right account.

Which calendar maps to which profile: `~/.config/link-router/profiles.conf` (not in the
repo; template `docs/link-router-profiles.conf.example`). If an Omarchy update rewrites
`hyprland-mimeapps.list`, links stop being routed: re-link it from the repo.

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
