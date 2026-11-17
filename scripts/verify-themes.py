#!/usr/bin/env python3
"""Validate installed custom themes in temporary homes; never switch the live desktop."""
from pathlib import Path
import configparser
import json
import os
import re
import shutil
import subprocess
import tempfile
import tomllib

home = Path.home()
hook = home / '.config/omarchy/hooks/theme-set.d/archway-takeover'
with tempfile.TemporaryDirectory(prefix='archway-hook-test-') as temp:
    fixture = Path(temp)
    config = fixture / '.config'
    assets = config / 'omarchy/themes/archway/takeover'
    assets.mkdir(parents=True)
    for name in ('screensaver.txt', 'about.txt', 'lazygit.yml'):
        (assets / name).write_text('Archway ' + name)
    branding = config / 'omarchy/branding'
    branding.mkdir(parents=True)
    (branding / 'screensaver.txt').write_text('my original screensaver')
    (branding / 'original-about.txt').write_text('my original About')
    (branding / 'about.txt').symlink_to('original-about.txt')
    (config / 'starship.toml').write_text('custom = "keep this module cyan"\n')
    current = fixture / '.local/state/omarchy/current/theme.name'
    current.parent.mkdir(parents=True)
    def run(theme, requested=None):
        current.write_text(theme)
        subprocess.run(['bash', str(hook), requested or theme], env={**os.environ, 'HOME': temp}, check=True)
    run('banana-blueberry')
    assert (branding / 'screensaver.txt').read_text() == 'my original screensaver'
    run('archway')
    assert (branding / 'screensaver.txt').read_text() == 'Archway screensaver.txt'
    assert 'keep this module blue' in (config / 'starship.toml').read_text()
    first_manifest = (fixture / '.local/state/omarchy/archway-takeover/manifest.json').read_bytes()
    run('archway')
    assert first_manifest == (fixture / '.local/state/omarchy/archway-takeover/manifest.json').read_bytes()
    (config / 'lazygit/config.yml').write_text('user edit while Archway is active')
    run('archway')
    assert (config / 'lazygit/config.yml').read_text() == 'user edit while Archway is active'
    run('banana-blueberry')
    assert (branding / 'screensaver.txt').read_text() == 'my original screensaver'
    assert (branding / 'about.txt').is_symlink()
    assert os.readlink(branding / 'about.txt') == 'original-about.txt'
    assert (config / 'starship.toml').read_text() == 'custom = "keep this module cyan"\n'
    assert (config / 'lazygit/config.yml').read_text() == 'user edit while Archway is active'
    assert not (config / 'fastfetch/config.jsonc').exists()
    run('banana-blueberry', 'archway')
    assert (branding / 'screensaver.txt').read_text() == 'my original screensaver'
    # A second full cycle must restore the edits retained from the first.
    run('archway')
    run('banana-blueberry')
    assert (config / 'lazygit/config.yml').read_text() == 'user edit while Archway is active'
    print('Hook: unrelated theme, activation, idempotence, user edits, symlink restoration, absent files, stale calls, second cycle PASS')

for name in ('archway', 'banana-blueberry'):
    source = home / '.config/omarchy/themes' / name
    with tempfile.TemporaryDirectory(prefix='omarchy-theme-stage-') as temp:
        fixture = Path(temp)
        target = fixture / '.config/omarchy/themes' / name
        shutil.copytree(source, target)
        env = {**os.environ, 'HOME': temp, 'OMARCHY_THEME_HEADLESS': '1', 'OMARCHY_PATH': '/usr/share/omarchy'}
        subprocess.run(['/usr/bin/omarchy-theme-set', name], env=env, check=True, capture_output=True, text=True)
        generated = fixture / '.local/state/omarchy/current/theme'
        for required in ('colors.toml', 'shell.toml', 'ghostty.conf', 'kitty.conf', 'foot.ini', 'alacritty.toml', 'btop.theme', 'helix.toml', 'hyprland.lua', 'neovim.lua', 'vscode-theme.json', 'keyboard.rgb', 'chromium.theme'):
            assert (generated / required).is_file(), (name, required)
        count = 0
        for path in generated.iterdir():
            if not path.is_file() or path.suffix in ('.png','.jpg','.py','.md'):
                continue
            if path.suffix in ('.toml', '.lua', '.json', '.yaml', '.conf', '.ini', '.css'):
                assert '{{' not in path.read_text(), (name, path.name, 'unresolved token')
            if path.suffix == '.toml':
                tomllib.loads(path.read_text()); count += 1
            if path.suffix == '.json':
                json.loads(path.read_text()); count += 1
            if path.suffix == '.lua':
                subprocess.run(['luac','-p',str(path)],check=True); count += 1
        subprocess.run(['ghostty','+validate-config','--config-file='+str(generated/'ghostty.conf')],check=True,capture_output=True,text=True)
        subprocess.run(['magick','identify','-regard-warnings',*[str(p) for p in (generated/'backgrounds').iterdir()]],check=True,capture_output=True)
        assert (fixture / '.local/state/omarchy/current/background').resolve().is_file()
        if name == 'banana-blueberry':
            ghostty=(generated/'ghostty.conf').read_text()
            palette={int(k):v for k,v in re.findall(r'^palette = (\d+)=(#[a-f0-9]{6})$',ghostty,re.M)}
            alacritty=tomllib.loads((generated/'alacritty.toml').read_text())['colors']
            kitty=dict(re.findall(r'^(\S+) (\S+)$',(generated/'kitty.conf').read_text(),re.M))
            foot=configparser.ConfigParser();foot.read(generated/'foot.ini');foot=foot['colors-dark']
            order=['black','red','green','yellow','blue','magenta','cyan','white']
            for i in range(16):
                assert alacritty['normal' if i<8 else 'bright'][order[i%8]] == palette[i]
                assert kitty['color'+str(i)] == palette[i]
                assert '#'+foot[('regular' if i<8 else 'bright')+str(i%8)] == palette[i]
            assert alacritty['cursor'] == {'text':'#ffffff','cursor':'#e07d13'}
            assert kitty['cursor']=='#e07d13' and kitty['cursor_text_color']=='#ffffff'
            assert foot['cursor']=='ffffff e07d13'
            assert {p.name for p in (generated/'backgrounds').iterdir()} == {'01-midnight-snack.png', '02-banana-moon.png', '03-fruit-frequency.png'}
            print('Banana Blueberry: exact 16 ANSI slots + cursor in all four terminals PASS')
        print(name+': isolated Omarchy build, '+str(count)+' parsed configs, Ghostty validation, wallpaper decoding PASS')
