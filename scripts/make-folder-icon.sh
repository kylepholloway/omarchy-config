#!/usr/bin/env bash
# Generate a Yaru-style "Applications" folder icon: a Launchpad 3x3 grid on the
# stock folder, using Yaru's own symbol blue. Re-run to restyle for a new theme.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE="${1:-/usr/share/icons/Yaru-blue/256x256/places/folder.png}"
OUT="${2:-$REPO/assets/folder-applications.png}"
SYM="${3:-#01269C}"

[[ -f $BASE ]] || { echo "base folder icon not found: $BASE" >&2; exit 1; }
S=28; G=11; TOT=$((3*S + 2*G))
X0=$(( (256 - TOT) / 2 )); Y0=$(( 146 - TOT/2 ))
draw=""
for r in 0 1 2; do for c in 0 1 2; do
  x=$((X0 + c*(S+G))); y=$((Y0 + r*(S+G)))
  draw="$draw roundrectangle $x,$y $((x+S)),$((y+S)) 7,7"
done; done
magick "$BASE" -fill "$SYM" -stroke none -draw "$draw" "$OUT"
echo "wrote $OUT"
