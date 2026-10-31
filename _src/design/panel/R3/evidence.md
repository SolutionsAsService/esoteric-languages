# Evidence for panel round R3 (WHOLE artifact, after move M11)

Repo root `D:\New folder\PrometheusIntelligence\esoteric-languages`. Built HTML in `site\`; sources in `_src\`.
Decision records and panel reports R1–R2: `_src\design\DESIGN-LOG.md`. R2 had 8 PASS and no OBJECT; M11 adopted its requests.

## What M11 changed
- Malbolge field and page: changed characters are underlined with a light tint (were solid white with red text) — Arnheim, Mace.
- Ook! field: the program's Brainfuck commands, each with the Ook pair that spells it set beneath, in program order, from the
  first command (computed from hello.bf) — Shklovsky. 21 pairs visible whole at 1280, 8 at 375.
- Malbolge page: before and after shown as aligned 16-character chunks that wrap (was one scrolling line): no sideways scroll
  (scrollWidth = clientWidth: 578/578 at 1280, 328/328 at 375) — Fletcher. Note on the page: "Changed characters are underlined".
- Hero sentence one size up (14–19 px; 14 px on phones) — Krug. Phone outputs and notes 12 px (were 11) — Holmes.
- Declined: Debord's optional "2 blocks in a different kind" (the label already says blocks and "control: not esoteric").

## Measurements (probe `_src\design\measure.js`, all 11 pages, after the last edit)
| Check | 1280 x 800 | 375 x 812 |
|---|---|---|
| First screen: poster bottom / fold | 800 / 800, complete | 812 / 812, complete |
| Fields with clipped name, figure or output; poster sideways scroll | 0; no | 0; no |
| Contrast minimum light / dark; pairs below 4.5 | 5.25 / 5.25; 0 | 5.25 / 5.25; 0 |
| Page sideways overflow; targets under 24 px | 0; 0 | 0; 0 |
| Smallest text | 12 px | 12 px (was 11) |
| One h1 per page | yes | yes |
| Programs re-run by the build | 906, 906, 98, 27, 26, 40, 1 steps; outputs unchanged | |

## Screenshots
`_src\design\shots\R3\index-first-screen-1280x800.png`, and `index`, `ook`, `malbolge`, `piet`, `scratch` at `-1280.png`.
