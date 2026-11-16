#!/usr/bin/env bash
# Recreate the comms setup (Chrome profiles per org, Bitwarden everywhere,
# brand colors, merged calendar) on a fresh Omarchy machine.
# See docs/comms.md. Safe to re-run. Quit Chrome first (Ctrl+Q).
#
#   ./scripts/setup-comms.sh
#
# Needs: install.sh already run (links local/bin, applications, icons, hypr,
# systemd units), google-chrome as the default browser, slack-desktop installed.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
say() { printf '\033[1;36m==>\033[0m %s\n' "$*"; }

if pgrep -x chrome >/dev/null; then
  echo "Quit Chrome first (Ctrl+Q in any window), then re-run." >&2
  exit 1
fi

# --------------------------------------------------------------- policies
# Omarchy writes one theme color to every Chrome profile (color.json) on each
# theme change. Its writer skips a policy directory that is a symlink, so move
# the policies into managed.d, link to it, and drop color.json. Then force
# Bitwarden (self-hosted Vaultwarden) into every profile.
say "Chrome policies: per-profile colors + Bitwarden"
sudo sh -c '
  set -e
  cd /etc/opt/chrome/policies 2>/dev/null || { mkdir -p /etc/opt/chrome/policies; cd /etc/opt/chrome/policies; }
  if [ -d managed ] && [ ! -L managed ]; then mv managed managed.d; fi
  mkdir -p managed.d
  [ -L managed ] || ln -s managed.d managed
  rm -f managed.d/color.json
'
sudo install -o root -g root -m 644 "$REPO/system/chrome-policies/bitwarden.json" /etc/opt/chrome/policies/managed.d/bitwarden.json

# --------------------------------------------------------------- profiles
say "Chrome profiles: Personal, Archway, CAVA, TRF"
python3 -I - <<'PY'
import json, os
base = os.path.expanduser("~/.config/google-chrome")
os.makedirs(base, exist_ok=True)
# dir, name, built-in avatar, brand color (None = neutral gray)
PROFILES = [
    ("Default",   None,      None, None),
    ("Profile 1", "Archway", 26,   "6B8AFD"),
    ("Profile 2", "CAVA",    27,   "F9D000"),
    ("Profile 3", "TRF",     28,   "005F5D"),
]
argb = lambda h: (0xFF000000 | int(h, 16)) - (1 << 32)
ls_path = os.path.join(base, "Local State")
ls = json.load(open(ls_path)) if os.path.exists(ls_path) else {}
cache = ls.setdefault("profile", {}).setdefault("info_cache", {})
order = ls["profile"].setdefault("profiles_order", [])
for d, name, avatar, color in PROFILES:
    os.makedirs(os.path.join(base, d), exist_ok=True)
    pp = os.path.join(base, d, "Preferences")
    prefs = json.load(open(pp)) if os.path.exists(pp) else {}
    prefs.setdefault("session", {})["restore_on_startup"] = 1
    theme = prefs.setdefault("browser", {}).setdefault("theme", {})
    if color:
        theme.update({"user_color2": argb(color), "color_variant2": 1, "is_grayscale2": False})
    else:
        theme.pop("user_color2", None)
        theme["is_grayscale2"] = True
    entry = cache.setdefault(d, {})
    if name:
        prefs.setdefault("profile", {}).update({"name": name, "avatar_index": avatar,
            "using_default_name": False, "using_default_avatar": False})
        entry.update({"name": name, "avatar_icon": f"chrome://theme/IDR_PROFILE_AVATAR_{avatar}",
            "is_using_default_name": False, "is_using_default_avatar": False})
    if color:
        entry["profile_color_seed"] = entry["profile_highlight_color"] = argb(color)
    json.dump(prefs, open(pp, "w"))
    if d not in order:
        order.append(d)
json.dump(ls, open(ls_path, "w"))
print("    profiles ready")
PY

# --------------------------------------------------------------- calendar
say "Calendar sync timer"
mkdir -p ~/.config/cal-sync
if [[ ! -e ~/.config/cal-sync/feeds.conf ]]; then
  cp "$REPO/docs/feeds.conf.example" ~/.config/cal-sync/feeds.conf
  chmod 600 ~/.config/cal-sync/feeds.conf
  echo "    add your private calendar addresses to ~/.config/cal-sync/feeds.conf"
fi
systemctl --user daemon-reload
systemctl --user enable --now cal-sync.timer cal-notify.timer

say "Bar widget"
omarchy-shell shell rescanPlugins >/dev/null 2>&1 || true
omarchy bar put kph.calendar --section centerBegin || true

say "Done. Open Chrome, sign in to Bitwarden and each org's accounts in its profile."
