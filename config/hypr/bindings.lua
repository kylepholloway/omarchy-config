-- Keep only your personal keybinding overrides here. Add new bindings with
-- o.bind or replace defaults with o.rebind.

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

-- Change an existing binding. o.rebind takes the same arguments as o.bind.
-- This example replaces the default file manager with Flea.
-- o.rebind("SUPER + SHIFT + F", "File manager", { launch = "flea" })

-- Disable a default binding without replacing it.
-- hl.unbind("SUPER + SHIFT + B")

-- Logitech MX Keys examples:
-- o.bind("SUPER + H", nil, "voxtype record toggle")
-- o.bind("SUPER + PERIOD", nil, { panel = "omarchy.emojis" })

-- ── Web apps removed November 16, 2026 ─────────────────────────────────────
-- Omarchy binds these to its preinstalled web apps; those apps are uninstalled,
-- so the keys are freed rather than left doing nothing.
hl.unbind("SUPER + SHIFT + C")        -- HEY Calendar
hl.unbind("SUPER + SHIFT + E")        -- HEY Email
hl.unbind("SUPER + SHIFT + ALT + E")  -- HEY New email
hl.unbind("SUPER + SHIFT + ALT + G")  -- WhatsApp
hl.unbind("SUPER + SHIFT + CTRL + G") -- Google Messages
hl.unbind("SUPER + SHIFT + P")        -- Google Photos
hl.unbind("SUPER + SHIFT + S")        -- Google Maps
hl.unbind("SUPER + SHIFT + X")        -- X
hl.unbind("SUPER + SHIFT + ALT + X")  -- X Post

-- ── Herdr desktop app (November 16, 2026) ──────────────────────────────────
-- Kyle uses the Herdr desktop app (herdr-app + herdr-core), not Herdr's terminal
-- app. Focus its window if it is open, otherwise start it.
o.rebind("SUPER + CTRL + RETURN", "Herdr", { focus = "herdr-app", launch = "/home/kyle/.local/bin/herdr-app" })
hl.unbind("SUPER + CTRL + K")         -- cheat sheet for the Herdr terminal app

-- ── Screenshots, Mac-style (NuPhy Air75) ───────────────────────────────────
-- Mac muscle memory: Cmd+Shift+4. Omarchy's smart mode is the closest match:
-- drag a region, or click a window to take just that window (same as Print).
-- Super+Shift+4 normally moves a window to workspace 4; Super+Shift+Alt+4 still
-- moves it there (without following), then Super+4 to go along.
o.rebind("SUPER + SHIFT + code:13", "Screenshot (Mac Cmd+Shift+4)", "omarchy-capture-screenshot")
o.bind("SUPER + SHIFT + S", "Screenshot", "omarchy-capture-screenshot")
