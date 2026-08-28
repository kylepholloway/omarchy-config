-- Archway · Neovim
--
-- There is no Archway colorscheme plugin, so this rides tokyonight's
-- structure and rewrites every colour it exposes to an Archway token.
-- Ink for surfaces, Slate for text, Signal for the one accent, and the
-- cool semantic quartet for diagnostics and diffs.

local ink = {
  n975 = "#07090d",
  n950 = "#0b0e14",
  n900 = "#0f1319",
  n800 = "#161c26",
  n700 = "#283044",
  n600 = "#454d5f",
  n500 = "#6a7488",
}
local slate = { s50 = "#fafbfc", s200 = "#ebeef3", s300 = "#e0e5ec", s400 = "#b9c3d4", s500 = "#8d98ab" }
local signal = { s300 = "#8ba0f9", s400 = "#6b8afd", s500 = "#4a6bdc", s600 = "#3b5bdb" }
local ok, warn, crit, info = "#4fb39a", "#e2b14a", "#c86b6b", "#7aa0c4"
local code, teal, plum = "#d97757", "#4aa39d", "#b07ed9"

return {
  {
    "folke/tokyonight.nvim",
    priority = 1000,
    opts = {
      style = "night",
      transparent = false,
      styles = {
        comments = { italic = true },
        keywords = { italic = false },
        sidebars = "normal",
        floats = "normal",
      },
      on_colors = function(c)
        c.bg = ink.n950
        c.bg_dark = ink.n975
        c.bg_float = ink.n900
        c.bg_popup = ink.n900
        c.bg_sidebar = ink.n900
        c.bg_statusline = ink.n900
        c.bg_highlight = ink.n800
        c.bg_visual = ink.n700
        c.bg_search = signal.s600
        c.fg = slate.s300
        c.fg_dark = slate.s400
        c.fg_float = slate.s300
        c.fg_sidebar = slate.s400
        c.fg_gutter = ink.n700
        c.comment = ink.n500
        c.border = ink.n700
        c.border_highlight = signal.s400

        c.blue = signal.s400
        c.blue0 = signal.s600
        c.blue1 = signal.s300
        c.blue2 = signal.s300
        c.blue5 = signal.s300
        c.blue6 = slate.s200
        c.blue7 = signal.s600
        c.cyan = teal
        c.green = ok
        c.green1 = ok
        c.green2 = ok
        c.teal = teal
        c.yellow = warn
        c.orange = code
        c.red = crit
        c.red1 = crit
        c.magenta = plum
        c.magenta2 = plum
        c.purple = plum

        c.git = { add = ok, change = info, delete = crit }
        c.gitSigns = { add = ok, change = info, delete = crit }
        c.diff = {
          add = "#10302a",
          change = "#15212d",
          delete = "#351515",
          text = "#24378c",
        }
        c.error = crit
        c.warning = warn
        c.info = info
        c.hint = teal
        c.todo = signal.s400
        c.terminal_black = ink.n700
      end,
      on_highlights = function(hl, c)
        -- The active-nav affordance: an accent edge on what is current.
        hl.CursorLineNr = { fg = signal.s400, bold = true }
        hl.LineNr = { fg = ink.n600 }
        hl.CursorLine = { bg = ink.n900 }
        hl.ColorColumn = { bg = ink.n900 }
        hl.WinSeparator = { fg = ink.n800 }
        hl.VertSplit = { fg = ink.n800 }
        hl.FloatBorder = { fg = ink.n700, bg = ink.n900 }
        hl.NormalFloat = { fg = slate.s300, bg = ink.n900 }
        hl.Pmenu = { fg = slate.s300, bg = ink.n900 }
        hl.PmenuSel = { fg = slate.s50, bg = ink.n700 }
        hl.PmenuSbar = { bg = ink.n900 }
        hl.PmenuThumb = { bg = ink.n600 }
        hl.Visual = { bg = ink.n700 }
        hl.Search = { fg = ink.n950, bg = signal.s400 }
        hl.IncSearch = { fg = ink.n950, bg = signal.s300 }
        hl.MatchParen = { fg = signal.s300, bold = true }
        hl.Title = { fg = slate.s50, bold = true }
        hl.Directory = { fg = signal.s400 }
        hl.SignColumn = { bg = ink.n950 }
        hl.TabLineSel = { fg = slate.s50, bg = ink.n800 }
        hl.TabLine = { fg = ink.n500, bg = ink.n975 }
        -- Inline code references get the code ramp, not the warn ramp.
        hl["@markup.raw"] = { fg = code }
        hl["@markup.raw.block"] = { fg = code }
        hl["@markup.link.url"] = { fg = signal.s400, underline = true }
      end,
    },
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "tokyonight-night",
    },
  },
}
