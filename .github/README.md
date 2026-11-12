# Esoteric Languages

A static site explaining esoteric programming languages: Brainfuck, Ook!, Befunge, Whitespace, Piet, Malbolge, LOLCODE, Chef, Shakespeare, Unlambda, FALSE, INTERCAL and Rockstar, with Scratch and HolyC as controls. Every program it shows is run by the site's own build, except Scratch's blocks (drawn) and the HolyC programs, which were run in TempleOS under QEMU and are checked against that record (`_src/design/templeos/`).

- Live address: https://esoteric-languages.shadw.app/
- Built site: `site/` (committed). Source and generator: `_src/` (`python _src/build.py`).
- Interpreters: `_src/eso/`. Reproduce any figure: `python _src/eso/run.py site/programs/hello.bf`
- Design record: `_src/design/DESIGN-LOG.md`

By SolutionsAsService.
