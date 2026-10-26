import json, re
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
