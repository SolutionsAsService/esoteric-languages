# Evidence for panel round R4 (WHOLE artifact, final state, after M12 and the 2f deletions). This is the last round (cap).

Repo root `D:\New folder\PrometheusIntelligence\esoteric-languages`. Built HTML in `site\`; sources in `_src\`.
All decisions and panel reports R1–R3: `_src\design\DESIGN-LOG.md`.

## Since R3
- M12: the Ook! field shows whole rows only (row height fixed; the box is cut to a multiple of the row pitch with CSS `round()`
  against the field's container height; a one-row fallback for browsers without `round()`). Measured at six sizes, 0 cut pairs:
  1024 x 768 2 rows; 1280 x 800 2 rows (12 pairs); 1440 x 900 4 rows; 375 x 812 1 row (8 pairs); 414 x 896 2 rows; at 320 x 640
  the glyph area is 0 px and only the caption shows.
- 2f deletions: an invisible rectangle in the Befunge glyph, a zero-size box-shadow rule, an unused parameter. Built output differs
  only in those places.

## Final measurements (probe `_src\design\measure.js`, all 11 pages, after the last edit)
| Check | 1280 x 800 | 375 x 812 |
|---|---|---|
| First screen: poster top / bottom / fold | 165 / 800 / 800, complete | 189 / 812 / 812, complete |
| Poster sideways scroll; fields with clipped name, figure or output | no; 0 | no; 0 |
| Ook! pairs shown / cut | 12 / 0 | 8 / 0 |
| Figures on the poster | 906 906 98 27 26 40 1 2 | same |
| Contrast minimum light / dark; pairs below 4.5 | 5.25 / 5.25; 0 | 5.25 / 5.25; 0 |
| Page overflow; targets under 24 px; one h1 per page | 0; 0; yes | 0; 0; yes |
| Smallest readable text (aria-hidden glyphs excluded, their content is text on each page) | 12 px | 12 px |
| Programs re-run by the build | outputs and 906, 906, 98, 27, 26, 40, 1 steps unchanged | |

## Screenshots
`_src\design\shots\R4\index-first-screen-1280x800.png` and `index`, `ook`, `malbolge`, `befunge`, `about` at `-1280.png`.
