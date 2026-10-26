"""Build filled glyph outlines from the canonical SVG strokes, not faux-bold fonts."""
import json
from pathlib import Path
import skia
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.basePen import BasePen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

root = Path(__file__).resolve().parent.parent
icons = json.loads((root / 'icons.json').read_text())
fonts = root / 'fonts'
fonts.mkdir(exist_ok=True)
(root / 'css').mkdir(exist_ok=True)

class SkiaPen(BasePen):
    def __init__(self):
        super().__init__(None)
        self.path = skia.Path()
    def _moveTo(self, p): self.path.moveTo(*p)
    def _lineTo(self, p): self.path.lineTo(*p)
    def _curveToOne(self, a, b, c): self.path.cubicTo(*a, *b, *c)
    def _qCurveToOne(self, a, b): self.path.quadTo(*a, *b)
    def _closePath(self): self.path.close()
    def _endPath(self): pass

def glyph(data, width):
    source = SkiaPen()
    parse_path(data, source)
    paint = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=width,
                       StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    outline = skia.Path()
    paint.getFillPath(source.path, outline)
    tt = TTGlyphPen(None)
    pen = TransformPen(Cu2QuPen(tt, 0.5), (32, 0, 0, -32, 128, 896))
    iterator = iter(outline)
    for verb, pts in iterator:
        point = lambda p: (p.x(), p.y())
        if verb == skia.Path.kMove_Verb: pen.moveTo(point(pts[0]))
        elif verb == skia.Path.kLine_Verb: pen.lineTo(point(pts[1]))
        elif verb == skia.Path.kQuad_Verb: pen.qCurveTo(*map(point, pts[1:]))
        elif verb == skia.Path.kCubic_Verb: pen.curveTo(*map(point, pts[1:]))
        elif verb == skia.Path.kConic_Verb:
            quads = skia.Path.ConvertConicToQuads(*pts, iterator.conicWeight(), 2)
            for i in range(1, len(quads), 2): pen.qCurveTo(point(quads[i]), point(quads[i+1]))
        elif verb == skia.Path.kClose_Verb: pen.closePath()
    return tt.glyph()

css = []
for style, weight, stroke in [('Light', 300, 1), ('Regular', 400, 1.5), ('Bold', 700, 2.5)]:
    fb = FontBuilder(1024, isTTF=True)
    names = ['.notdef'] + list(icons)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap({int(data['codepoint'], 16): name for name, data in icons.items()})
    fb.setupGlyf({'.notdef': TTGlyphPen(None).glyph(), **{name: glyph(data['path'], stroke) for name, data in icons.items()}})
    fb.setupHorizontalMetrics({name: (1024, getattr(fb.font['glyf'][name], 'xMin', 0)) for name in names})
    fb.setupHorizontalHeader(ascent=1024, descent=0)
    fb.setupNameTable({'familyName':'PixlPrfct Icons', 'styleName':style,
                      'uniqueFontIdentifier':f'PixlPrfctIcons-{style}-0.1.0',
                      'fullName':f'PixlPrfct Icons {style}', 'psName':f'PixlPrfctIcons-{style}',
                      'version':'Version 0.1.0'})
    fb.setupOS2(sTypoAscender=1024, sTypoDescender=0, usWinAscent=1024, usWinDescent=0,
                usWeightClass=weight, fsSelection=32 if weight==700 else 64 if weight==400 else 0)
    fb.setupPost()
    fb.font['head'].macStyle = 1 if weight==700 else 0
    fb.font['head'].created = fb.font['head'].modified = 3786912000
    fb.font.recalcTimestamp=False
    filename=f'pixlprfct-icons-{style.lower()}'
    fb.save(fonts / (filename+'.ttf'))
    fb.font.flavor='woff2'
    fb.save(fonts / (filename+'.woff2'))
    check=TTFont(fonts / (filename+'.woff2'))
    assert len(check.getBestCmap()) == len(icons)
    assert all(check['glyf'][name].numberOfContours > 0 for name in icons)
    css.append(f'@font-face{{font-family:"PixlPrfct Icons";src:url("../fonts/{filename}.woff2") format("woff2");font-weight:{weight};font-style:normal;font-display:block}}')
css += ['.pxi{display:inline-block;font-family:"PixlPrfct Icons"!important;font-style:normal;font-weight:400;font-variant:normal;text-transform:none;line-height:1;font-synthesis:none;speak:none;-webkit-font-smoothing:antialiased}', '.pxi-light{font-weight:300}.pxi-regular{font-weight:400}.pxi-bold{font-weight:700}']
for name, data in icons.items(): css.append(f'.pxi-{name}::before{{content:"\\{data["codepoint"]}"}}')
(root / 'css/icons.css').write_text('\n'.join(css)+'\n')
print(f'Built and validated {len(icons)} glyphs in 3 weights (TTF + WOFF2).')
