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

-- Switchboard: live window overview across all workspaces (Mission Control).
-- https://github.com/thebenwalther/omarchy-switchboard
o.bind("SUPER + SHIFT + code:51", "Switchboard: window overview", "omarchy-shell -q switchboard toggle")

-- ── Reclaim bindings for web apps that were removed ────────────────────────
-- Omarchy binds these to preinstalled web apps; those apps are uninstalled, so
-- the keys did nothing.
hl.unbind("SUPER + SHIFT + S")        -- was Google Maps
hl.unbind("SUPER + SHIFT + P")        -- was Google Photos
hl.unbind("SUPER + SHIFT + X")        -- was X
hl.unbind("SUPER + SHIFT + CTRL + G") -- was Google Messages
hl.unbind("SUPER + SHIFT + ALT + G")  -- was WhatsApp

-- ── Screenshots without a Print key ────────────────────────────────────────
-- This keyboard has no Print key, so Omarchy's PRINT-based capture bindings are
-- unreachable. These mirror macOS: region select is the one you actually use.
o.bind("SUPER + SHIFT + 5", "Screenshot (region)", "omarchy capture screenshot region")
o.bind("SUPER + SHIFT + S", "Screenshot (region)", "omarchy capture screenshot region")
o.bind("SUPER + SHIFT + P", "Screenshot (window)", "omarchy capture screenshot windows")
