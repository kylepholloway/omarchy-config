-- Keep only your personal keybinding overrides here. Add new bindings or
-- unbind defaults before replacing them.

-- See current bindings and descriptions:
--   omarchy menu keybindings --print

-- To disable every Omarchy default binding, set this in
-- ~/.config/hypr/hyprland.lua before require("default.hypr.omarchy"), then add
-- only the bindings you want below:
--   omarchy_default_bindings = false

-- To disable all preinstalled app/webapp bindings, set:
--   omarchy_preinstalled_bindings = false

-- Add a new binding.
-- o.bind("SUPER + SHIFT + R", "SSH", "alacritty -e ssh your-server")

-- Change an existing binding by unbinding it first, then binding the key again.
-- This example changes SUPER+SPACE from the launcher to the Omarchy root menu.
-- hl.unbind("SUPER + SPACE")
-- o.bind("SUPER + SPACE", "Omarchy menu", "omarchy-menu toggle root")

-- Disable a default binding without replacing it.
-- hl.unbind("SUPER + SHIFT + B")

-- Start Herdr at the root containing the local code repositories. Panes and
-- tabs created inside Herdr still follow the active project's directory.
hl.unbind("SUPER + CTRL + RETURN")
o.bind(
  "SUPER + CTRL + RETURN",
  "Herdr (~/Work)",
  "setsid uwsm-app -- xdg-terminal-exec --dir=/home/kph/Work herdr"
)

-- Keep workspace numbers local to the focused monitor and match each
-- monitor's independent workspace bar.
pcall(dofile, os.getenv("HOME") .. "/.config/omarchy/plugins/mmsbrggr.per-monitor-workspaces/hypr/init.lua")

-- Logitech MX Keys examples:
-- o.bind("SUPER + SHIFT + S", nil, "omarchy-capture-screenshot")
-- o.bind("SUPER + H", nil, "voxtype record toggle")
-- o.bind("SUPER + PERIOD", nil, "omarchy-shell shell toggle omarchy.emojis")
