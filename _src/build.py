"""Builds site/ for esoteric-languages.shadw.app.

Every program the site shows is written to site/programs/, run from that file
by the interpreters in _src/eso/, and checked against the figures the pages
print. The build fails if an output, a step count or an internal link drifts.
"""
import html
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / '_src'
OUT = ROOT / 'site'
sys.path.insert(0, str(SRC / 'eso'))
import langs  # noqa: E402
import malbolge  # noqa: E402
import piet  # noqa: E402
import run as runner  # noqa: E402

SITE_URL = 'https://esoteric-languages.shadw.app/'
REPO_URL = 'https://github.com/SolutionsAsService/esoteric-languages'
LANG = json.loads((SRC / 'data/languages.json').read_text(encoding='utf-8'))
RUNNABLE = [k for k in LANG if LANG[k]['file']]
PAGES = ([('index', 'Index', 'index.html')] + [(k, LANG[k]['name'], f'{k}.html') for k in LANG]
         + [('more', 'More languages', 'more.html'), ('about', 'About', 'about.html')])

# What each program printed and how many steps it took, as the pages say it.
# The build re-runs every program and stops if any of these changes.
EXPECT = {
    'brainfuck': ('Hello World!\n', 906),
    'ook': ('Hello World!\n', 906),
    'befunge': ('Hello, World!', 98),
    'whitespace': ('Hello, World!', 27),
    'piet': ('Hello, World!', 26),
    'malbolge': ('Hello World!', 40),
    'lolcode': ('Hello, World!\n', 1),
}
SCRATCH_BLOCKS = [('event', 'when ⚑ clicked'), ('looks', 'say [Hello, World!]')]


class BuildError(Exception):
    pass


def field(key):
    f = LANG[key]['field']
    return {'W': '#FFFFFF', 'K': '#000000'}.get(f) if isinstance(f, str) else '#' + piet.RGB[tuple(f)]


# ------------------------------------------------------------------ programs
PROG = {}   # key -> program text (or Piet grid)
RUN = {}    # key -> (output, steps)


def write_programs():
    d = OUT / 'programs'
    d.mkdir(parents=True, exist_ok=True)
    for f in ('hello.bf', 'hello.befunge', 'hello.mb', 'hello.lol', 'count.lol'):
        shutil.copyfile(SRC / 'programs' / f, d / f)
    bf = (SRC / 'programs/hello.bf').read_text(encoding='utf-8')
    (d / 'hello.ook').write_text(langs.bf_to_ook(bf) + '\n', encoding='utf-8', newline='\n')
    (d / 'hello.ws').write_bytes(langs.ws_print('Hello, World!').encode('ascii'))
    grid = piet.generate('Hello, World!', height=20)  # aspect fits the poster field (M9)
    piet.to_png(grid, d / 'hello-piet.png')
    if piet.from_png(d / 'hello-piet.png') != grid:
        raise BuildError('the Piet PNG does not read back as the program that was generated')
    for key in RUNNABLE:
        path = d / LANG[key]['file']
        RUN[key] = runner.run_file(path)
        if RUN[key] != EXPECT[key]:
            raise BuildError(f'{key}: {path.name} now gives {RUN[key]!r}, the pages say {EXPECT[key]!r}')
        PROG[key] = grid if key == 'piet' else path.read_bytes().decode('utf-8')
    lol2 = langs.lol_run((d / 'count.lol').read_text(encoding='utf-8'))
    if lol2 != ('O HAI 0\nO HAI 1\nO HAI 2\n', 11):
        raise BuildError(f'count.lol now gives {lol2!r}')
    RUN['lolcount'] = lol2


def size_of(key):
    if key == 'piet':
        g = PROG['piet']
        return f"{len(g[0])} × {len(g)} codels"
    if key == 'whitespace':
        return f"{len(PROG[key])} characters, all invisible"
    if key == 'befunge':
        return f"{len(PROG[key].strip())} cells"
    return f"{len(PROG[key].strip())} characters"


def shown(text):
    """An output, with its newline made visible."""
    return html.escape(text).replace('\n', '<span class="nl">↵</span>')


# ------------------------------------------------------------------ glyphs: each program drawn from itself
def befunge_visits():
    _, _, path = langs.befunge_run(PROG['befunge'])
    line = PROG['befunge'].rstrip('\n')
    return line, [sum(1 for p in path if p == (x, 0)) for x in range(len(line))]


def malbolge_after():
    """The program's cells after it has run: Malbolge rewrites each instruction as it executes (M10)."""
    mem = []
    malbolge.run(PROG['malbolge'], memory=mem)
    src = PROG['malbolge']
    after = [chr(v) if 33 <= v <= 126 else None for v in mem[:len(src)]]
    return src, after, sum(1 for a, b in zip(src, after) if a != b)


def glyph(key):
    if key == 'brainfuck':
        # the program above the bytes it leaves on the tape (M10)
        cells = ''.join(f'<span class="cell"><b>{v}</b>{html.escape(chr(v)) if 32 < v < 127 else ("↵" if v == 10 else "·")}</span>'
                        for v in langs.bf_tape(PROG[key]))
        return (f'<span class="g g-bf-wrap"><span class="g-code g-bf">{html.escape(PROG[key])}</span>'
                f'<span class="g-tape">{cells}</span></span>')
    if key == 'ook':
        # each Brainfuck command with the Ook pair that spells it, in program order (M11)
        bf = [c for c in PROG['brainfuck'] if c in langs.OOK]
        pairs = ''.join(f'<span class="op"><b>{html.escape(c)}</b>{langs.OOK[c].replace(" ", "<br>")}</span>' for c in bf)
        return f'<span class="g g-ook-pairs">{pairs}</span>'
    if key == 'malbolge':
        # as written, and the same cells after running: changed characters marked (M10)
        src, after, _ = malbolge_after()
        row = ''.join(f'<i>{html.escape(b)}</i>' if b and b != a else (html.escape(b) if b else '<i>·</i>')
                      for a, b in zip(src, after))
        return (f'<span class="g g-mb-wrap"><span class="g-code g-mb">{html.escape(src)}</span>'
                f'<span class="g-code g-mb g-mb-after">{row}</span></span>')
    if key == 'lolcode':
        return f'<p class="g g-lol">{html.escape(PROG[key].strip())}</p>'
    if key == 'befunge':
        line, visits = befunge_visits()
        n, cw, top = len(line), 20, max(visits)
        cells = []
        for i, (ch, v) in enumerate(zip(line, visits)):
            h = 4 + 52 * v / top
            cells.append(f'<rect class="bv" x="{i * cw + 2}" y="{88 - h:.1f}" width="{cw - 4}" height="{h:.1f}"/>'
                         f'<text class="bc" x="{i * cw + cw / 2}" y="22">{html.escape(ch)}</text>')
        return (f'<svg class="g g-svg g-bef" viewBox="0 0 {n * cw} 92" preserveAspectRatio="xMinYMax meet" aria-hidden="true" focusable="false">'
                f'{"".join(cells)}</svg>')
    if key == 'whitespace':
        # the program as one stream, wrapped: a bar per character, so all of it fits one field
        per, w, h = 24, 10, 12
        cls = {' ': 'ws-s', '\t': 'ws-t', '\n': 'ws-l'}
        # space: an outline; tab: solid; line feed: solid red and taller, so shape tells them apart too (M9)
        geo = {' ': (1.5, 3, w - 5, h - 6), '\t': (1, 1.5, w - 3, h - 3), '\n': (1, 0, w - 3, h)}
        bars = ''.join(f'<rect class="{cls[ch]}" x="{(i % per) * w + geo[ch][0]}" y="{(i // per) * h + geo[ch][1]}" '
                       f'width="{geo[ch][2]}" height="{geo[ch][3]}"/>' for i, ch in enumerate(PROG[key]))
        rows = -(-len(PROG[key]) // per)
        return (f'<svg class="g g-svg g-ws" viewBox="0 0 {per * w} {rows * h}" preserveAspectRatio="xMinYMax meet" '
                f'aria-hidden="true" focusable="false">{bars}</svg>')
    if key == 'piet':
        return piet.to_svg(PROG[key], codel=4, cls='g g-svg g-piet')
    if key == 'scratch':
        fills = {'event': ('#FFBF00', '#000'), 'looks': ('#9966FF', '#fff')}
        parts = []
        for i, (kind, text) in enumerate(SCRATCH_BLOCKS):
            bg, fg = fills[kind]
            y = 10 + i * 46
            shape = (f'M0 {y + 14} Q40 {y - 6} 80 {y + 14} H200 V{y + 44} H0Z' if i == 0 else
                     f'M0 {y} H16 l6 6 h12 l6 -6 H200 V{y + 36} H40 l-6 6 h-12 l-6 -6 H0Z')
            parts.append(f'<path d="{shape}" fill="{bg}" stroke="#000" stroke-width="1.5"/>'
                         f'<text x="12" y="{y + (34 if i == 0 else 24)}" fill="{fg}" class="sc">{html.escape(text)}</text>')
        return (f'<svg class="g g-svg g-sc" viewBox="-2 -2 204 104" preserveAspectRatio="xMinYMax meet" aria-hidden="true" focusable="false">'
                f'{"".join(parts)}</svg>')
    raise BuildError(key)


# ------------------------------------------------------------------ the poster (landing)
def poster():
    tiles = []
    for key in LANG:
        d = LANG[key]
        if key == 'scratch':
            fig, unit, out = str(len(SCRATCH_BLOCKS)), 'blocks', 'control: not esoteric'
        else:
            out_text, steps = RUN[key]
            fig, unit, out = f'{steps:,}', 'step' if steps == 1 else 'steps', shown(out_text)
        note = {'ook': 'the Brainfuck program, in orangutan',
                'malbolge': f'{malbolge_after()[2]} of its {len(PROG["malbolge"])} characters rewritten as it ran'}.get(key)
        tiles.append(
            f'<li class="tile t-{key}" style="--f:{field(key)};--i:{d["ink"]}">'
            f'<a href="{key}.html"><span class="t-name">{html.escape(d["name"])}<span class="t-go" aria-hidden="true"> →</span></span>'
            f'<span class="t-fig"><b>{fig}</b> {unit}</span>'
            f'<code class="t-out">{out}</code>'
            + (f'<span class="t-note">{html.escape(note)}</span>' if note else '') +
            f'<span class="t-glyph" aria-hidden="true">{glyph(key)}</span></a></li>')
    return f'<ol class="poster" aria-label="The languages on this site">{"".join(tiles)}</ol>'


# ------------------------------------------------------------------ inner-page components
def band(key):
    d = LANG[key]
    who = f'{html.escape(d["by"])}' + (f', {d["year"]}' if d['year'] else '')
    return (f'<header class="band" style="--f:{field(key)};--i:{d["ink"]}">'
            f'<div class="band-text"><p class="kicker">{"Control" if key == "scratch" else "Esoteric language"}</p>'
            f'<h1 id="top">{html.escape(d["name"])}</h1><p class="band-line">{html.escape(d["line"])}</p>'
            f'<p class="band-by">By {who}.</p></div>'
            f'<div class="band-glyph" aria-hidden="true">{glyph(key)}</div></header>')


def program_block(key):
    d = LANG[key]
    if key == 'piet':
        return (f'<figure class="prog prog-piet"><figcaption>{d["file"]} · {size_of(key)}, shown at 4 px a codel'
                f' · <a href="programs/{d["file"]}" download>download the PNG (10 px a codel)</a></figcaption>'
                f'<div class="piet-wrap" tabindex="0" role="region" aria-label="The Piet program">{glyph(key)}</div></figure>')
    text = PROG[key]
    if key == 'whitespace':
        text = text.replace(' ', '[S]').replace('\t', '[T]').replace('\n', '[L]\n')
        note = ' (S space, T tab, L line feed: the real file is invisible)'
    else:
        note = ''
    return (f'<figure class="prog"><figcaption>{d["file"]} · {size_of(key)}{note} · '
            f'<a href="programs/{d["file"]}" download>download</a></figcaption>'
            f'<pre tabindex="0" aria-label="{html.escape(d["name"])} program"><code>{html.escape(text.rstrip())}</code></pre></figure>')


def run_block(key):
    out, steps = RUN[key]
    f = LANG[key]['file']
    return (f'<figure class="term"><figcaption>run by this site’s build</figcaption><pre tabindex="0" aria-label="Output">'
            f'$ python _src/eso/run.py site/programs/{f}\n{html.escape(f"site/programs/{f}: {out!r} in {steps} steps")}'
            f'</pre></figure>')


def trace(key):
    if key == 'ook':
        return ('<p>Every pair of words turns back into one Brainfuck command, so the run is the same machine'
                f' doing the same {RUN["ook"][1]:,} steps. See <a href="brainfuck.html#how-h">how the Brainfuck version runs</a>.</p>')
    if key == 'brainfuck':
        code = [c for c in PROG['brainfuck'] if c in '<>+-.,[]']
        # stop at the first '.', and show the tape the loops built
        tape, p, ip, jump, st = [0] * 16, 0, 0, {}, []
        for i, c in enumerate(code):
            if c == '[':
                st.append(i)
            elif c == ']':
                j = st.pop()
                jump[i], jump[j] = j, i
        steps = 0
        while code[ip] != '.':
            c = code[ip]
            steps += 1
            p += (c == '>') - (c == '<')
            tape[p] = (tape[p] + (c == '+') - (c == '-')) % 256
            if (c == '[' and tape[p] == 0) or (c == ']' and tape[p] != 0):
                ip = jump[ip]
            ip += 1
        cells = ''.join(f'<li{" class=cur" if i == p else ""}><b>{v}</b><span>{html.escape(chr(v)) if 32 < v < 127 else "·"}</span></li>'
                        for i, v in enumerate(tape[:8]))
        return (f'<p>After {steps:,} steps the loops have built these values on the tape, and the pointer'
                f' (outlined) sits on {tape[p]}, which is <code>{html.escape(chr(tape[p]))}</code>. The first <code>.</code> prints it.</p>'
                f'<ol class="tape" aria-label="The first eight tape cells">{cells}</ol>')
    if key == 'befunge':
        line, visits = befunge_visits()
        rows = ''.join(f'<tr><td><code>{html.escape(c) if c != " " else "␠"}</code></td><td>{v}</td></tr>'
                       for c, v in zip(line, visits))
        return (f'<p>The bars in the band above count how often the instruction pointer passed each cell. The string'
                f' cells are passed once, pushing the letters backwards; the six cells of the print loop'
                f' <code>&gt;:#,_</code> are passed again and again, and <code>#</code> makes the pointer jump the'
                f' cell after it on the way back.</p><div class="tablewrap" tabindex="0" role="region" aria-label="Visits per cell">'
                f'<table class="visits"><thead><tr><th>Cell</th><th>Visits</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if key == 'whitespace':
        prog = langs.ws_parse(PROG[key])
        vis = lambda s: s.replace(' ', 'S').replace('\t', 'T').replace('\n', 'L')
        rows = []
        for ch in 'Hello, World!':
            enc = vis(' ' + ' ' + langs.ws_number(ord(ch))) + ' ' + vis('\t\n  ')
            rows.append(f'<tr><td><code>{html.escape(ch)}</code></td><td>push {ord(ch)}, print it</td><td><code>{enc}</code></td></tr>')
        rows.append(f'<tr><td>end</td><td>stop</td><td><code>LLL</code></td></tr>')
        return (f'<p>The program decodes to {len(prog)} instructions: a push and a print for each of the 13 characters,'
                f' then an end. Numbers are written in binary, with space for 0 and tab for 1.</p>'
                f'<div class="tablewrap" tabindex="0" role="region" aria-label="Decoded program"><table><thead><tr>'
                f'<th>Prints</th><th>Instructions</th><th>Encoding</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    if key == 'piet':
        log = []
        piet.run(PROG['piet'], log=log)
        sw = lambda c: f'<span class="sw" style="background:#{piet.RGB[c]}"></span>{piet.HUES[c[1]]}, {["light", "normal", "dark"][c[0]]}'
        row = lambda i, a, b, s, c: (f'<tr><td>{i}</td><td>{sw(a)}</td><td>{sw(b)}</td><td>{s}</td>'
                                     f'<td>{c.replace("_c", " (char)")}</td></tr>')
        head = '<thead><tr><th>Step</th><th>From</th><th>To</th><th>Block size</th><th>Command</th></tr></thead>'
        first = ''.join(row(i + 1, *t) for i, t in enumerate(log[:6]))
        every = ''.join(row(i + 1, *t) for i, t in enumerate(log))
        return (f'<p>The interpreter starts at the top-left codel and moves right. Its direction is held by the'
                f' <i>direction pointer</i>, which this program never turns. Leaving a block whose size is'
                f' the character code, with the next colour one step darker, is <i>push</i>: it puts the block’s size'
                f' on the stack. Moving on with the hue shifted five steps and the lightness two is <i>out (char)</i>:'
                f' it takes the number back off and prints it as a letter. The build generated this program and ran it'
                f' {RUN["piet"][1]} transitions to the end, where every exit is blocked. The first six:</p>'
                f'<div class="tablewrap" tabindex="0" role="region" aria-label="First six transitions"><table>{head}<tbody>{first}</tbody></table></div>'
                f'<details class="all"><summary>All {len(log)} transitions, as text</summary>'
                f'<div class="tablewrap" tabindex="0" role="region" aria-label="All transitions"><table>{head}<tbody>{every}</tbody></table></div></details>')
    if key == 'malbolge':
        log = []
        malbolge.run(PROG['malbolge'], log=log)
        rows = ''.join(f'<tr><td>{i + 1}</td><td>{c}</td><td><code>{html.escape(ch)}</code></td><td>{op}</td>'
                       f'<td>{html.escape(o) if o.strip() else ("␠" if o else "")}</td></tr>' for i, (c, ch, op, o) in enumerate(log))
        src, after, changed = malbolge_after()
        cmp = ''.join(f'<tr><td>{i}</td><td><code>{html.escape(a)}</code></td><td><code>{html.escape(b) if b else "·"}</code></td></tr>'
                      for i, (a, b) in enumerate(zip(src, after)) if a != b)
        before_after = (f'<p>Running it changes it. After the {len(log)} steps, {changed} of the program’s {len(src)} characters'
                        f' are different. Changed characters are underlined; a dot is a value with no printable character.</p>'
                        + '<div class="mb-chunks" role="group" aria-label="The program before and after, in chunks of 16 characters">'
                        + '<span class="mb-chunk mb-lab"><span>before</span><span>after</span></span>'
                        + ''.join('<span class="mb-chunk"><code>' + html.escape(src[i:i + 16]) + '</code><code>'
                                  + ''.join(f'<u>{html.escape(b)}</u>' if b and b != a else (html.escape(b) if b else '<u>·</u>')
                                            for a, b in zip(src[i:i + 16], after[i:i + 16])) + '</code></span>'
                                  for i in range(0, len(src), 16))
                        + '</div>'
                        f'<details class="all"><summary>Every changed cell, as a list</summary><div class="tablewrap" tabindex="0" role="region"'
                        f' aria-label="Changed cells"><table><thead><tr><th>Cell</th><th>Before</th><th>After</th></tr></thead>'
                        f'<tbody>{cmp}</tbody></table></div></details>')
        return before_after + (f'<p>All {len(log)} steps. The instruction is not the character itself but (character + position)'
                f' mod 94, and after each step the character is replaced through a fixed substitution table, so the'
                f' same cell means something else next time.</p><div class="tablewrap" tabindex="0" role="region" aria-label="Every step">'
                f'<table><thead><tr><th>Step</th><th>Cell</th><th>Holds</th><th>Does</th><th>Prints</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if key == 'lolcode':
        return (f'<figure class="prog"><figcaption>count.lol · <a href="programs/count.lol" download>download</a></figcaption>'
                f'<pre tabindex="0" aria-label="count.lol"><code>{html.escape(PROG_TEXT("count.lol"))}</code></pre></figure>'
                f'<figure class="term"><figcaption>run by this site’s build</figcaption><pre tabindex="0" aria-label="Output">'
                f'$ python _src/eso/run.py site/programs/count.lol\n{html.escape(repr(RUN["lolcount"][0]))} in {RUN["lolcount"][1]} steps</pre></figure>')
    raise BuildError(key)


def PROG_TEXT(name):
    return (OUT / 'programs' / name).read_text(encoding='utf-8').rstrip()


def facts_list():
    rows = ''.join(f'<tr><th scope="row"><a href="{k}.html">{html.escape(d["name"])}</a></th><td>{html.escape(d["by"])}</td>'
                   f'<td>{d["year"] or "—"}</td><td>{"—" if k == "scratch" else f"{RUN[k][1]:,}"}</td></tr>'
                   for k, d in LANG.items())
    return (f'<div class="tablewrap" tabindex="0" role="region" aria-label="All languages"><table><thead><tr><th>Language</th>'
            f'<th>Made by</th><th>Year</th><th>Steps to say hello</th></tr></thead><tbody>{rows}</tbody></table></div>')


def sources(key):
    return '<ul class="sources">' + ''.join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for t, u in LANG[key]['sources']) + '</ul>'


def pager(key):
    keys = [p[0] for p in PAGES]
    i = keys.index(key)
    prev, nxt = PAGES[i - 1], PAGES[(i + 1) % len(PAGES)]
    return (f'<nav class="pager" aria-label="Previous and next"><a href="{prev[2]}"><span>Previous</span>{html.escape(prev[1])}</a>'
            f'<a href="{nxt[2]}"><span>Next</span>{html.escape(nxt[1])}</a></nav>')


def expand(key, body):
    def sub(m):
        name, _, arg = m.group(1).strip().partition(' ')
        k = arg.strip() or key
        if name == 'poster':
            return poster()
        if name == 'band':
            return band(k)
        if name == 'program':
            return program_block(k)
        if name == 'run':
            return run_block(k)
        if name == 'steps':
            return f'{RUN[k][1]:,}'
        if name == 'output':
            return f'<code>{shown(RUN[k][0])}</code>'
        if name == 'size':
            return size_of(k)
        if name == 'trace':
            return trace(k)
        if name == 'sources':
            return sources(k)
        if name == 'facts':
            return facts_list()
        if name == 'name':
            return html.escape(LANG[k]['name'])
        if name == 'repo':
            return REPO_URL
        if name == 'pager':
            return pager(key)
        if name == 'ooktable':
            rows = ''.join(f'<tr><td><code>{langs.OOK[c]}</code></td><td><code>{html.escape(c)}</code></td></tr>' for c in '><+-.,[]')
            return ('<div class="tablewrap" tabindex="0" role="region" aria-label="Word pairs"><table><thead><tr>'
                    f'<th>Ook!</th><th>Brainfuck</th></tr></thead><tbody>{rows}</tbody></table></div>')
        if name == 'piettable':
            head = ''.join(f'<th>{l}</th>' for l in ('no change', '1 darker', '2 darker'))
            rows = ''.join(f'<tr><th scope="row">{h} hue step{"s" if h != 1 else ""}</th>'
                           + ''.join(f'<td>{c.replace("_n", " (number)").replace("_c", " (char)")}</td>' for c in row) + '</tr>'
                           for h, row in enumerate(piet.COMMANDS))
            return ('<div class="tablewrap" tabindex="0" role="region" aria-label="Piet commands"><table><thead><tr>'
                    f'<th>Hue change</th>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
        if name == 'scratchglyph':
            return glyph('scratch')
        if name == 'blocks':
            return str(len(SCRATCH_BLOCKS))
        raise BuildError(f'unknown placeholder {name}')
    return re.sub(r'\{\{(.+?)\}\}', sub, body)


# ------------------------------------------------------------------ page shell
def mark(cls='mark'):
    return (f'<svg class="{cls}" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
            f'<rect width="32" height="32" fill="#000"/><rect x="2" y="2" width="17" height="17" fill="#FF0000"/>'
            f'<rect x="21" y="2" width="9" height="9" fill="#FFFF00"/><rect x="21" y="13" width="9" height="17" fill="#fff"/>'
            f'<rect x="2" y="21" width="17" height="9" fill="#0000FF"/></svg>')


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><style>.k{fill:#000}.w{fill:#fff}'
            '@media (prefers-color-scheme: dark){.k{fill:#fff}.w{fill:#000}}</style>'
            '<rect class="k" width="32" height="32"/><rect x="2" y="2" width="17" height="17" fill="#FF0000"/>'
            '<rect x="21" y="2" width="9" height="9" fill="#FFFF00"/><rect class="w" x="21" y="13" width="9" height="17"/>'
            '<rect x="2" y="21" width="17" height="9" fill="#0000FF"/></svg>\n')


def og():
    cells, x = [], 0
    widths = [3, 2, 4, 3, 5, 3, 2, 2]
    for i, key in enumerate(LANG):
        w = widths[i] * 100
        row = i // 4
        x = sum(widths[(i // 4) * 4:i]) * 100
        name = html.escape(LANG[key]['name'])
        cells.append(f'<rect x="{x + 8}" y="{230 + row * 200 + 8}" width="{w - 16}" height="184" fill="{field(key)}"/>'
                     f'<text x="{x + 28}" y="{230 + row * 200 + 60}" font-family="Archivo, Arial, sans-serif" font-weight="900"'
                     f' font-size="34" fill="{LANG[key]["ink"]}">{name}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
            f'<rect width="1200" height="630" fill="#000"/><rect x="8" y="8" width="1184" height="214" fill="#F4F1EA"/>'
            f'<text x="40" y="110" font-family="Archivo, Arial, sans-serif" font-weight="900" font-size="78">Esoteric Languages</text>'
            f'<text x="40" y="180" font-family="Archivo, Arial, sans-serif" font-size="34">Eight ways to say Hello, World!, each one run by the site</text>'
            f'{"".join(cells)}</svg>\n')


def page_html(key, file, meta, body):
    title = meta['title'] if key == 'index' else f"{meta['title']} · Esoteric Languages"
    url = SITE_URL + ('' if file == 'index.html' else file.removesuffix('.html'))
    chips = ''
    if key != 'index':
        chips = ('<nav class="chips" aria-label="Languages"><ul>' + ''.join(
            f'<li><a href="{k}.html" style="--f:{field(k)};--i:{d["ink"]}"{" aria-current=page" if k == key else ""}>'
            f'{html.escape(d["name"])}</a></li>' for k, d in LANG.items()) + '</ul></nav>')
    top = [('index', 'Home', 'index.html'), ('more', 'More', 'more.html'), ('about', 'About', 'about.html')]
    nav = ''.join(f'<li><a href="{f}"{" aria-current=page" if k == key else ""}>{t}</a></li>' for k, t, f in top)
    ld = ''
    if key == 'index':
        ld = ('<script type="application/ld+json">' + json.dumps({
            '@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Esoteric Languages', 'url': SITE_URL,
            'description': meta['description'], 'author': {'@type': 'Organization', 'name': 'SolutionsAsService'}}) + '</script>\n')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(meta['description'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(meta['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}og.svg">
<meta name="theme-color" content="#F4F1EA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=JetBrains+Mono:wght@400;700&display=swap">
<link rel="stylesheet" href="style.css">
{ld}</head>
<body class="p-{key}">
<a class="skip" href="#main">Skip to content</a>
<header class="mast">
<a class="brand" href="index.html">{mark()}<span>Esoteric<br>Languages</span></a>
<nav class="top" aria-label="Site"><ul>{nav}</ul></nav>
</header>
{chips}
<main id="main">
{body}
</main>
<footer class="foot">
<p>Every program on this site except the two Scratch blocks was run by the site’s own build, with the interpreters in <a href="{REPO_URL}/tree/main/_src/eso">_src/eso</a>. Facts about each language link to their sources.</p>
<p>By SolutionsAsService. This site sets no cookies and collects nothing.</p>
</footer>
</body>
</html>
"""


def check_links(out):
    written = {str(p.relative_to(out)).replace('\\', '/') for p in out.rglob('*') if p.is_file()}
    bad = []
    for page in out.glob('*.html'):
        text = page.read_text(encoding='utf-8')
        ids = set(re.findall(r'\sid="([^"]+)"', text))
        for ref in re.findall(r'(?:href|src)="([^"]+)"', text):
            if re.match(r'(https?:|mailto:|data:)', ref):
                continue
            target, _, frag = ref.partition('#')
            if target and target not in written:
                bad.append(f'{page.name}: {ref}')
            if frag and not target and frag not in ids:
                bad.append(f'{page.name}: #{frag}')
    if bad:
        raise BuildError('broken internal links:\n  ' + '\n  '.join(bad))


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    write_programs()
    (OUT / 'style.css').write_text((SRC / 'style.css').read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
    (OUT / 'favicon.svg').write_text(favicon(), encoding='utf-8', newline='\n')
    (OUT / 'og.svg').write_text(og(), encoding='utf-8', newline='\n')
    for key, _, file in PAGES:
        raw = (SRC / 'pages' / f'{key}.html').read_text(encoding='utf-8')
        head, _, body = raw.partition('\n---\n')
        meta = json.loads(expand(key, head))
        (OUT / file).write_text(page_html(key, file, meta, expand(key, body)), encoding='utf-8', newline='\n')
    urls = ''.join(f"<url><loc>{SITE_URL}{'' if f == 'index.html' else f.removesuffix('.html')}</loc></url>" for _, _, f in PAGES)
    (OUT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
                                     encoding='utf-8', newline='\n')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n', encoding='utf-8', newline='\n')
    (OUT / 'vercel.json').write_text(json.dumps({'framework': None, 'installCommand': '', 'buildCommand': '',
                                                 'outputDirectory': '.', 'cleanUrls': True, 'fluid': True}, indent=2) + '\n',
                                     encoding='utf-8', newline='\n')
    check_links(OUT)
    print(f'built {len(PAGES)} pages into {OUT}')


if __name__ == '__main__':
    try:
        build()
    except BuildError as e:
        sys.exit(f'build failed: {e}')
