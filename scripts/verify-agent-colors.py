#!/usr/bin/env python3
"""Validate prompt and code theme integration without touching running agents."""
import json
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import tempfile
import tomllib

repo=Path(__file__).resolve().parent.parent
hook=repo/'config/omarchy/hooks/theme-set.d/60-agent-colors'
with tempfile.TemporaryDirectory(prefix='agent-colors-test-') as temp:
    home=Path(temp)
    claude=home/'.claude';claude.mkdir()
    codex=home/'.codex';codex.mkdir()
    state=home/'.local/state/omarchy/current';state.mkdir(parents=True)
    (state/'theme.name').write_text('archway')
    original={'model':'keep-model','theme':'custom:omarchy','enabledPlugins':{'prismantis@prismantis':True},'pluginConfigs':{'prismantis@prismantis':{'options':{'promptStyle':'framed','replyStyle':'off','promptBorderColor':'#3d2e55','promptTextColor':'#cccccc','promptFillColor':'#262034','bubbleLabels':'small'}}}}
    settings=claude/'settings.json';settings.write_text(json.dumps(original))
    config=codex/'config.toml';config.write_text('# keep my comment\nmodel = "keep-model"\n[tui]\nnotifications = true\nstatus_line = ["model", "context-used"]\n[tui.model_availability_nux]\n"keep-model" = 1\n')
    before=tomllib.loads(config.read_text())
    hookdir=home/'.config/omarchy/hooks/theme-set.d';hookdir.mkdir(parents=True)
    if hook.exists():shutil.copy2(hook,hookdir/hook.name)
    env={**os.environ,'HOME':temp,'CODEX_HOME':str(codex),'CLAUDE_CONFIG_DIR':str(claude)}
    def run():
        subprocess.run(['/usr/bin/omarchy-hook','theme-set','archway'],env=env,check=True,capture_output=True)
    run()
    options=json.loads(settings.read_text())['pluginConfigs']['prismantis@prismantis']['options']
    assert options['promptBorderColor']=='blue','Prismantis prompt frames must use the active terminal accent, not a fixed purple'
    assert options['promptTextColor']=='white' and options['promptFillColor']=='black'
    assert options['promptStyle']=='framed' and options['replyStyle']=='off' and options['bubbleLabels']=='small'
    after=json.loads(settings.read_text());after['pluginConfigs']['prismantis@prismantis']['options']=original['pluginConfigs']['prismantis@prismantis']['options'];assert after==original
    parsed=tomllib.loads(config.read_text());assert parsed['tui'].pop('theme')=='omarchy';assert parsed==before
    assert config.read_text().startswith('# keep my comment\n')
    theme=plistlib.loads((codex/'themes/omarchy.tmTheme').read_bytes())
    scopes={entry.get('scope'):entry['settings'] for entry in theme['settings']}
    assert scopes['codex.accent']['foreground']=='#04000000'
    assert scopes['markup.heading']['foreground']=='#04000000'
    assert scopes['markup.inserted, diff.inserted']['foreground']=='#02000000'
    assert scopes['markup.deleted, diff.deleted']['foreground']=='#01000000'
    for entry in theme['settings']:
        for key,value in entry['settings'].items():
            if key in ('foreground','background'):
                assert value[0]=='#' and len(value)==9 and value[-2:] in ('00','01')
                if value[-2:]=='00':assert int(value[1:3],16)<16
    snapshot=(settings.read_bytes(),config.read_bytes(),(codex/'themes/omarchy.tmTheme').read_bytes())
    run();assert snapshot==(settings.read_bytes(),config.read_bytes(),(codex/'themes/omarchy.tmTheme').read_bytes())
    subprocess.run(['bash',str(hook),'banana-blueberry'],env=env,check=True,capture_output=True)
    assert snapshot==(settings.read_bytes(),config.read_bytes(),(codex/'themes/omarchy.tmTheme').read_bytes())
    # Bat uses the same syntect theme parser and ANSI marker semantics as Codex.
    if shutil.which('bat'):
        source=home/'bat-source/themes';source.mkdir(parents=True)
        shutil.copy2(codex/'themes/omarchy.tmTheme',source/'omarchy.tmTheme')
        cache=home/'bat-cache'
        subprocess.run(['bat','cache','--build','--source',str(source.parent),'--target',str(cache)],check=True,capture_output=True)
        rendered=subprocess.run(['bat','--no-config','--theme=omarchy','--color=always','--style=plain','--paging=never','--language=python'],input='def hello(name):\n    return "hello" + str(42)\n',text=True,capture_output=True,check=True,env={**env,'BAT_CACHE_PATH':str(cache)})
        assert '\x1b[34mhello' in rendered.stdout and '\x1b[32m' in rendered.stdout
        assert '\x1b[38;2;' not in rendered.stdout,'Theme must use the active ANSI palette rather than fixed RGB'
    # Invalid configs fail without overwriting either agent's settings.
    config.write_text('[tui\nbroken')
    failed=subprocess.run(['bash',str(hook),'archway'],env=env,capture_output=True)
    assert failed.returncode!=0 and config.read_text()=='[tui\nbroken'
    print('Agent colors: palette-backed Prismantis prompts and Codex scopes, preserved settings/comments, idempotence, invalid config protection PASS')
