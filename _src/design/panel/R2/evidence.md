# Evidence for panel round R2 (WHOLE artifact, after moves M7–M10)

Artifact: the Esoteric Languages website, 11 pages, repo root `D:\New folder\PrometheusIntelligence\esoteric-languages`.
Built HTML in `site\`; sources `_src\pages\*.html`, `_src\style.css`, `_src\build.py`; interpreters `_src\eso\`.
Decision records and the R1 panel report: `_src\design\DESIGN-LOG.md`.

## What changed since R1
- M7 (Debord, Cairo, Krug, Fletcher): the first-screen sentence now reads "Each field is a real program; the number is the steps it took
  to print the line below it. Seven were run by this site, Scratch is drawn. Steps differ by language: costs, not a ranking."
  Every field name has an arrow (→). The Ook! field is captioned "the Brainfuck program, in orangutan". Meta description, JSON-LD
  and footer say seven of eight were run and Scratch is drawn. The home "906 … 1" sentence links "what counts as a step". About now
  says the counts are not comparable and that three programs print "Hello World!" without the comma. Nav "Index" is now "Home".
  The Ook! page's Discworld sentence is one clause.
- M8 (Holmes): piet.html and whitespace.html define "stack" (and Whitespace's "heap"; Piet's direction pointer) at first use;
  piet.html lists all 26 transitions as a text table in a `<details>` after the first six.
- M9 (Arnheim, Mace): the Piet program is generated 20 codels tall (77 x 21) so it fills its field: 490 of 490 px wide at 1280
  (it stopped at about 360 before); the build re-ran it: 26 steps, "Hello, World!". Whitespace bars differ by shape as well as
  hue (space: outline; tab: solid; line feed: taller, red).
- M10 (S4 ambition push of the poster; Shklovsky): Brainfuck's field shows the program above the tape it leaves (computed:
  0 0 72 100 87 33 10 0, i.e. H d W ! and a line feed); Malbolge's shows the program as written above the same cells after it ran,
  changed characters marked, captioned "58 of its 64 characters rewritten as it ran" (computed by the build); LOLCODE is set as a
  lolcat caption. Plain-program-text fields: 4 before, 0 after (counted by class). Malbolge's page shows the before and after too.
- Declined: a different form for "How it runs" on every inner page (kept one template, M6); see the log.

## Measurements (probe `_src\design\measure.js`, all 11 pages, after the last edit)
| Check | 1280 x 800 | 375 x 812 |
|---|---|---|
| First screen: poster bottom / fold | 800 / 800, complete | 812 / 812, complete |
| Poster scrolls sideways; fields with clipped name, figure or output | no; 0 | no; 0 |
| Text contrast minimum, light and dark; pairs below 4.5 | 5.25; 0 | 5.25; 0 |
| Page sideways overflow (all pages, both schemes) | 0 | 0 |
| Targets under 24 px | 0 | 0 |
| Smallest text | 12 px | 11 px (poster output lines and notes) |
| Programs re-run by the build | 7, outputs and steps unchanged (906, 906, 98, 27, 26, 40, 1) | |

## Screenshots
`_src\design\shots\R2\index-first-screen-1280x800.png` (the first screen exactly) and `<page>-1280.png` for index, brainfuck, ook,
whitespace, piet, malbolge, lolcode, about. Phone screens are not captured as files (headless Chrome lays out wider than a phone);
the phone layout is given by the measurements above and was inspected live at 375 x 812: all eight field devices visible.
