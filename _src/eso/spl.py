"""Shakespeare Programming Language (Karl Wiberg and Jon Åslund, 2001): a program is a play.

A reference interpreter for the part of SPL this site uses. run() returns
(output, steps); a step is one spoken sentence read while it is the
interpreter's turn (a sentence skipped by "If so" or "If not" still counts).

Characters are variables holding integers, each with a stack. A noun is worth
1, or -1 if it is a negative noun; each adjective in front of it doubles the
value. The word lists below are a subset of the specification's, so a play
that uses other words is rejected, not guessed at.
"""
import re

NEG_NOUNS = {'devil', 'fiend', 'hell', 'hog', 'pig', 'plague', 'rat', 'toad', 'villain', 'coward', 'knave', 'curse',
             'liar', 'snake', 'swine', 'fool', 'bastard', 'wretch'}
NOUNS = {'angel', 'brother', 'cat', 'chihuahua', 'cousin', 'cow', 'daughter', 'day', 'door', 'face', 'father', 'flower',
         'friend', 'hamster', 'heaven', 'hero', 'horse', 'king', 'lamp', 'lantern', 'lord', 'moon', 'morning', 'mother',
         'nose', 'pony', 'purse', 'queen', 'road', 'rose', 'sister', 'sky', 'son', 'squirrel', 'summer', 'sun', 'thing',
         'town', 'tree', 'uncle', 'wind', 'wolf', 'woman', 'man'} | NEG_NOUNS
ADJECTIVES = {'amazing', 'beautiful', 'big', 'blessed', 'bold', 'brave', 'bright', 'charming', 'fair', 'fine', 'gentle',
              'golden', 'good', 'great', 'happy', 'handsome', 'honest', 'lovely', 'merry', 'noble', 'pretty', 'proud',
              'sweet', 'sunny', 'warm', 'black', 'blue', 'green', 'hard', 'huge', 'large', 'little', 'normal', 'old',
              'purple', 'red', 'small', 'tiny', 'white', 'yellow', 'bad', 'cowardly', 'cursed', 'damned', 'dirty',
              'evil', 'foul', 'hairy', 'horrible', 'lying', 'rotten', 'ugly', 'vile', 'worried'}
GREATER = {'better', 'bigger', 'fresher', 'friendlier', 'jollier', 'nicer', 'prettier', 'happier', 'warmer'}
LESS = {'worse', 'punier', 'smaller', 'dirtier', 'uglier'}
DET = {'a', 'an', 'the', 'my', 'your', 'thy', 'thine', 'mine', 'his', 'her', 'our'}
FIRST = {'me', 'myself', 'i'}
SECOND = {'you', 'thee', 'thou', 'thyself', 'yourself'}


class SplError(ValueError):
    pass


def roman(s):
    vals, total, prev = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100}, 0, 0
    for ch in reversed(s.lower()):
        v = vals[ch]
        total += -v if v < prev else v
        prev = max(prev, v)
    return total


TOKEN = re.compile(r'\[(?P<dir>[^\]]*)\]'
                   r'|(?P<head>(?:Act|Scene)\s+(?P<kind_n>[IVXLC]+)\s*:[^.]*\.)'
                   r'|(?P<who>[A-Z][A-Za-z\' ]*?)\s*:'
                   r'|(?P<sent>[^.!?\[\]:]+[.!?])')


def parse(src):
    text = src.strip()
    title, _, rest = text.partition('.')
    lines = rest.strip().split('\n')
    cast, body_at = [], 0
    for i, l in enumerate(lines):
        l = l.strip()
        if not l:
            continue
        if re.match(r'^act\s', l, re.I):
            body_at = i
            break
        cast.append(l.split(',')[0].strip().lower())
    body = '\n'.join(lines[body_at:])
    events, act, scene = [], 0, 0
    scenes, acts = {}, {}
    for m in TOKEN.finditer(body):
        if m.group('dir') is not None:
            d = m.group('dir').strip()
            low = d.lower()
            names = lambda t: [n.strip().lower() for n in re.split(r',|\band\b', t) if n.strip()]
            if low.startswith('enter'):
                events.append(('enter', names(d[5:])))
            elif low.startswith('exeunt'):
                events.append(('exeunt', names(d[6:])))
            elif low.startswith('exit'):
                events.append(('exit', names(d[4:])))
            else:
                raise SplError(f'unknown stage direction [{d}]')
        elif m.group('head'):
            head = m.group('head')
            n = roman(m.group('kind_n'))
            if head.lower().startswith('act'):
                act, scene = n, 0
            else:
                scene = n
                scenes[(act, scene)] = len(events)
                acts.setdefault(act, len(events))
        elif m.group('who'):
            who = m.group('who').strip().lower()
            if who not in cast:
                raise SplError(f'{who!r} is not in the dramatis personae')
            events.append(('speaker', who))
        else:
            events.append(('say', m.group('sent').strip()))
    return title.strip(), cast, events, scenes, acts


def run(src, stdin='', max_steps=100_000):
    title, cast, events, scenes, acts = parse(src)
    value = {c: 0 for c in cast}
    stack = {c: [] for c in cast}
    stage, speaker, cond = [], None, False
    out, inp, steps = [], list(stdin), 0
    cur_act = min(scenes, key=scenes.get)[0] if scenes else 1
    pc = 0

    def value_of(tokens, pos, me, you):
        t = tokens
        if pos >= len(t):
            raise SplError('a value was expected')
        w = t[pos]
        for phrase, fn in (
                (('the', 'sum', 'of'), lambda a, b: a + b),
                (('the', 'difference', 'between'), lambda a, b: a - b),
                (('the', 'product', 'of'), lambda a, b: a * b),
                (('the', 'quotient', 'between'), lambda a, b: a // b if b else _div0()),
                (('the', 'remainder', 'of', 'the', 'quotient', 'between'), lambda a, b: a % b if b else _div0())):
            if tuple(t[pos:pos + len(phrase)]) == phrase:
                a, p = value_of(t, pos + len(phrase), me, you)
                if p >= len(t) or t[p] != 'and':
                    raise SplError(f'"and" expected after {" ".join(phrase)}')
                b, p = value_of(t, p + 1, me, you)
                return fn(a, b), p
        for phrase, fn in ((('the', 'square', 'root', 'of'), lambda a: int(a ** 0.5) if a >= 0 else _div0()),
                           (('the', 'square', 'of'), lambda a: a * a), (('the', 'cube', 'of'), lambda a: a ** 3),
                           (('the', 'factorial', 'of'), _fact), (('twice',), lambda a: 2 * a)):
            if tuple(t[pos:pos + len(phrase)]) == phrase:
                a, p = value_of(t, pos + len(phrase), me, you)
                return fn(a), p
        if w in ('nothing', 'zero'):
            return 0, pos + 1
        if w in FIRST:
            return value[me], pos + 1
        if w in SECOND:
            return value[you], pos + 1
        if w in value:
            return value[w], pos + 1
        if w in DET:
            p, n = pos + 1, 0
            while p < len(t) and t[p] in ADJECTIVES:
                p, n = p + 1, n + 1
            if p < len(t) and t[p] in NOUNS:
                return (-1 if t[p] in NEG_NOUNS else 1) * 2 ** n, p + 1
        raise SplError(f'cannot read a value at {" ".join(t[pos:pos + 4])!r}')

    def goto(kind, n):
        nonlocal pc, cur_act
        if kind == 'scene':
            if (cur_act, n) not in scenes:
                raise SplError(f'no scene {n} in act {cur_act}')
            pc = scenes[(cur_act, n)]
        else:
            if n not in acts:
                raise SplError(f'no act {n}')
            cur_act = n
            pc = acts[n]

    while pc < len(events):
        ev = events[pc]
        pc += 1
        kind = ev[0]
        if kind == 'enter':
            for n in ev[1]:
                if n in stage:
                    raise SplError(f'{n} is already on stage')
                stage.append(n)
        elif kind == 'exit':
            for n in ev[1]:
                stage.remove(n)
        elif kind == 'exeunt':
            if ev[1]:
                for n in ev[1]:
                    stage.remove(n)
            else:
                stage.clear()
        elif kind == 'speaker':
            speaker = ev[1]
        else:
            steps += 1
            if steps > max_steps:
                raise RuntimeError('step limit')
            if speaker not in stage or len(stage) != 2:
                raise SplError('a line needs exactly two characters on stage, with the speaker one of them')
            me = speaker
            you = next(n for n in stage if n != me)
            s = ev[1]
            q = s.endswith('?')
            words = re.sub(r"[^a-z' ]", ' ', s.lower()).split()
            if words[:1] == ['if'] and len(words) > 1 and words[1] in ('so', 'not'):
                if cond != (words[1] == 'so'):
                    continue
                words = words[2:]
            w = words
            if re.match(r'(let us|we shall|we must) (proceed|return) to ', ' '.join(w)):
                m = re.search(r'to (act|scene) ([ivxlc]+)$', ' '.join(w))
                if not m:
                    raise SplError(f'cannot read {s!r}')
                goto(m.group(1), roman(m.group(2)))
            elif ' '.join(w) == 'speak your mind':
                out.append(chr(value[you]))
            elif ' '.join(w) == 'open your heart':
                out.append(str(value[you]))
            elif ' '.join(w) == 'listen to your heart':
                m = re.match(r'-?\d+', ''.join(inp))
                if not m:
                    raise SplError('no number to read')
                del inp[:len(m.group(0))]
                value[you] = int(m.group(0))
            elif ' '.join(w) == 'open your mind':
                value[you] = ord(inp.pop(0)) if inp else -1
            elif w[:1] == ['remember']:
                stack[you].append(value_of(w, 1, me, you)[0])
            elif w[:1] == ['recall']:
                if not stack[you]:
                    raise SplError('recall from an empty stack')
                value[you] = stack[you].pop()
            elif q and w[0] in ('are', 'art') and w[1] in SECOND:
                p, neg = 2, False
                if w[p] == 'not':
                    p, neg = p + 1, True
                if w[p] == 'as' and w[p + 2] == 'as' and w[p + 1] in ADJECTIVES:
                    rhs, _ = value_of(w, p + 3, me, you)
                    truth = value[you] == rhs
                elif w[p] in GREATER | LESS and w[p + 1] == 'than':
                    rhs, _ = value_of(w, p + 2, me, you)
                    truth = value[you] > rhs if w[p] in GREATER else value[you] < rhs
                else:
                    raise SplError(f'cannot read the question {s!r}')
                cond = truth != neg
            elif w[0] in SECOND and w[1] in ('are', 'art', 'be'):
                p = 2
                if w[p] == 'as' and p + 2 < len(w) and w[p + 1] in ADJECTIVES and w[p + 2] == 'as':
                    p += 3
                v, end = value_of(w, p, me, you)
                if end != len(w):
                    raise SplError(f'unread words after the value in {s!r}')
                value[you] = v
            else:
                raise SplError(f'not in the subset: {s}')
    return ''.join(out), steps


def _div0():
    raise SplError('division by zero')


def _fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r
