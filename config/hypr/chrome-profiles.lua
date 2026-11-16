-- Color-code Chrome web app windows by profile (see ~/.local/bin/webapp-profile).
-- Web app windows get the class chrome-<site>-<Profile dir>, so the suffix
-- tells the profile apart. Bright border when focused, dim when not.
local profiles = {
  -- Personal (Default) keeps the normal Omarchy border
  { dir = "Profile_1", color = "6b8afd" }, -- Archway
  { dir = "Profile_2", color = "f9d000" }, -- CAVA
  { dir = "Profile_3", color = "008f8b" }, -- TRF (#005F5D brightened to read on dark)
}

for _, p in ipairs(profiles) do
  o.window("^chrome-.*-" .. p.dir .. "$", {
    border_color = "rgba(" .. p.color .. "ee) rgba(" .. p.color .. "66)",
  })
end
