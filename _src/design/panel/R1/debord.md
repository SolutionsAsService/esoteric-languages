# Critic: Provocateur (Debord), R1

Anchor used: Debord, Society of the Spectacle, thesis 1/4: what was directly lived becomes representation; the image mediates. Test: does the poster show a thing done, or a picture of the claim "done"?

Observed in the work:
- site/index.html lead: "Each field is a real program in that language, run by this site." The Scratch field is not run: it shows "2 blocks", and site/about.html says "Not run; the poster counts blocks". Meta description and JSON-LD: "Every program shown is run by the site's own build." Same overreach. (Verified; the other seven do reproduce: hello.bf 906, hello.mb 40, hello.lol 1 via run.py.)
- index prose: "Brainfuck needs 906 steps to print one line; LOLCODE ... needs 1." about.html line 60 admits "step sizes differ from one language to the next" and LOLCODE excludes HAI/KTHXBYE. The home page, where the big numbers are the image, gives the comparison with no such caveat. The number as spectacle: a commensurable-looking figure whose unit is defined elsewhere.
- Credit: the poster's programs, outputs and counts are real and rebuilt by the build, which fails on drift. That is the opposite of spectacle; it is the site's strength.

Verdict: OBJECT (concrete: a printed claim the site itself contradicts).

Requested change: on index.html, the lead sentence, meta description and JSON-LD description should say "seven of the eight fields are run by this site; Scratch, the control, is drawn, not run", and the 906-vs-1 sentence should carry "(a step is a different size in each language; see how steps are counted)" with the link.

Statement of meaning: a poster of real, reproducible Hello Worlds, honest in its programs but tidier in its headline than in its footnotes.

Critic question: if the big number cannot be compared across fields, why is it the loudest thing in every field?
