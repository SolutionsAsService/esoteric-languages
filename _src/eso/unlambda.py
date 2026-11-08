"""Unlambda (David Madore, 1999): functions applied to functions, and nothing else.

A reference interpreter for the part of Unlambda this site uses. run() returns
(output, steps); a step is one function application.

Supported: ` (apply), s, k, i, v, d, r and .x. Not supported: c, e, @, ?x, |.
"""
import sys


class UnlambdaError(ValueError):
    pass


def parse(src):
    toks, i = [], 0
    while i < len(src):
        ch = src[i]
        if ch == '#':
            while i < len(src) and src[i] != '\n':
                i += 1
        elif ch.isspace():
            pass
        elif ch == '.':
            if i + 1 >= len(src):
                raise UnlambdaError('. needs a character')
            i += 1
            toks.append('.' + src[i])
        elif ch in '`skivdr':
            toks.append(ch)
        else:
            raise UnlambdaError(f'not in the subset: {ch!r}')
        i += 1
    pos = 0

    def node():
        nonlocal pos
        if pos >= len(toks):
            raise UnlambdaError('the program ends in the middle of an application')
        t = toks[pos]
        pos += 1
        if t == '`':
            f = node()
            return ('ap', f, node())
        return ('fn', t)

    tree = node()
    if pos != len(toks):
        raise UnlambdaError('extra tokens after the program')
    return tree


def run(src, max_steps=1_000_000):
    tree = parse(src)
    out, steps = [], 0
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10_000))

    def ev(n):
        if n[0] == 'fn':
            return n
        f = ev(n[1])
        if f == ('fn', 'd'):
            return ('promise', n[2])
        return apply(f, ev(n[2]))

    def force(p):
        return ev(p[1]) if p[0] == 'promise' else p

    def apply(f, x):
        nonlocal steps
        steps += 1
        if steps > max_steps:
            raise RuntimeError('step limit')
        f = force(f)
        t = f[0]
        if t == 'fn':
            name = f[1]
            if name == 'i':
                return x
            if name == 'v':
                return ('fn', 'v')
            if name == 'k':
                return ('k1', x)
            if name == 's':
                return ('s1', x)
            if name == 'r':
                out.append('\n')
                return x
            if name == 'd':
                return ('promise_arg', x)
            if name[0] == '.':
                out.append(name[1])
                return x
        if t == 'k1':
            return f[1]
        if t == 's1':
            return ('s2', f[1], x)
        if t == 's2':
            return apply(apply(f[1], x), apply(f[2], x))
        if t == 'promise_arg':
            return apply(force(f[1]), x)
        raise UnlambdaError(f'cannot apply {f}')

    ev(tree)
    return ''.join(out), steps
