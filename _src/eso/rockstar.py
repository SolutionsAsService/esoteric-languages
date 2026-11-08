"""Rockstar (Dylan Beattie, 2018): programs written as power-ballad lyrics.

A reference interpreter for the part of Rockstar this site uses. run() returns
(output, steps); a step is one statement executed (a loop's condition counts
each time it is tested).

Supported: Shout/Say/Whisper/Scream, "Put x into y", poetic number literals
("Tommy was a lean mean wrecking machine"), poetic strings ("Tommy says ..."),
Build x up and Knock x down, plus and minus and times and over, comparisons
(is less than, is greater than), and While/Until loops that end at a blank line.
"""
import re


class RockstarError(ValueError):
    pass


VAR = r"(?:(?:[Aa]|[Aa]n|[Tt]he|[Mm]y|[Yy]our|[Oo]ur) [a-z]+|[A-Z][A-Za-z]*(?: [A-Z][A-Za-z]*)*|[a-z]+)"
LITERALS = {'nothing': 0, 'nowhere': 0, 'nobody': 0, 'empty': 0, 'gone': 0, 'right': True, 'yes': True, 'ok': True,
            'true': True, 'wrong': False, 'no': False, 'lies': False, 'false': False, 'null': None}


def poetic(words):
    digits = ''
    for w in words:
        if w == '.' or '.' in w and w.replace('.', '') == '':
            digits += '.'
            continue
        digits += str(len(re.sub(r"[^A-Za-z]", '', w.replace("'", ''))) % 10)
    return float(digits) if '.' in digits else int(digits)


def parse(src):
    lines = [l.rstrip() for l in src.split('\n')]
    pos = 0

    def block():
        nonlocal pos
        out = []
        while pos < len(lines):
            line = lines[pos].strip()
            pos += 1
            if not line:
                if out:
                    return out
                continue
            if re.match(r'(While|Until) ', line):
                out.append((line, block()))
            else:
                out.append((line, None))
        return out

    return block_all(block, lines)


def block_all(block, lines):
    stmts = []
    while True:
        b = block()
        if not b:
            break
        stmts.extend(b)
    return stmts


def run(src, max_steps=100_000):
    stmts = parse(src)
    env, out, steps = {}, [], 0

    def name(s):
        return s.strip().lower() if re.match(r'(?:a|an|the|my|your|our) ', s.strip().lower()) else s.strip()

    def value(expr):
        expr = expr.strip().rstrip(',')
        m = re.fullmatch(r'(.+?) (is less than|is greater than|is not|is) (.+)', expr)
        if m:
            a, b = value(m.group(1)), value(m.group(3))
            return {'is less than': a < b, 'is greater than': a > b, 'is not': a != b, 'is': a == b}[m.group(2)]
        m = re.fullmatch(r'(.+?) (plus|minus|times|over) (.+)', expr)
        if m:
            a, b = value(m.group(1)), value(m.group(3))
            return {'plus': a + b, 'minus': a - b, 'times': a * b, 'over': a / b if b else _div0()}[m.group(2)]
        if re.fullmatch(r'-?\d+(\.\d+)?', expr):
            return float(expr) if '.' in expr else int(expr)
        if expr.startswith('"') and expr.endswith('"') and len(expr) > 1:
            return expr[1:-1]
        if expr.lower() in LITERALS:
            return LITERALS[expr.lower()]
        k = name(expr)
        if k not in env:
            raise RockstarError(f'{expr!r} was never given a value')
        return env[k]

    def show(v):
        if v is True:
            return 'true'
        if v is False:
            return 'false'
        if v is None:
            return 'null'
        if isinstance(v, float) and v == int(v):
            return str(int(v))
        return str(v)

    def execute(block):
        nonlocal steps
        for line, body in block:
            steps += 1
            if steps > max_steps:
                raise RuntimeError('step limit')
            if body is not None:
                kind, cond = line.split(' ', 1)
                while bool(value(cond)) == (kind == 'While'):
                    execute(body)
                    steps += 1
                    if steps > max_steps:
                        raise RuntimeError('step limit')
                continue
            m = re.fullmatch(r'(?:Shout|Say|Whisper|Scream) (.+)', line)
            if m:
                out.append(show(value(m.group(1))) + '\n')
                continue
            m = re.fullmatch(r'Put (.+) into (' + VAR + ')', line)
            if m:
                env[name(m.group(2))] = value(m.group(1))
                continue
            m = re.fullmatch(r'(Build|Knock) (' + VAR + r') (up|down)(?:, (?:up|down))*', line)
            if m:
                n = line.count(', ') + 1
                env[name(m.group(2))] = env[name(m.group(2))] + (n if m.group(1) == 'Build' else -n)
                continue
            m = re.fullmatch(r'(' + VAR + r') says (.*)', line)
            if m:
                env[name(m.group(1))] = m.group(2)
                continue
            m = re.fullmatch(r'(' + VAR + r') (?:is|was|were) (.+)', line)
            if m:
                rest = m.group(2).strip()
                if re.fullmatch(r'-?\d+(\.\d+)?|"[^"]*"', rest) or rest.lower() in LITERALS:
                    env[name(m.group(1))] = value(rest)
                else:
                    env[name(m.group(1))] = poetic(rest.split())
                continue
            raise RockstarError(f'not in the subset: {line}')

    execute(stmts)
    return ''.join(out), steps


def _div0():
    raise RockstarError('division by zero')
