# Contributing

1. Open an issue for a new icon or design change, or submit a focused pull request.
2. Edit `icons.json`. Use a 24×24 view box with SVG path commands, and assign a new unused private-use codepoint. Preserve existing names and codepoints.
3. Install the pinned dependencies in `scripts/requirements.txt`, then run `npm run build`, `npm test`, and `npm run build:site`.
4. Inspect Light, Regular, and Bold in the gallery. Keep strokes readable at 16–24px.
5. Commit the generated fonts and CSS alongside the source update.

Only contribute artwork you created or have permission to redistribute under MIT. By contributing, you agree to license your contribution under this repository's MIT license.

The default branch requires a pull request and the **Validate icon package** check. Force pushes and deletion are disabled. Maintainers should keep releases versioned and codepoints stable.
