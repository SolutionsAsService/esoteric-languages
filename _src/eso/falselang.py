"""FALSE (Wouter van Oortmerssen, 1993): a stack language with lambdas.

A reference interpreter for the part of FALSE this site uses. run() returns
(output, steps); a step is one token executed: a number, character, string,
operator or lambda literal, and each ! ? or # counts as one too.

Supported: integers, 'c characters, "strings", { comments }, [lambdas], ! ? #,
a-z variables with : and ;, $ % \\ @ ø, + - * / _ = > ~ & |, and , . ^.
"""
import re


class FalseError(ValueError):
    pass


def parse(src):
    toks, i = [], 0

    def block(i, close):
        out = []
        while i < len(src):
            ch = src[i]
            if ch == '{':
                i = src.index('}', i) + 1
            elif ch.isspace():
                i += 1
            elif ch.isdigit():
                m = re.compile(r'\d+').match(src, i)
                out.append(('num', int(m.group())))
                i = m.end()
            elif ch == "'":
                out.append(('num', ord(src[i + 1])))
                i += 2
            elif ch == '"':
                j = src.index('"', i + 1)
                out.append(('str', src[i + 1:j]))
                i = j + 1
            elif ch == '[':
                body, i = block(i + 1, ']')
                out.append(('lam', body))
            elif ch == ']':
                if close != ']':
                    raise FalseError('unbalanced ]')
                return out, i + 1
            elif ch.islower():
                out.append(('var', ch))
                i += 1
            elif ch in '$%\\@ø+-*/_=>~&|,.^!?#:;':
                out.append(('op', ch))
                i += 1
            else:
                raise FalseError(f'not in the subset: {ch!r}')
        if close:
            raise FalseError('unbalanced [')
        return out, i

    return block(0, None)[0]


def run(src, stdin='', max_steps=1_000_000):
    prog = parse(src)
    st, var, out, inp, steps = [], {}, [], list(stdin), 0

    def pop():
        if not st:
            raise FalseError('the stack is empty')
        return st.pop()

    def exe(code):
        nonlocal steps
        for kind, v in code:
            steps += 1
            if steps > max_steps:
                raise RuntimeError('step limit')
            if kind == 'num':
                st.append(v)
            elif kind == 'str':
                out.append(v)
            elif kind == 'lam':
                st.append(v)
            elif kind == 'var':
                st.append(('ref', v))
            else:
                op(v)

    def op(c):
        if c == '$':
            st.append(st[-1])
        elif c == '%':
            pop()
        elif c == '\\':
            b, a = pop(), pop()
            st.extend([b, a])
        elif c == '@':
            c3, b, a = pop(), pop(), pop()
            st.extend([b, c3, a])
        elif c == 'ø':
            n = pop()
            st.append(st[-1 - n])
        elif c in '+-*/&|=>':
            b, a = pop(), pop()
            st.append({'+': a + b, '-': a - b, '*': a * b, '/': a // b if b else 0,
                       '&': a & b, '|': a | b, '=': -1 if a == b else 0, '>': -1 if a > b else 0}[c])
        elif c == '_':
            st.append(-pop())
        elif c == '~':
            st.append(~pop())
        elif c == ',':
            out.append(chr(pop()))
        elif c == '.':
            out.append(str(pop()))
        elif c == '^':
            st.append(ord(inp.pop(0)) if inp else -1)
        elif c == ':':
            ref, v = pop(), pop()
            var[ref[1]] = v
        elif c == ';':
            ref = pop()
            st.append(var.get(ref[1], 0))
        elif c == '!':
            exe(pop())
        elif c == '?':
            body, cond = pop(), pop()
            if cond:
                exe(body)
        elif c == '#':
            body, cond = pop(), pop()
            while True:
                exe(cond)
                if not pop():
                    break
                exe(body)

    exe(prog)
    return ''.join(out), steps
