"""Small reference interpreters. Each run() returns (output, steps), where a
step is one executed instruction, so the figures the site prints can be
reproduced by anyone with these files."""


# ------------------------------------------------------------------ Brainfuck
def bf_run(code, stdin='', max_steps=10_000_000):
    prog = [c for c in code if c in '<>+-.,[]']
    jump, stack = {}, []
    for i, c in enumerate(prog):
        if c == '[':
            stack.append(i)
        elif c == ']':
            j = stack.pop()
            jump[i], jump[j] = j, i
    if stack:
        raise ValueError('unbalanced [')
    tape, p, ip, out, inp, steps = [0] * 30000, 0, 0, [], list(stdin), 0
    while ip < len(prog):
        c = prog[ip]
        steps += 1
        if steps > max_steps:
            raise RuntimeError('step limit')
        if c == '>':
            p += 1
        elif c == '<':
            p -= 1
        elif c == '+':
            tape[p] = (tape[p] + 1) % 256
        elif c == '-':
            tape[p] = (tape[p] - 1) % 256
        elif c == '.':
            out.append(chr(tape[p]))
        elif c == ',':
            tape[p] = ord(inp.pop(0)) if inp else 0
        elif c == '[' and tape[p] == 0:
            ip = jump[ip]
        elif c == ']' and tape[p] != 0:
            ip = jump[ip]
        ip += 1
    return ''.join(out), steps


# ------------------------------------------------------------------ Ook! (Brainfuck, spelled by an orangutan)
OOK = {'>': 'Ook. Ook?', '<': 'Ook? Ook.', '+': 'Ook. Ook.', '-': 'Ook! Ook!',
       '.': 'Ook! Ook.', ',': 'Ook. Ook!', '[': 'Ook! Ook?', ']': 'Ook? Ook!'}
KOO = {v: k for k, v in OOK.items()}


def bf_to_ook(code):
    return ' '.join(OOK[c] for c in code if c in OOK)


def ook_run(src, stdin=''):
    words = src.split()
    if len(words) % 2:
        raise ValueError('odd number of Ook words')
    return bf_run(''.join(KOO[f'{words[i]} {words[i + 1]}'] for i in range(0, len(words), 2)), stdin)


# ------------------------------------------------------------------ Befunge-93
def befunge_run(src, stdin='', max_steps=1_000_000):
    """Returns (output, steps, visited cells in order)."""
    lines = src.split('\n')
    grid = [[ord(lines[y][x]) if y < len(lines) and x < len(lines[y]) else 32 for x in range(80)] for y in range(25)]
    x = y = 0
    dx, dy = 1, 0
    stack, out, inp, steps, strmode, path = [], [], list(stdin), 0, False, []
    pop = lambda: stack.pop() if stack else 0
    import random
    rng = random.Random(0)
    while steps < max_steps:
        c = chr(grid[y][x])
        path.append((x, y))
        steps += 1
        if strmode and c != '"':
            stack.append(ord(c))
        elif c == '"':
            strmode = not strmode
        elif c.isdigit():
            stack.append(int(c))
        elif c in '+-*/%`':
            b, a = pop(), pop()
            stack.append({'+': a + b, '-': a - b, '*': a * b, '/': a // b if b else 0,
                          '%': a % b if b else 0, '`': int(a > b)}[c])
        elif c == '!':
            stack.append(int(not pop()))
        elif c in '><^v?':
            dx, dy = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}.get(
                c, rng.choice([(1, 0), (-1, 0), (0, -1), (0, 1)]))
        elif c == '_':
            dx, dy = (1, 0) if pop() == 0 else (-1, 0)
        elif c == '|':
            dx, dy = (0, 1) if pop() == 0 else (0, -1)
        elif c == ':':
            v = pop()
            stack += [v, v]
        elif c == '\\':
            b, a = pop(), pop()
            stack += [b, a]
        elif c == '$':
            pop()
        elif c == '.':
            out.append(f'{pop()} ')
        elif c == ',':
            out.append(chr(pop()))
        elif c == '#':
            x, y = (x + dx) % 80, (y + dy) % 25
        elif c == 'g':
            yy, xx = pop(), pop()
            stack.append(grid[yy][xx] if 0 <= yy < 25 and 0 <= xx < 80 else 0)
        elif c == 'p':
            yy, xx, v = pop(), pop(), pop()
            if 0 <= yy < 25 and 0 <= xx < 80:
                grid[yy][xx] = v
        elif c == '&':
            stack.append(int(''.join(inp)) if inp else 0)
            inp = []
        elif c == '~':
            stack.append(ord(inp.pop(0)) if inp else -1)
        elif c == '@':
            break
        x, y = (x + dx) % 80, (y + dy) % 25
    else:
        raise RuntimeError('step limit')
    return ''.join(out), steps, path


# ------------------------------------------------------------------ Whitespace
S, T, L = ' ', '\t', '\n'


def ws_number(n):
    return (S if n >= 0 else T) + bin(abs(n))[2:].replace('0', S).replace('1', T) + L


def ws_print(text):
    """A Whitespace program that prints text: push each character, output it, end."""
    return ''.join(S + S + ws_number(ord(ch)) + T + L + S + S for ch in text) + L + L + L


def ws_parse(src):
    code = [c for c in src if c in ' \t\n']
    i, prog = 0, []

    def num():
        nonlocal i
        sign = 1 if code[i] == S else -1
        i += 1
        v = 0
        while code[i] != L:
            v = v * 2 + (code[i] == T)
            i += 1
        i += 1
        return sign * v

    def lab():
        nonlocal i
        j = code.index(L, i)
        s = ''.join(code[i:j])
        i = j + 1
        return s

    table = [  # (prefix, name, argument)
        (S + S, 'push', num), (S + L + S, 'dup', None), (S + T + S, 'copy', num), (S + L + T, 'swap', None),
        (S + L + L, 'drop', None), (S + T + L, 'slide', num),
        (T + S + S + S, 'add', None), (T + S + S + T, 'sub', None), (T + S + S + L, 'mul', None),
        (T + S + T + S, 'div', None), (T + S + T + T, 'mod', None),
        (T + T + S, 'store', None), (T + T + T, 'load', None),
        (L + S + S, 'label', lab), (L + S + T, 'call', lab), (L + S + L, 'jmp', lab), (L + T + S, 'jz', lab),
        (L + T + T, 'jn', lab), (L + T + L, 'ret', None), (L + L + L, 'end', None),
        (T + L + S + S, 'outc', None), (T + L + S + T, 'outn', None), (T + L + T + S, 'inc', None),
        (T + L + T + T, 'inn', None)]
    while i < len(code):
        for pre, name, arg in table:
            if ''.join(code[i:i + len(pre)]) == pre:
                i += len(pre)
                prog.append((name, arg() if arg else None))
                break
        else:
            raise ValueError(f'unknown instruction at {i}')
    return prog


def ws_run(src, stdin='', max_steps=1_000_000):
    prog = ws_parse(src)
    labels = {a: k for k, (n, a) in enumerate(prog) if n == 'label'}
    st, heap, calls, out, inp, ip, steps = [], {}, [], [], list(stdin), 0, 0
    while ip < len(prog):
        n, a = prog[ip]
        ip += 1
        steps += 1
        if steps > max_steps:
            raise RuntimeError('step limit')
        if n == 'push':
            st.append(a)
        elif n == 'dup':
            st.append(st[-1])
        elif n == 'copy':
            st.append(st[-1 - a])
        elif n == 'swap':
            st[-1], st[-2] = st[-2], st[-1]
        elif n == 'drop':
            st.pop()
        elif n == 'slide':
            top = st.pop()
            del st[len(st) - a:]
            st.append(top)
        elif n in ('add', 'sub', 'mul', 'div', 'mod'):
            b, x = st.pop(), st.pop()
            st.append({'add': x + b, 'sub': x - b, 'mul': x * b, 'div': x // b, 'mod': x % b}[n])
        elif n == 'store':
            v, k = st.pop(), st.pop()
            heap[k] = v
        elif n == 'load':
            st.append(heap.get(st.pop(), 0))
        elif n == 'call':
            calls.append(ip)
            ip = labels[a]
        elif n == 'jmp':
            ip = labels[a]
        elif n == 'jz':
            if st.pop() == 0:
                ip = labels[a]
        elif n == 'jn':
            if st.pop() < 0:
                ip = labels[a]
        elif n == 'ret':
            ip = calls.pop()
        elif n == 'end':
            break
        elif n == 'outc':
            out.append(chr(st.pop()))
        elif n == 'outn':
            out.append(str(st.pop()))
        elif n == 'inc':
            heap[st.pop()] = ord(inp.pop(0)) if inp else -1
        elif n == 'inn':
            heap[st.pop()] = int(''.join(inp) or 0)
            inp = []
    return ''.join(out), steps


# ------------------------------------------------------------------ LOLCODE (the subset the site's examples use)
def lol_run(src, max_steps=100_000):
    import re
    lines = [l.strip() for l in src.split('\n') if l.strip() and not l.strip().startswith('BTW')]
    if not lines or not lines[0].startswith('HAI') or lines[-1] != 'KTHXBYE':
        raise ValueError('a LOLCODE program starts with HAI and ends with KTHXBYE')
    env, out, steps = {}, [], 0

    def val(expr):
        expr = expr.strip()
        m = re.fullmatch(r'(SUM|DIFF|PRODUKT|QUOSHUNT|MOD) OF (.+?) AN (.+)', expr)
        if m:
            a, b = val(m.group(2)), val(m.group(3))
            return {'SUM': a + b, 'DIFF': a - b, 'PRODUKT': a * b, 'QUOSHUNT': a // b, 'MOD': a % b}[m.group(1)]
        m = re.fullmatch(r'BOTH SAEM (.+?) AN (.+)', expr)
        if m:
            return val(m.group(1)) == val(m.group(2))
        if expr.startswith('"'):
            return expr[1:-1].replace(':)', '\n')
        if re.fullmatch(r'-?\d+', expr):
            return int(expr)
        return env[expr]

    body = lines[1:-1]
    pc, loops = 0, []
    while pc < len(body):
        steps += 1
        if steps > max_steps:
            raise RuntimeError('step limit')
        s = body[pc]
        m = re.fullmatch(r'I HAS A (\S+)(?: ITZ (.+))?', s)
        if m:
            env[m.group(1)] = val(m.group(2)) if m.group(2) else None
        elif s.startswith('VISIBLE '):
            parts = re.findall(r'"[^"]*"|\S+', s[8:])
            out.append(''.join(str(val(p)) for p in parts) + '\n')
        elif (m := re.fullmatch(r'(\S+) R (.+)', s)):
            env[m.group(1)] = val(m.group(2))
        elif (m := re.fullmatch(r'IM IN YR (\S+) UPPIN YR (\S+) TIL (.+)', s)):
            if val(m.group(3)):
                depth, j = 1, pc
                while depth:
                    j += 1
                    depth += body[j].startswith('IM IN YR') - body[j].startswith('IM OUTTA YR')
                pc = j
            else:
                loops.append(pc)
        elif s.startswith('IM OUTTA YR'):
            start = loops.pop()
            var = re.fullmatch(r'IM IN YR \S+ UPPIN YR (\S+) TIL .+', body[start]).group(1)
            env[var] += 1
            pc = start
            continue
        else:
            raise ValueError(f'not in the subset: {s}')
        pc += 1
    return ''.join(out), steps


def bf_tape(code, cells=8):
    """The first cells of the tape after a Brainfuck program has run."""
    prog = [c for c in code if c in '<>+-.,[]']
    jump, stack = {}, []
    for i, c in enumerate(prog):
        if c == '[':
            stack.append(i)
        elif c == ']':
            j = stack.pop()
            jump[i], jump[j] = j, i
    tape, p, ip = [0] * 30000, 0, 0
    while ip < len(prog):
        c = prog[ip]
        if c in '<>':
            p += 1 if c == '>' else -1
        elif c in '+-':
            tape[p] = (tape[p] + (1 if c == '+' else -1)) % 256
        elif (c == '[' and tape[p] == 0) or (c == ']' and tape[p] != 0):
            ip = jump[ip]
        ip += 1
    return tape[:cells]
