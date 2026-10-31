# Evidence for panel round R1 (WHOLE artifact, after moves M1–M6)

Artifact: the Esoteric Languages website, 11 pages, built by `D:\New folder\PrometheusIntelligence\esoteric-languages\_src\build.py`
into `...\esoteric-languages\site\`. Page sources: `_src\pages\*.html`; CSS `_src\style.css`; facts `_src\data\languages.json`;
interpreters `_src\eso\*.py`. Read the built HTML in `site\` for exact text. Decision records: `_src\design\DESIGN-LOG.md`.

## The concept in one line
A Mondrian grid of black bars, coloured with the Piet specification's colours. The home page's first screen is a poster with one
field per language page, each showing that language's real Hello World program as its image, the language name, and the number
of steps the program took. Inner pages share one template: a coloured band, What it is, the instructions, Hello World (program,
download, run output), How it runs (a generated trace), Sources.

## Programs and figures (all run by the build from the shipped files in `site\programs\`; build fails on drift)
| Language | Output (verbatim) | Steps | Reproduce |
|---|---|---|---|
| Brainfuck | `Hello World!\n` | 906 | `python _src/eso/run.py site/programs/hello.bf` |
| Ook! | `Hello World!\n` | 906 | `... hello.ook` |
| Befunge-93 | `Hello, World!` | 98 | `... hello.befunge` |
| Whitespace (generated) | `Hello, World!` | 27 | `... hello.ws` |
| Piet (generated; PNG read back) | `Hello, World!` | 26 | `... hello-piet.png` |
| Malbolge | `Hello World!` | 40 | `... hello.mb` |
| LOLCODE | `Hello, World!\n` | 1 | `... hello.lol` |
| Scratch (control) | not run: 2 blocks drawn | — | — |

## Measurements (in-browser probe `_src\design\measure.js`, all 11 pages, 1280 x 800 and 375 x 812, light and dark)
| Check | Result |
|---|---|
| First screen rule, home: poster bottom edge vs fold | 1280 x 800: bottom 800, fold 800, complete. 375 x 812: bottom 812, fold 812, complete |
| Poster scrolls sideways inside its box | no, at both sizes |
| Poster fields with clipped name, figure or output text | none, at both sizes |
| Glyph area per field | 157 px tall at 1280; 47 px at 375 |
| Text contrast minimum, light and dark | 5.25 (black on Piet red #FF0000), 0 pairs below 4.5 |
| Page sideways overflow | 0 on all pages, both widths, both schemes |
| Targets under 24 px | 0 |
| Smallest text | 12 px (output lines in fields); 11 px on the phone poster |
| One h1 per page | yes |
| Probe controls | a planted 1.92:1 text, a 10 px link and a poster pushed to 1464 px were each flagged, so the checks can fail |
Excluded from contrast and said so: glyphs (the programs drawn in each field) are `aria-hidden` decoration; their text is
repeated in full on each language page.

## Screenshots (headless Chrome, 1280 wide; full page)
`...\_src\design\shots\R1\index-first-screen-1280x800.png` (the first screen exactly), and `<page>-1280.png` for all 11 pages.
Headless Chrome cannot show a true phone; the phone layout is given by the measurements above.
