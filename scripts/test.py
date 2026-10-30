import json, re, subprocess, sys, hashlib
from pathlib import Path
from fontTools.ttLib import TTFont
root=Path(__file__).resolve().parent.parent
icons=json.loads((root/'icons.json').read_text())
points=[int(icon['codepoint'],16) for icon in icons.values()]
assert len(set(points))==len(points)
assert all(0xe000<=point<=0xf8ff for point in points)
for name,icon in icons.items():
    assert re.fullmatch(r'[a-z][a-z0-9-]*',name)
    assert re.fullmatch(r'[MmZzLlHhVvCcSsQqTtAaEe0-9.,+\-\s]+',icon['path'])
for style,weight in [('light',300),('regular',400),('bold',700)]:
    for extension in ['ttf','woff2']:
        font=TTFont(root/f'fonts/pixlprfct-icons-{style}.{extension}')
        assert font['OS/2'].usWeightClass==weight
        assert set(font.getBestCmap())==set(points)
        assert all(font['glyf'][name].numberOfContours>0 for name in icons)
css=(root/'css/icons.css').read_text()
assert all(f'.pxi-{name}::before' in css for name in icons)
print(f'Validated {len(icons)} permanent codepoints, 6 fonts, and all CSS classes.')

# Rounded conic strokes must use the active iterator weight on every build.
outputs=list((root/"fonts").glob("*"))+[root/"css/icons.css"]
before={p:hashlib.sha256(p.read_bytes()).digest() for p in outputs}
subprocess.run([sys.executable,str(root/"scripts/build.py")],check=True)
assert before=={p:hashlib.sha256(p.read_bytes()).digest() for p in outputs}, "Font rebuild changed glyph outlines"
print("Verified byte-identical font and CSS rebuilds.")

# The recorded Territory Track inventory must resolve without generic fallbacks.
coverage=json.loads((root/'territory-track.json').read_text())
seen=set()
for ref in coverage['references']:
    key=(ref['group'],ref['name'])
    assert key not in seen, f"Duplicate mapping {key}"
    seen.add(key)
    assert ref['target'] in icons, f"Missing icon for {key}"
    assert ref['name'] in icons[ref['target']].get('keywords',[]), f"Unsearchable {key}"
    assert ref['uses'], f"No source evidence for {key}"
assert {r['group'] for r in coverage['references']} == {'web','lucide','avatar','custom','ios'}
print(f"Validated {len(seen)} Territory Track mappings without fallback icons.")

from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path
for name,data in icons.items():
    if not data.get('introducedIn'): continue
    pen=BoundsPen(None)
    parse_path(data['path'],pen)
    assert pen.bounds and min(pen.bounds)>=0 and max(pen.bounds)<=24, (name,pen.bounds)
print("Verified introduced icon paths remain inside their 24×24 viewboxes.")
