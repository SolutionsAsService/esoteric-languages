# R1 Critic: Inclusion (Mace)

**Anchor used:** Mace et al., Principles of Universal Design: 4 Perceptible Information, 5 Tolerance for Error, 2 Flexibility in Use, 3 Simple and Intuitive Use. Named check: focus visibility.

**Observed in the work:**
- Focus rings: site-wide `:focus-visible` is 4px solid `--ink` (black in light, #F4F1EA in dark) on `--paper`, so it matches the surface in both schemes. Poster fields, chips and pager links draw the ring inset (-10px, -8px, -8px) in the field's own `--i` over its own `--f`. That is the same pair as the text, measured at 5.25:1 or better, and an inset ring is not clipped by the field's `overflow:hidden`. The Piet field and chip (white ink on black) and the pager (dark mode, ink on #0d0d0d) are covered too.
- Skip link is the first link, offscreen until focus, then shown at 8px/8px in `--ink` on `--paper` with a 3px ring gap. `main` has `id="main"`.
- Wide tables, code blocks and the Piet image wrapper carry `tabindex="0"`, a `role="region"` and an `aria-label`. They scroll by keyboard and show the global ring.
- Reduced motion: the only motion is a 0.15s filter transition, wrapped in `no-preference`.
- Colour alone: the Whitespace glyph (faint, black and red bars) is `aria-hidden` and decorative, but the page prose explains the encoding. Faint vs solid differs by lightness; black vs red does not. Piet swatches always sit beside text labels ("red, dark").
- Targets: 0 under 24px, per the measured evidence.

**Verdict:** PASS

**Requested change (non-blocking):** Add a short text legend or key under the Whitespace band, or a visible link to the downloadable `.ws` file, so the black/red distinction does not rely on hue. Optionally add `scroll-padding-top` and `:focus-visible` on `main`.

**Statement of meaning:** Every interactive element can be seen and reached from the keyboard in both schemes, and nothing needed is carried by colour alone.

**Critic question:** Does any future inner page place a focusable element on a `--f` field whose `--i` ink contrasts less than 3:1 against it?
