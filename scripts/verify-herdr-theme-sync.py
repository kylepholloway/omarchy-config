#!/usr/bin/env python3
"""Exercise the desktop theme bridge using isolated homes, without touching a live app."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

repo = Path(__file__).resolve().parent.parent
hook = repo / 'config/omarchy/hooks/theme-set.d/50-herdr-desktop'
with tempfile.TemporaryDirectory(prefix='herdr-theme-sync-test-') as temp:
    home = Path(temp)
    app = home / '.config/herdr-app'
    app.mkdir(parents=True)
    settings = {'theme': 'banana-blueberry', 'font_size': 17, 'sounds': {'enabled': False}}
    (app / 'settings.json').write_text(json.dumps(settings))
    target = home / '.config/omarchy/hooks/theme-set.d'
    target.mkdir(parents=True)
    if hook.exists():
        shutil.copy2(hook, target / hook.name)
    env = {**os.environ, 'HOME': temp, 'HERDR_APP_HOME': str(app), 'OMARCHY_THEME_HEADLESS': '1', 'OMARCHY_PATH': '/usr/share/omarchy'}
    def select(name):
        destination = home / '.config/omarchy/themes' / name
        if not destination.exists():
            shutil.copytree(repo / 'config/omarchy/themes' / name, destination)
        subprocess.run(['/usr/bin/omarchy-theme-set', name], env=env, check=True, capture_output=True)
        subprocess.run(['/usr/bin/omarchy-hook', 'theme-set', name], env=env, check=True, capture_output=True)
    select('archway')
    generated = app / 'themes/omarchy.json'
    assert generated.exists(), 'Switching Omarchy to Archway must generate a Herdr Desktop theme'
    archway = json.loads(generated.read_text())
    assert archway['background'] == '#0b0e14'
    assert archway['colors']['accent'] == '#6b8afd'
    assert len(archway['ansi']) == 16
    assert json.loads((app / 'settings.json').read_text()) == {**settings, 'theme': 'omarchy'}
    select('banana-blueberry')
    banana = json.loads(generated.read_text())
    original = repo / 'config/omarchy/themes/banana-blueberry/ghostty.conf'
    import re
    ansi = {int(i): color for i, color in re.findall(r'^palette = (\d+)=(#[a-f0-9]{6})$', original.read_text(), re.M)}
    assert banana['ansi'] == [ansi[i] for i in range(16)]
    assert banana['background'] == '#191323' and banana['foreground'] == '#cccccc'
    assert banana['selection'] == '#3d2e55' and banana['cursor'] == '#e07d13'
    assert banana['colors']['accent'] == '#22e8df'
    before = generated.read_bytes()
    subprocess.run(['/usr/bin/omarchy-hook', 'theme-set', 'archway'], env=env, check=True, capture_output=True)
    assert generated.read_bytes() == before, 'A delayed Archway hook must not replace the newer Banana Blueberry theme'
    subprocess.run(['/usr/bin/omarchy-hook', 'theme-set', 'banana-blueberry'], env=env, check=True, capture_output=True)
    assert generated.read_bytes() == before, 'Reapplying the current theme must be idempotent'
    # A stock light theme verifies semantic fallback and appearance handling.
    subprocess.run(['/usr/bin/omarchy-theme-set', 'catppuccin-latte'], env=env, check=True, capture_output=True)
    subprocess.run(['/usr/bin/omarchy-hook', 'theme-set', 'catppuccin-latte'], env=env, check=True, capture_output=True)
    latte = json.loads(generated.read_text())
    assert latte['background'] == '#eff1f5' and latte['colors']['accent'] == '#1e66f5'
    # A malformed settings file must be left untouched, and must fail visibly.
    (app / 'settings.json').write_text('{broken')
    failed = subprocess.run(['bash', str(hook), 'catppuccin-latte'], env=env, capture_output=True)
    assert failed.returncode != 0
    assert (app / 'settings.json').read_text() == '{broken'
    print('Herdr bridge: Archway, exact Mac palette/cursor, preference preservation, delayed hooks, idempotence, stock light theme, invalid settings PASS')
