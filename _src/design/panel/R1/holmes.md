# Critic: Inclusion (Holmes), R1

**Anchor:** Kat Holmes, Mismatch: exclusion arises from a mismatch between a person and the design. Solve for one, extend to many (permanent / temporary / situational).

**Observed (verified in site\*.html):**
- Good: Hello World programs are real text on every page (index fields repeat program text; whitespace.html spells [S][T][L] and decodes each character; Hello output in labelled `pre`). Skip link, lang="en", one h1. Piet commands are named in words (red, magenta, "1 darker"), not colour alone. Brainfuck/Befunge explain tape, pointer, stack, Turing tarpit in place.
- piet.html: the program picture is an aria-hidden SVG inside a region labelled "The Piet program", so that region is silent to a screen reader. The only equivalent is a table of "the first six" of 26 transitions. The 67 x 25 image is not otherwise available as text; the 20 other steps are lost to a blind reader (and to a colour-blind one who cannot tell the hues apart, though the table names them).
- piet.html uses "pointer switch", "dup", "roll", "push/pop", "block", but never defines a stack or the direction pointer on that page. whitespace.html heads a table "Stack / Heap / Flow control" with no gloss. These terms are explained only on other pages (brainfuck, befunge), reached by no link from the spot of use. A newcomer landing on Piet from a search hits unexplained jargon.
- Phone: poster glyphs are 47 px tall and smallest text 11 px: tiny for low-vision readers (situational: sunlight).

**Verdict: OBJECT** (two verified gaps, one change requested).

**Requested change (one):** On piet.html, add a plain-words sentence defining "stack" and "pointer" at first use (with a link to the Befunge stack explanation), and publish the full 26-row transition list as an expandable text alternative inside the "The Piet program" region (the same fix extends to whitespace's "Stack/Heap" terms).

**Statement of meaning:** Every reader gets the same program and the same explanation, whatever way they perceive the picture.

**Critic question:** If the picture vanished, could a reader still reconstruct what the Piet program does, and know what a stack is?
