Critic: Inclusion (Mace), R2.

Anchor used: Principle 4 Perceptible Information (redundant presentation, legibility) and Principle 2 Flexibility in Use / Principle 5 Tolerance for Error (focus visible, keyboard reachable). Named check: focus visibility.

Observed in the work:
- Both `<summary>` elements (piet.html "All 26 transitions, as text", malbolge.html "Every changed cell, as a list") are native, so keyboard-reachable; `details.all summary` has min-height 24px plus .2rem padding. The global `:focus-visible` (style.css line 18) draws a 4px ink outline, offset 3px, on paper/ink tokens, so it shows in light and dark. The tablewrap inside has tabindex=0, role=region and a label.
- Whitespace bars: space = outline (ws-s), tab = solid (ws-t), line feed = taller and red; the shape carries the meaning, so colour is redundant.
- Malbolge changed characters use white background plus red text against the unchanged ones. This is a colour-only mark in the glyph itself, but the caption gives the count ("58 of its 64 characters rewritten") and the details list gives every changed cell as text, so the information is available another way.
- LOLCODE stroke text: white fill, black stroke and shadow, high contrast; it does not rely on colour. The arrows in field names are redundant with the text.
- Reduced motion: the only transition (a filter on tile hover) sits inside `prefers-reduced-motion: no-preference`; details adds no animation. Evidence reports overflow 0 and targets under 24px at 0 for both widths.
- Minor: the summary has no custom marker styling, so it keeps the browser's default disclosure triangle (not checked in a rendered screenshot).

Verdict: PASS. No verified barrier.

Requested change (one): Mark changed Malbolge cells with a non-colour cue (for example an underline), so the mark survives forced-colours or greyscale modes.

Statement of meaning: Everything new can be reached by keyboard, seen in focus, and understood without colour.

Critic question: When a Malbolge character changes to one that looks like its neighbour, does a reader without colour vision get anything from the glyph alone, or only from the list below it?
