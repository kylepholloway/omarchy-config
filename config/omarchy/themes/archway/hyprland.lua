-- Archway · Hyprland chrome
--
-- The product's signature affordance is a 2px accent edge on the active
-- thing against a raised surface. The same idea, at window scale: the
-- focused window is bordered in Signal (400 → 600, the accent's own ramp,
-- never a purple-to-blue gradient), everything else falls back to Ink.
--
-- Border only, no shadow. That is what 21 of Omarchy's 22 stock themes do,
-- and Omarchy's default looknfeel sets shadow.enabled = false — so this file
-- stays silent on shadows and lets that default stand.

-- Hyprland takes a gradient as a table, not a "a b 135deg" string.
local active_border_color = { colors = { "rgba(6b8afdff)", "rgba(3b5bdbff)" }, angle = 135 }
local inactive_border_color = "rgba(283044aa)"

hl.config({
  general = {
    col = {
      active_border = active_border_color,
      inactive_border = inactive_border_color,
    },
  },

  group = {
    col = {
      border_active = active_border_color,
      border_inactive = inactive_border_color,
    },

    groupbar = {
      col = {
        active = "rgba(6b8afdff)",
        inactive = "rgba(161c26ff)",
      },
    },
  },
})
