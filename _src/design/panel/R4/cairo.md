Critic: Evidence (Cairo), R4

Anchor used: Cairo, How Charts Lie, "Charts can lie by showing insufficient evidence": a figure must be reproducible and its denominator stated.

Observed in the work: I ran `python _src/build.py` (11 pages) and `run.py` on the 7 programs. Outputs and steps are 906, 906, 98, 27, 26, 40, 1. All match the site's figures and the evidence. I recomputed the other printed figures:
- Brainfuck is 106 bytes, and Ook! is 1060 bytes including a trailing newline, shown as 1059 characters. That is 9.99x, so "ten times" holds.
- hello.mb is 64 characters.
- The Piet PNG is 770x210 px at 10 px a codel, which is 77x21 codels.
- Whitespace has 13x2+1 = 27 instructions.
- The Befunge line has 21 cells.
- The LOLCODE program is 39 characters; the file is 40 with the newline.
- The Malbolge "58 of 64 changed" and Brainfuck "851 steps" figures are computed by build.py.

The stale "21 pairs" is gone from site and _src. The R4 evidence and the DESIGN-LOG M12 "Measured after" entry agree: 12 pairs and 0 cut at 1280, 8 and 0 at 375. I did not re-render those pair counts in a browser. They come from the measure.js probe, which is present.

Verdict: PASS

Requested change: none

Statement of meaning: every printed number reproduces from the run, and the stale one is retired.

Critic question: should the reader be told that the 12 pairs shown at 1280 are 12 of 106?
