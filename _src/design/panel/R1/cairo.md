# Critic: Evidence (Cairo), R1

**Anchor used:** Cairo, How Charts Lie: a chart is truthful only if its figures are reproducible and the encoding does not invite a false comparison; "show the units, show what was not controlled".

**Observed in the work**
- Reran `python _src/build.py` (11 pages, no drift) and `_src/eso/run.py` on all 7 programs: 906, 906, 98, 27, 26, 40, 1 steps, outputs as stated. Every number on index.html (poster and table) and in the about.html table matches. Scratch "2 blocks" is drawn, not run, and labelled so. Figures are true and reproducible.
- Read step counters in `_src/eso/*.py`. BF/Ook: every command incl. `[` `]` each count 1 (about says "a jump counts once", fits). Befunge: every cell executed, spaces and `"` included. Whitespace: every decoded instruction. Piet: counts only colour-block moves; white slides and blocked retries are uncounted. Malbolge: every instruction. LOLCODE: one statement per step. Definitions on about.html match the code.
- The defect is encoding. Steps are different units: one BF command vs one whole LOLCODE statement (1 step prints 13 chars) vs one Piet block move. The poster sets them as one big number in one slot, and the intro says only "how many steps". The first screen carries no caveat, and "step sizes differ" appears only on about.html, behind a link. The about wording "compare how much work each program does" also contradicts itself. The home intro ("906 steps; LOLCODE needs 1") invites a ranking.
- Uncontrolled: BF/Ook print "Hello World!" (12 chars, no comma), others "Hello, World!" (13). Scratch's "2 blocks" sits in the same big-number slot as steps (unit labelled, but still same weight).

**Verdict: OBJECT** (verified: the cross-language comparison is not caveated where it is shown; the numbers themselves are all true).

**Requested change (one):** Put on the poster, beside the intro line, one sentence: "Steps are counted differently in each language, so these are not a ranking", and rewrite the about.html sentence to say counts are not comparable across languages.

**Statement of meaning:** Each number is an honest count of its own language's steps, and the page should say they are not a league table.

**Critic question:** If a reader remembers only "LOLCODE 1, Brainfuck 906", what false belief do they leave with?
