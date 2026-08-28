#!/usr/bin/env bash
# Build ~/Applications — a macOS-style folder holding EVERY installed app,
# each showing its real logo. Complements the curated Favorites menu
# (SUPER+ALT+SPACE): that is the short list, this is the findable catch-all.
#
# Re-run after installing or removing software.
set -uo pipefail

DEST="${1:-$HOME/Applications}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$DEST"
find "$DEST" -maxdepth 1 -name '*.desktop' -delete 2>/dev/null

# ---------------------------------------------------------------- icon lookup
ICON_DIRS=("$HOME/.local/share/icons" "$HOME/.icons")
IFS=":" read -ra _dd <<< "${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"
for _d in "${_dd[@]}"; do ICON_DIRS+=("$_d/icons"); done
ICON_DIRS+=(/usr/share/pixmaps)

# Highest-resolution match wins; scalable SVG beats every raster size.
resolve_icon() {
  local name=$1 d f best="" bestscore=-1 score
  for d in "${ICON_DIRS[@]}"; do
    [[ -d $d ]] || continue
    while IFS= read -r f; do
      [[ -n $f ]] || continue
      if [[ $f == *.svg ]]; then
        score=10000
      else
        score=$(sed -n 's|.*/\([0-9]\{1,\}\)x[0-9]\{1,\}.*|\1|p' <<<"$f")
        [[ $score =~ ^[0-9]+$ ]] || score=1
      fi
      if (( score > bestscore )); then bestscore=$score; best=$f; fi
    done < <(find "$d" \( -name "$name.svg" -o -name "$name.png" -o -name "$name.xpm" \) 2>/dev/null)
  done
  [[ -n $best ]] && printf '%s\n' "$best"
}

# -------------------------------------------------------------------- scan
declare -A seen
count=0 iconed=0

scan() {
  local dir=$1 f id name out icon path
  [[ -d $dir ]] || return 0
  while IFS= read -r -d '' f; do
    id="$(basename "$f" .desktop)"
    [[ -n ${seen[$id]+x} ]] && continue        # first match wins (user > system)
    seen[$id]=1

    grep -q '^Type=Application' "$f" || continue
    # NoDisplay/Hidden marks MIME and action handlers (polkit prompts, disk-image
    # mounters) that are not apps. We do NOT honour omarchy's launcher.hides —
    # those are real apps merely hidden for launcher noise, and findability is
    # this folder's whole purpose.
    grep -qE '^(NoDisplay|Hidden)=true' "$f" && continue

    name="$(grep -m1 '^Name=' "$f" | cut -d= -f2- | tr '/' '-')"
    [[ -z $name ]] && name="$id"
    out="$DEST/$name.desktop"

    cp "$f" "$out"
    chmod +x "$out"
    gio set "$out" metadata::trusted true 2>/dev/null

    icon="$(grep -m1 '^Icon=' "$f" | cut -d= -f2-)"
    path=""
    if [[ -n $icon ]]; then
      if [[ $icon == /* && -f $icon ]]; then path="$icon"
      else path="$(resolve_icon "$icon")"; fi
    fi
    if [[ -n $path ]]; then
      gio set "$out" metadata::custom-icon "file://$path" 2>/dev/null && iconed=$((iconed+1))
    fi
    count=$((count+1))
  done < <(find "$dir" -maxdepth 1 -type f -name '*.desktop' -print0 2>/dev/null | sort -z)
}

scan "$HOME/.local/share/applications"
for d in "${_dd[@]}"; do scan "$d/applications"; done

# The folder's own Launchpad-style icon.
FOLDER_ICON="$REPO/assets/folder-applications.png"
[[ -f $FOLDER_ICON ]] && gio set "$DEST" metadata::custom-icon "file://$FOLDER_ICON" 2>/dev/null

echo "$count apps -> $DEST  ($iconed with logos)"
