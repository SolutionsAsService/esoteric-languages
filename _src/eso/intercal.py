"""INTERCAL (Don Woods and James Lyon, 1972): a language designed to resemble nothing else.

A reference interpreter for the part of INTERCAL this site uses. run() returns
(output, steps); a step is one statement executed.

Supported: PLEASE and DO, labels, ,n arrays with SUB, .n and :n variables
assigned from #constants, READ OUT of arrays (the Turing Text Model) and of
numbers (in Roman numerals), and GIVE UP. The compiler's politeness rule is
enforced: fewer than a fifth of the statements marked PLEASE is rejected as
insufficiently polite, more than a third as too polite.
"""
import re


class IntercalError(ValueError):
    pass


def roman(n):
    if not 0 < n < 4000:
        raise IntercalError('only 1 to 3999 are written here')
    out = ''
    for v, s in ((1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'),
                 (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
        while n >= v:
            out, n = out + s, n - v
    return out


def parse(src):
    stmts = []
    for raw in src.split('\n'):
        line = raw.strip()
        if not line:
            continue
        m = re.fullmatch(r'(?:\((\d+)\)\s*)?(PLEASE\s+)?(?:DO\s+)?(.+)', line)
        label, polite, body = m.group(1), bool(m.group(2)), m.group(3).strip()
        if not polite and not line.startswith(('DO', '(')) :
            raise IntercalError(f'a statement starts with DO or PLEASE: {line!r}')
        stmts.append((int(label) if label else None, polite, body))
    return stmts


def run(src, max_steps=100_000):
    stmts = parse(src)
    polite = sum(1 for s in stmts if s[1])
    if polite * 5 < len(stmts):
        raise IntercalError('E079 PROGRAMMER IS INSUFFICIENTLY POLITE')
    if polite * 3 > len(stmts):
        raise IntercalError('E099 PROGRAMMER IS OVERLY POLITE')
    arrays, scalars, out, steps, last = {}, {}, [], 0, {}
    pc = 0
    while pc < len(stmts):
        steps += 1
        if steps > max_steps:
            raise RuntimeError('step limit')
        _, _, body = stmts[pc]
        pc += 1
        if body == 'GIVE UP':
            break
        m = re.fullmatch(r'(,\d+)\s*<-\s*#(\d+)', body)
        if m:
            arrays[m.group(1)] = [0] * int(m.group(2))
            continue
        m = re.fullmatch(r'(,\d+)\s+SUB\s+#(\d+)\s*<-\s*#(\d+)', body)
        if m:
            a, i, v = m.group(1), int(m.group(2)), int(m.group(3))
            if a not in arrays or not 1 <= i <= len(arrays[a]):
                raise IntercalError(f'{a} has no element {i}')
            arrays[a][i - 1] = v % 256
            continue
        m = re.fullmatch(r'([.:]\d+)\s*<-\s*#(\d+)', body)
        if m:
            limit = 65536 if m.group(1)[0] == '.' else 2 ** 32
            if int(m.group(2)) >= limit:
                raise IntercalError('the constant does not fit')
            scalars[m.group(1)] = int(m.group(2))
            continue
        m = re.fullmatch(r'READ OUT\s+(.+)', body)
        if m:
            what = m.group(1).strip()
            if what.startswith(','):
                prev = last.get(what, 0)
                for e in arrays[what]:
                    t = (prev - e) % 256
                    prev = t
                    out.append(chr(int(f'{t:08b}'[::-1], 2)))
                last[what] = prev
            else:
                out.append(roman(scalars.get(what, 0) if what[0] in '.:' else int(what.lstrip('#'))) + '\n')
            continue
        raise IntercalError(f'not in the subset: {body}')
    return ''.join(out), steps
