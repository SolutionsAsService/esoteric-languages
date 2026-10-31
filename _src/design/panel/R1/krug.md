# Critic: Usability (Krug), R1

**Anchor used:** Steve Krug, Don't Make Me Think: five-second test, trunk test, self-evident labels.

**Observed in the work**
- Five-second test (first screen only): site ID "Esoteric Languages" with logo top left; h1 "Eight ways to say Hello, World!"; Brainfuck, Ook!, Befunge, Whitespace, Piet, Malbolge, LOLCODE, Scratch all named in big type. The big numbers are explained in the intro: "how many steps it took to print the line below it". A newcomer passes name, three topics and number meaning.
- Where to click: the fields are links (index.html line 33, `<a href="brainfuck.html">`) but nothing says so: no arrow, no "open", no hover cue visible, and the intro never says "click". Scratch breaks the "steps" pattern (2 blocks, "control: not esoteric") under a headline that promises eight; it is explained only in small 12 px text.
- Trunk test, befunge.html: site ID, current page (h1 Befunge, kicker "Esoteric language"), local chip row with Befunge marked current (aria-current, underlined), top nav, Previous/Next footer. Complete and self-evident. More shows the same chips with no chip current, and its Previous/Next (Scratch / About) chain works.
- Label: top nav says "Index" for the home page; "Home" is what people expect.

**Verdict:** PASS. Findings are mild friction, not a verified blocker; the poster is large and plainly the content.

**Requested change (one):** add one sentence to the home intro: "Click a field to see the program, how it runs and its sources." (Optionally rename nav "Index" to "Home".) No spectacle is added or removed.

**Statement of meaning:** A newcomer sees what the site is, what the numbers mean, and how to move between pages without thinking, except that the invitation to click is unstated.

**Critic question:** Does the Debord seat accept that a plain text cue is added to the intro, given the poster must stay the loudest thing on the first screen?
