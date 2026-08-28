#!/usr/bin/env bash
# Restore this Omarchy configuration onto a machine.
# Idempotent: safe to re-run. Existing real files are backed up, never overwritten.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$HOME/.omarchy-config-backup/$STAMP"

MACHINE="${1:-}"
DO_PKGS=1
DO_PLUGINS=1
for arg in "$@"; do
  case "$arg" in
    --no-packages) DO_PKGS=0 ;;
    --no-plugins)  DO_PLUGINS=0 ;;
    --help|-h)
      cat <<'USAGE'
usage: ./install.sh [machine-name] [--no-packages] [--no-plugins]

  machine-name    dir under machines/ to apply (e.g. dell-latitude).
                  Omit to skip machine-specific config (monitors, etc).
  --no-packages   skip installing packages from packages/
  --no-plugins    skip cloning omarchy shell plugins
USAGE
      exit 0 ;;
  esac
done

say() { printf '\033[1;36m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m!!\033[0m %s\n' "$*"; }

# link <source-file> <dest-path>
link() {
  local src=$1 dest=$2
  mkdir -p "$(dirname "$dest")"
  if [[ -L $dest ]]; then
    [[ "$(readlink -f "$dest")" == "$(readlink -f "$src")" ]] && return 0
    rm -f "$dest"
  elif [[ -e $dest ]]; then
    mkdir -p "$(dirname "$BACKUP/${dest#$HOME/}")"
    mv "$dest" "$BACKUP/${dest#$HOME/}"
    warn "backed up ${dest/#$HOME/\~} -> ${BACKUP/#$HOME/\~}"
  fi
  ln -s "$src" "$dest"
}

# ---------------------------------------------------------------- config
say "Linking ~/.config"
while IFS= read -r -d '' f; do
  link "$f" "$HOME/.config/${f#"$REPO/config/"}"
done < <(find "$REPO/config" -type f -print0)

if [[ -d "$REPO/local/icons" ]]; then
  say "Linking ~/.local/share/icons"
  while IFS= read -r -d '' f; do
    link "$f" "$HOME/.local/share/icons/${f#"$REPO/local/icons/"}"
  done < <(find "$REPO/local/icons" -type f -print0)
  gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
fi

say "Linking ~/.local/share/applications"
while IFS= read -r -d '' f; do
  link "$f" "$HOME/.local/share/applications/$(basename "$f")"
done < <(find "$REPO/local/applications" -type f -name '*.desktop' -print0)

# ------------------------------------------------------------- machine
if [[ -n $MACHINE && $MACHINE != --* ]]; then
  if [[ -d "$REPO/machines/$MACHINE" ]]; then
    say "Applying machine config: $MACHINE"
    while IFS= read -r -d '' f; do
      link "$f" "$HOME/.config/${f#"$REPO/machines/$MACHINE/"}"
    done < <(find "$REPO/machines/$MACHINE" -type f -print0)
  else
    warn "no machines/$MACHINE — skipping. Available: $(ls "$REPO/machines" 2>/dev/null | tr '\n' ' ')"
    warn "You will need to write ~/.config/hypr/monitors.lua by hand."
  fi
else
  warn "No machine specified — ~/.config/hypr/monitors.lua not linked."
  warn "Available: $(ls "$REPO/machines" 2>/dev/null | tr '\n' ' ')"
fi

# ------------------------------------------------------------ packages
if (( DO_PKGS )); then
  say "Installing repo packages"
  mapfile -t want < "$REPO/packages/repo.txt"
  missing=()
  for p in "${want[@]}"; do pacman -Q "$p" &>/dev/null || missing+=("$p"); done
  if (( ${#missing[@]} )); then
    printf '    %s missing\n' "${#missing[@]}"
    sudo pacman -S --needed --noconfirm "${missing[@]}"
  else
    echo "    all present"
  fi

  if [[ -s "$REPO/packages/aur.txt" ]]; then
    say "Installing AUR packages"
    mapfile -t awant < "$REPO/packages/aur.txt"
    amissing=()
    for p in "${awant[@]}"; do pacman -Q "$p" &>/dev/null || amissing+=("$p"); done
    if (( ${#amissing[@]} )); then
      command -v yay &>/dev/null || { warn "yay not found; skipping AUR"; amissing=(); }
      (( ${#amissing[@]} )) && yay -S --needed --noconfirm "${amissing[@]}"
    else
      echo "    all present"
    fi
  fi
fi

# ------------------------------------------------------------- plugins
if (( DO_PLUGINS )) && [[ -s "$REPO/packages/omarchy-plugins.txt" ]]; then
  say "Installing Omarchy shell plugins"
  while read -r url; do
    [[ -z $url ]] && continue
    if omarchy plugin list 2>/dev/null | grep -qF "$(basename "$url" .git)"; then
      echo "    already present: $url"
    else
      omarchy plugin add "$url" --enable --yes || warn "failed: $url"
    fi
  done < "$REPO/packages/omarchy-plugins.txt"
fi

# -------------------------------------------------------------- finish
say "Refreshing desktop database"
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true

say "Done."
echo
echo "  Restart the shell:   omarchy restart shell"
echo "  Reload Hyprland:     hyprctl reload"
[[ -d $BACKUP ]] && echo "  Backups saved to:    ${BACKUP/#$HOME/\~}"
echo
echo "  Not restored (by design): logins, browser profiles, SSH keys, keyring."
