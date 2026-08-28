#!/usr/bin/env bash
# Re-capture things that are NOT symlinked and therefore drift:
# package manifests and the omarchy plugin list.
# Config files are symlinked by install.sh, so they track automatically.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

pacman -Qqen > "$REPO/packages/repo.txt"
pacman -Qqem > "$REPO/packages/aur.txt"

: > "$REPO/packages/omarchy-plugins.txt"
for p in "$HOME"/.config/omarchy/plugins/*/; do
  [[ -d $p ]] || continue
  git -C "$p" remote get-url origin 2>/dev/null >> "$REPO/packages/omarchy-plugins.txt" || true
done
sort -u -o "$REPO/packages/omarchy-plugins.txt" "$REPO/packages/omarchy-plugins.txt"

printf 'repo=%s aur=%s plugins=%s\n' \
  "$(wc -l < "$REPO/packages/repo.txt")" \
  "$(wc -l < "$REPO/packages/aur.txt")" \
  "$(wc -l < "$REPO/packages/omarchy-plugins.txt")"

cd "$REPO" && git status --short packages/

# Refresh the "Last captured" stamp in the README.
STAMP="$(date '+%Y-%m-%d %H:%M %Z')"
python3 - "$REPO/README.md" "$STAMP" <<'PY'
import sys, re
p, stamp = sys.argv[1], sys.argv[2]
s = open(p).read()
s = re.sub(r'(<!-- LAST-UPDATED -->\n\*\*Last captured:\*\* ).*',
           lambda m: m.group(1) + stamp, s, count=1)
open(p, 'w').write(s)
PY
echo "stamped README: $STAMP"
