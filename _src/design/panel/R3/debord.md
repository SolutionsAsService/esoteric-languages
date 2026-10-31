# R3 Critic: Provocateur (Debord)

Anchor used: Debord, The Society of the Spectacle, thesis 1 and 18 (the image replaces the thing; the spectacle is false when the picture stands for what was never done). Test: is each new image the thing itself?

Observed in the work: I ran the build. Ook! device: 106 Brainfuck commands, 106 .op spans on index.html and on ook.html, in the same order as hello.bf (string-equal); the Ook words match site/programs/hello.ook word for word (translation equals the file). The "906 steps" and "ten times the original" (1059 vs 106) hold. Malbolge: malbolge_after() calls the site's own interpreter and reads its memory after the run; the first 16 after-characters (y d 3 < ] [ b @ Z | 8 ) P _ : 4) match the page. 58 of 64 cells differ: 42 printable, 16 shown as a dot, which the page says is "a value with no printable character". No unexecuted claim is dressed as a run. "Seven of the eight programs are run by the build" counts correctly (Scratch is drawn and is called the control).

Verdict: PASS

Requested change: none

Statement of meaning: the site now shows the program itself and what the machine left of it, and says which is which.

One critic question: the page says the changes come from running, but 42 of them include data cells altered by the program's own operations as well as instructions it re-encrypted; does a reader need that split, or is "running it changes it" honest enough?
