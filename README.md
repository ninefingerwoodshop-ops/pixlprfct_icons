# PixlPrfct Icons

Free, open-source interface icons in **Light, Regular, and Bold**, licensed under MIT. The library contains 226 icons for rich-text editing, forms, navigation, files, media, commerce, charts, developer tools, and the PixlPrfct editor. All original icon names and codepoints remain stable.

The `pixlprfct` brand symbol uses a full-height vertical pill on the left, a diamond at the top-right, and a circle at the bottom-right—no lettermark. Use `pxi-pixlprfct` in any of the three weights. The gallery favicon uses the same symbol.

[Browse and download the icons](https://ninefingerwoodshop-ops.github.io/pixlprfct_icons/)

## Use the font

Download the font package from the gallery and keep the `css` and `fonts` folders together. No npm publication is available yet.

```html
<link rel="stylesheet" href="css/icons.css">
<i class="pxi pxi-asterisk pxi-regular" aria-hidden="true"></i>
<i class="pxi pxi-search pxi-light" aria-hidden="true"></i>
<i class="pxi pxi-plus pxi-bold" aria-hidden="true"></i>
```

Use `font-size` and `color` to style an icon. Include visible text or an accessible label on its containing button; decorative icons should be hidden from screen readers. The icon font uses private-use codepoints, not text characters.

Each weight has WOFF2 for the web and TTF for design software. Weights are actual outlined glyphs, not synthetic bolding. The gallery can also download individual SVGs in all three weights.

## Develop

`icons.json` is the canonical source: each name has an SVG path on a 24×24 grid and a permanent private-use codepoint. Never reassign an existing codepoint, even if an icon is retired. Append new codepoints when adding icons.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r scripts/requirements.txt
npm run build
npm test
npm run build:site
python3 -m http.server --directory _site 8080
```

Build output includes three TTFs, three WOFF2s and `css/icons.css`. The site build creates `_site`, including a ZIP of the complete font package. `npm pack` can build a local npm archive; this repository does not automatically publish to npm.

## Contribute

Use a branch and pull request. Keep icon names stable, use rounded stroke caps/joins, and check each icon in all three weights. Run the build and tests before submitting. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — free for personal and commercial use, modification, and redistribution. Keep the license with redistributed copies.
