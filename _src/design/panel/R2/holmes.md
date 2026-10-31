# Critic: Inclusion (Holmes), R2

**Anchor:** Kat Holmes, Mismatch: exclusion is a mismatch between a person and the design; solve for one, extend to many (permanent / temporary / situational).

**Observed in the work (verified in site\*.html and _src\style.css):**
- R1 fixed. piet.html now defines "stack" at first use (line 36) and has a `<details>` "All 26 transitions, as text" with 27 `<tr>` (header plus 26), in a labelled, focusable region. whitespace.html defines "stack" and "heap" at first use and links Befunge.
- Poster glyphs are aria-hidden, but each has a text twin: Malbolge's field carries a real-text note "58 of its 64 characters rewritten as it ran"; malbolge.html "How it runs" gives before and after strings plus a full cell-by-cell changed list. Brainfuck page has the tape as a labelled region ("first eight tape cells") with the pointer explained in words. lolcode.html holds the program (HAI 1.2 appears 4 times). Each field also has real-text name, step count and output.
- Malbolge changed characters: white background plus red text (style.css line 88), a luminance difference, not hue alone; the page list duplicates it. No colour-only meaning.
- LOLCODE white-on-magenta with 1.2 px black stroke: outline gives contrast independent of the magenta; text is the real program. Contrast probe reports a 5.25 minimum.
- Phone: the smallest text is 11 px (output, note, tape cell). That is small for sunlight or low vision, but it is repeated at normal size on each language page, and nothing is unique to the poster. The 7 px Ook glyph is decoration only (aria-hidden, content on ook.html).

**Verdict: PASS.** I found no concrete, verified exclusion; the glyph devices never carry information absent from text.

**Requested change (one):** None required. Optional: raise the phone `.t-note` and `.t-out` from 11 px to 12 px, matching the desktop minimum.

**Statement of meaning:** Whatever way you perceive the poster, the same eight languages, counts and outputs reach you, and the pictures only add to them.

**Critic question:** If a reader on a small phone in sunlight cannot read 11 px, does the first screen still tell them, in one tap, what each language does?
