#!/usr/bin/env bash
# Drift check: what on this machine is NOT captured in the repo?
# Exit 0 = in sync, 1 = drift found. Safe to run anytime; changes nothing.
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OMARCHY="${OMARCHY_PATH:-/usr/share/omarchy}"
QUIET=0; [[ ${1:-} == --quiet ]] && QUIET=1
DRIFT=0

hdr()  { (( QUIET )) || printf '\033[1;36m%s\033[0m\n' "$*"; }
item() { (( QUIET )) || printf '    %s\n' "$*"; }

# 1. Uncommitted changes in the repo itself
if [[ -n "$(git -C "$REPO" status --porcelain 2>/dev/null)" ]]; then
  DRIFT=1; hdr "Uncommitted changes in repo:"
  (( QUIET )) || git -C "$REPO" status --short | sed 's/^/    /'
fi

# 2. Package drift
mapfile -t have_repo < <(pacman -Qqen)
mapfile -t want_repo < <(cat "$REPO/packages/repo.txt" 2>/dev/null)
added=$(comm -13 <(printf '%s\n' "${want_repo[@]}" | sort) <(printf '%s\n' "${have_repo[@]}" | sort))
gone=$(comm -23 <(printf '%s\n' "${want_repo[@]}" | sort) <(printf '%s\n' "${have_repo[@]}" | sort))

mapfile -t have_aur < <(pacman -Qqem)
mapfile -t want_aur < <(cat "$REPO/packages/aur.txt" 2>/dev/null)
aadded=$(comm -13 <(printf '%s\n' "${want_aur[@]}" | sort) <(printf '%s\n' "${have_aur[@]}" | sort))
agone=$(comm -23 <(printf '%s\n' "${want_aur[@]}" | sort) <(printf '%s\n' "${have_aur[@]}" | sort))

if [[ -n $added$gone$aadded$agone ]]; then
  DRIFT=1; hdr "Package drift (run scripts/capture.sh):"
  [[ -n $added  ]] && { item "installed, not in repo.txt:"; sed 's/^/      + /' <<<"$added"; }
  [[ -n $gone   ]] && { item "in repo.txt, not installed:"; sed 's/^/      - /' <<<"$gone"; }
  [[ -n $aadded ]] && { item "AUR installed, not tracked:"; sed 's/^/      + /' <<<"$aadded"; }
  [[ -n $agone  ]] && { item "AUR tracked, not installed:"; sed 's/^/      - /' <<<"$agone"; }
fi

# 3. Omarchy plugin drift
live=$(for p in "$HOME"/.config/omarchy/plugins/*/; do
         [[ -d $p ]] && git -C "$p" remote get-url origin 2>/dev/null
       done | sort)
tracked=$(sort "$REPO/packages/omarchy-plugins.txt" 2>/dev/null)
if [[ "$live" != "$tracked" ]]; then
  DRIFT=1; hdr "Plugin drift (run scripts/capture.sh):"
  diff <(echo "$tracked") <(echo "$live") | grep -E '^[<>]' | sed 's/^/    /'
fi

# 4. THE IMPORTANT ONE:
#    config files you customized but never added to the repo.
hdr_shown=0
while IFS= read -r f; do
  rel="${f#"$OMARCHY/config/"}"
  user="$HOME/.config/$rel"
  [[ -f $user ]] || continue
  cmp -s "$f" "$user" && continue              # unchanged from stock
  [[ -L $user ]] && continue                   # already managed by this repo
  case "$rel" in chromium/*|*/Default/*) continue ;; esac   # browser state
  grep -qxF "$rel" "$REPO/.driftignore" 2>/dev/null && continue   # intentionally untracked
  if (( ! hdr_shown )); then
    DRIFT=1; hdr "Customized but NOT in repo:"; hdr_shown=1
  fi
  item "~/.config/$rel"
done < <(find "$OMARCHY/config" -type f 2>/dev/null)

if (( DRIFT == 0 )); then
  (( QUIET )) || printf '\033[1;32m✓ in sync\033[0m\n'
  exit 0
fi
(( QUIET )) || { echo; echo "  cd $REPO && ./scripts/capture.sh && git add -A && git commit"; }
exit 1
