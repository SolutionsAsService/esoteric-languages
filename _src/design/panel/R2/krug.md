# R2 Critic: Usability (Krug)

Anchor used: Steve Krug, "Don't Make Me Think": five-second test, trunk test, self-evident labels.

Observed in the work:
- Five-second test, first screen (index-first-screen-1280x800.png): in five seconds I can say what this is (eight ways to say Hello, World!), that each coloured field is one language, and that the big number is a count. Name, big number and "steps" sit in the same top-left slot in all eight fields, so the eye hops field to field without hunting. The arrow after every name now reads as "this goes somewhere"; my R1 request is met. Nav says Home, More, About; trunk test passes: site name, current page, and the way out are all visible.
- Added devices did not break scanning. Tape cells, Malbolge's before/after rows, the Ook! caption and the LOLCODE caption all sit below the name/number/output stack, so the scan path is untouched. They are secondary and read as texture, not as controls.
- Mild friction, not a defect: the sentence that explains the number is about 12 px and sits well under a very large H1; the "line below it" it points to is also tiny mono. Scratch's "2 blocks / control: not esoteric" changes the unit, but it is labelled in the field itself.
- Malbolge page leads with the program as scrambled text, then its explanation; the title and one-line summary come first, so it is self-evident.

Verdict: PASS.

Requested change (one): set the "Each field is a real program..." sentence one size step up so the rule for reading the numbers survives a glance; do not add anything else to the fields.

Statement of meaning: a first-time visitor knows within five seconds what a field is, what its number means, and that clicking the arrowed name opens the language.

Critic question: Debord seat, if the explanatory sentence grows, does it still read as part of the poster rather than a caption stuck on top of it?
