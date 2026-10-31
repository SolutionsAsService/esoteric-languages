"""Malbolge (Ben Olmstead, 1998): a reference interpreter.

Memory is 59049 ternary words. Each step the instruction is (mem[c] + c) % 94;
after it runs, mem[c] is replaced through the encryption table and c and d
both advance. Programs are loaded with the same rule the original
interpreter uses: only the eight instruction characters may appear, and the
rest of memory is filled with the crazy operation of the two words before it.
"""

ENCRYPT = ('5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB'
           '6v^=I_0/8|jsb9m<.TVac`uY*MK\'X~xDl}REokN:#?G"i@')
OPS = {4: 'jmp', 5: 'out', 23: 'in', 39: 'rot', 40: 'mov', 62: 'crz', 68: 'nop', 81: 'end'}
SIZE = 3 ** 10
CRZ = [[1, 0, 0], [1, 0, 2], [2, 2, 1]]


def crazy(a, d):
    r, p = 0, 1
    for _ in range(10):
        r += CRZ[d % 3][a % 3] * p
        a //= 3
        d //= 3
        p *= 3
    return r


def rotate(x):
    return x // 3 + (x % 3) * 3 ** 9


def load(src):
    mem = [0] * SIZE
    i = 0
    for ch in src:
        if ch.isspace():
            continue
        if (ord(ch) + i) % 94 not in OPS:
            raise ValueError(f'invalid character {ch!r} at {i}')
        mem[i] = ord(ch)
        i += 1
    while i < SIZE:
        mem[i] = crazy(mem[i - 1], mem[i - 2])
        i += 1
    return mem


def run(src, stdin='', max_steps=10_000_000, log=None, memory=None):
    mem = load(src)
    a = c = d = 0
    out, inp, steps = [], list(stdin), 0
    while steps < max_steps:
        if not 33 <= mem[c] <= 126:
            break
        op = OPS.get((mem[c] + c) % 94)
        steps += 1
        if log is not None:
            log.append((c, chr(mem[c]), op, chr(a % 256) if op == 'out' else ''))
        if op == 'jmp':
            c = mem[d]
        elif op == 'out':
            out.append(chr(a % 256))
        elif op == 'in':
            a = ord(inp.pop(0)) if inp else SIZE - 1
        elif op == 'rot':
            a = mem[d] = rotate(mem[d])
        elif op == 'mov':
            d = mem[d]
        elif op == 'crz':
            a = mem[d] = crazy(a, mem[d])
        elif op == 'end':
            break
        if 33 <= mem[c] <= 126:
            mem[c] = ord(ENCRYPT[mem[c] - 33])
        c = (c + 1) % SIZE
        d = (d + 1) % SIZE
    if memory is not None:
        memory.extend(mem)
    return ''.join(out), steps
