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
| `local/bin/webapp-profile` | `~/.local/bin/` | Opens a web app, meeting link (`join`) or any link (`pick`) in the right profile; picker when ambiguous |
| `local/bin/link-router` | `~/.local/bin/` | Handles every `https` link; see below |
| `local/applications/*.desktop` | `~/.local/share/applications/` | Gmail, Google Calendar, Outlook, Outlook Calendar, Teams, Chrome Profile, Zoom, Link Router |
| `local/icons/` | `~/.local/share/icons/` | Launcher icons |
| `config/hypr/chrome-profiles.lua` | `~/.config/hypr/` | Web app window borders in each profile's brand color (required from `hyprland.lua`) |
| `config/hyprland-mimeapps.list` | `~/.config/` | Sends `https` links to link-router (Omarchy reads this before `mimeapps.list`) |
| `system/chrome-policies/bitwarden.json` | `/etc/opt/chrome/policies/managed.d/` | Force-installs and pins Bitwarden in every profile |
| `scripts/setup-comms.sh` | run once | Creates the profiles and policies, puts OmaCal's widget on the bar |

## New machine

1. `./install.sh <machine>` (links the files above), then `yay -S slack-desktop omacal-bin`.
2. Quit Chrome, run `./scripts/setup-comms.sh`.
3. In each profile: log in to Bitwarden (self-hosted Vaultwarden), then the org's accounts,
   then Zoom. In CAVA's and TRF's Outlook, add the **Zoom for Outlook** add-in.
4. OmaCal (see Calendar), then copy `docs/link-router-profiles.conf.example` to
   `~/.config/link-router/profiles.conf` and fill in the account emails.

## Calendar

OmaCal (`omacal-bin`, AUR) holds every calendar; its own `omacal.upcoming` bar widget
(installed by OmaCal, placed left of the clock) shows the next meeting, and its reminders
are the only meeting alerts. **Super + Ctrl + J** opens the widget's agenda; **J** joins.

OmaCal keeps accounts and settings in its own database (`~/.local/share/com.omacal.app/`),
so on a new machine set it up by hand:

- **Settings (Ctrl + ,) → Accounts → Add Google account** for Personal and Archway. The
  sign-in page asks which Chrome profile to open in; pick the matching one.
- **Add WebCal account** for CAVA and TRF with each Outlook calendar's published ICS link
  (Outlook → Settings → Calendar → Shared calendars → Publish a calendar → Calendar,
  "Can view all details"). Name them exactly **CAVA** and **TRF**; link-router matches on
  those names. These feeds are read-only; edit those meetings in Outlook on the web.
- Week starts on Sunday (Settings, or `week_start = sunday` in its settings table).

The AUR package lagged upstream on November 17, 2026 (6.3.0 vs 6.5.1); 6.5.1 was built
from the AUR recipe with `pkgver` and the release's published sha256 swapped in.

## Link router

`local/bin/link-router` handles every `https` link; `http` stays on Chrome so Omarchy's
browser detection is unchanged.

- A Zoom, Meet, Teams or Webex link that belongs to an OmaCal event opens in that
  calendar's Chrome profile (OmaCal's Join, the bar widget, links clicked in Slack).
- Sign-in pages opened by apps (Google, Microsoft, Zoom, Slack OAuth) ask which profile.
- Other Zoom links get the profile picker; everything else goes to Chrome as before.

`~/.config/link-router/profiles.conf` maps OmaCal accounts to profiles: an email,
`@domain`, or an account/calendar name, matched exactly (never the feed URL). It is not
in this public repo; template in `docs/link-router-profiles.conf.example`. If an Omarchy
update rewrites `hyprland-mimeapps.list`, re-link it from the repo.

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
