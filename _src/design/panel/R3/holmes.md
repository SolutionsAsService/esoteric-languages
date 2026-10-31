# R3 Critic: Inclusion (Holmes)

**Anchor used:** Holmes, "Mismatch": solve for one, extend to many (permanent, temporary, situational limits; recognize exclusion).

**Observed in the work:**
- Ook! field: the tile's pairs are inside `t-glyph aria-hidden="true"`; the tile keeps a text note ("the Brainfuck program, in orangutan"). ook.html carries the same content as real text: the mapping table (`<code>Ook. Ook?</code>` to `>`) and the program in `<pre>` (Ook. runs). Decoration here, equivalent text there: no screen-reader loss.
- Malbolge: `role="group"` with a descriptive aria-label; changes are `<u>` (58 on the page) with 2 px underline, so the signal is not colour alone; the page states "Changed characters are underlined". Good.
- Mismatch, verified in CSS: `.g-ook-pairs .op` is 9 px (6 px on phones, line 175) and `.g-ook` 9 px (7 px on phones). evidence.md says smallest text is 12 px; the probe evidently skips aria-hidden glyphs. The bold command above each pair is 15 px (10 px on phones), so the field is still readable at command level; the pair under it is situationally unreadable (glare, low vision) but duplicated in text.

**Verdict:** PASS. No exclusion verified, because the content is not lost.

**Requested change:** none. (Optional: say in the log that the 12 px floor excludes decorative aria-hidden fields.)

**Statement of meaning:** What the field shows is also written plainly on the page, so a reader who cannot see 6 px type is not locked out.

**Critic question:** If the 6 px pair labels exist only as texture on a phone, why keep them at that size instead of dropping them at 375 px and leaving the 10 px commands?
