# Carry-forward: facts this run established by measurement

Read before Step 1 of any later run on this site. One line each: the fact, how it was measured, the move it changed.

1. **A count of whole items is not a check for cut ones.** The probe reported "21 Ook! pairs visible whole" while a third row was visibly sliced; three seats caught it in a screenshot. Measure items that intersect the box and are not contained by it. (M11 → M12)
2. **Snap a clipped flow to whole rows with a container query.** `container-type: size` on the clipping box plus `max-height: calc(round(down, 100cqh + gap, row + gap) - gap)` shows only whole rows at any size; put a plain `max-height` of one row first as the fallback for browsers without `round()`. Measured: 0 cut pairs at six viewports. (M12)
3. **A flex child ignores its own `height` in a first-screen control.** Forcing `.poster { height: 1400px }` changed nothing (it is `flex: 1`); the control had to resize the `.hero` container (bottom 1464, flagged). (probe control, R1)
4. **One sentence on the first screen can cost a phone its devices.** A three-sentence hero line took five lines at 375 x 812 and squeezed two fields' devices to nothing; one sentence of three clauses fixed it. Measure every field's device area at 375, not only the poster's bottom edge. (M7)
5. **A generated Piet program can be shaped to its frame.** The generator's block height sets the aspect (24 → 67 x 25, 2.68; 20 → 77 x 21, 3.67); choose it to match the field, then re-run it, since the step count must not change (26). (M9)
6. **Run the program from the file the site ships, then read a PNG back before trusting it.** The build writes `site/programs/*`, runs each from that file, and checks the Piet PNG decodes to the grid it drew. (M4)
7. **The Malbolge crazy operation is indexed [memory trit][accumulator trit].** The reverse order runs and prints structured garbage; the correct order prints the known Hello World programs. (interpreter, before M1)
8. **Bash heredocs in this tool eat backslashes** (`'\\n'` arrives as `'\n'`), even with a quoted delimiter; write patch scripts with the Write tool or use the Edit tool. (tooling, during M7)
9. **A seat that runs the build deletes files you placed in `site/` by hand** (the probe copy): copy the probe back after any seat runs `build.py`. (tooling, R1–R3)
