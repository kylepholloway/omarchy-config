# Old School RuneScape: Bolt, RuneLite, macropad

Set up on November 17, 2026.

## Packages

All three are already in `packages/`, so `install.sh` covers them.

| Package | Source | What |
|---|---|---|
| `bolt-launcher` | AUR | Jagex account login on Linux (there is no official Jagex Launcher) |
| `runelite` | AUR | The client Bolt starts |
| `jre17-openjdk` | extra | Java for RuneLite |

To build by hand instead: `bolt-launcher` needs `cmake` and `fmt` (install with
`--asdeps`). The build takes about four minutes.

Gotchas:
- The binary is `bolt`, not `bolt-launcher`. The launcher entry already uses it.
- When Bolt starts RuneLite, it uses its own home directory. RuneLite's files are
  in `~/.local/share/bolt-launcher/.runelite/`, not in `~/.runelite/`.

## First run on a new machine

1. Open **Bolt Launcher**, sign in with the Jagex account, pick the character,
   and choose RuneLite.
2. In RuneLite, log in to the RuneLite account (info panel, the "i" icon).
3. Configuration (wrench) → **Profiles** → click **MisoHormy**. It is
   cloud-synced, so plugins and settings come down with it. Nothing about
   RuneLite settings lives in this repo.

## Macropad (Matrice Pad Classic)

A 3x4 QMK pad (Pro Micro, ATmega32U4, USB `feed:6060`). It works as a plain
keyboard, so it needs no setup on this machine. Its keymap is saved in
`docs/qmk/matrice_pad_classic/` because the original QMK checkout came from the Mac
backup in `~/restore`. The `osrs` keymap is what is flashed:

```
F1    F2    F3    F4
F5    Up    F6    F7
Left  Down  Right Esc
```

**F4 is Party ping, not a game tab.** The MisoHormy profile sets the Party
plugin's *Ping hotkey* to F4, and RuneLite takes the key before the game sees
it. This is on purpose. The pad is fine. On November 17, 2026, a key logger showed
all 12 keys sending the right codes. To use that game tab, open it by mouse or
move it to another F-key in the game's keybinding settings. Visual Ticks also
has F4 as its tick-reset key, but that plugin is off.

To re-flash (not needed now): copy `docs/qmk/matrice_pad_classic/` into a QMK
checkout under `keyboards/matrice_technologies/`, then run
`qmk flash -kb matrice_technologies/matrice_pad_classic -km osrs`. To enter the
bootloader, hold the top-left key while plugging the pad in, or press the reset
button on the back.
