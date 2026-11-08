"""Chef (David Morgan-Mar, 2002): a program is a recipe.

A reference interpreter for the part of Chef this site uses. run() returns
(output, steps); a step is one method sentence executed (a loop's opening
and closing sentences count each time they are reached).

Supported: ingredients with dry/liquid measures; Take, Put, Fold, Add, Remove,
Combine, Divide, Add dry ingredients, Liquefy, Stir, Clean, Pour, Set aside,
Refrigerate, "Verb the x ... Verb until verbed" loops, numbered mixing bowls
and baking dishes. Not supported: auxiliary recipes (Serve with), Mix well
(it is random), and the "Cooking time" and "Pre-heat" lines are ignored.
Numbers in a baking dish print as decimals followed by a space.
"""
import re

DRY = {'g', 'kg', 'pinch', 'pinches'}
LIQUID = {'ml', 'l', 'dash', 'dashes'}
EITHER = {'cup', 'cups', 'teaspoon', 'teaspoons', 'tablespoon', 'tablespoons'}
ING = re.compile(r'^(?:(\d+)\s+)?(?:(heaped|level)\s+)?(?:(' + '|'.join(sorted(DRY | LIQUID | EITHER, key=len, reverse=True)) + r')\s+)?(.+)$')
NTH = r'(?:the |(\d+)(?:st|nd|rd|th) )'
BOWL = NTH + r'mixing bowl'
DISH = r'(?:the |(\d+)(?:st|nd|rd|th) )baking dish'


class ChefError(ValueError):
    pass


def parse(src):
    lines = [l.rstrip() for l in src.strip().split('\n')]
    try:
        i_ing = next(i for i, l in enumerate(lines) if l.strip().lower() == 'ingredients.')
        i_met = next(i for i, l in enumerate(lines) if l.strip().lower() == 'method.')
    except StopIteration:
        raise ChefError('a recipe needs an "Ingredients." list and a "Method."')
    ings = {}
    for l in lines[i_ing + 1:i_met]:
        l = l.strip()
        if not l or l.lower().startswith(('cooking time', 'pre-heat', 'preheat')):
            continue
        m = ING.match(l)
        if not m:
            raise ChefError(f'cannot read the ingredient {l!r}')
        num, heap, unit, name = m.groups()
        dry = None
        if unit in DRY or heap:
            dry = True
        elif unit in LIQUID:
            dry = False
        ings[name.strip().lower()] = [int(num) if num else 0, dry]
    text = ' '.join(l.strip() for l in lines[i_met + 1:])
    serves = 0
    m = re.search(r'\bserves (\d+)\s*\.?\s*$', text, re.I)
    if m:
        serves = int(m.group(1))
        text = text[:m.start()]
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    return ings, sentences, serves


def _name(s):
    s = s.strip().lower()
    return s[4:] if s.startswith('the ') else s


def _bowl(g):
    return int(g) - 1 if g else 0


def run(src, stdin='', max_steps=100_000):
    ings, sents, serves = parse(src)
    bowls, dishes = {}, {}
    inp = list(stdin)
    steps = 0

    def get(name):
        name = _name(name)
        if name not in ings:
            raise ChefError(f'no ingredient called {name!r}')
        return ings[name]

    def bowl(n):
        return bowls.setdefault(n, [])

    # pair each loop opener with its closer
    kinds = []
    for s in sents:
        low = s.lower()
        if re.match(r'^(\w+) (?:the )?(.+)$', low) and not _known(low) and ' until ' not in low:
            kinds.append('open')
        elif ' until ' in low and re.search(r'until \w+$', low) and not _known(low):
            kinds.append('close')
        else:
            kinds.append(None)
    pair, stack = {}, []
    for i, k in enumerate(kinds):
        if k == 'open':
            stack.append(i)
        elif k == 'close':
            if not stack:
                raise ChefError('a loop is closed that was never opened')
            j = stack.pop()
            pair[i], pair[j] = j, i
    if stack:
        raise ChefError('a loop is opened and never closed')

    pc, halt = 0, False
    while pc < len(sents) and not halt:
        steps += 1
        if steps > max_steps:
            raise RuntimeError('step limit')
        s, low = sents[pc], sents[pc].lower()
        m = None
        if (m := re.fullmatch(r'take (.+) from refrigerator', low)):
            get(m.group(1))[0] = ord(inp.pop(0)) if inp else 0
        elif (m := re.fullmatch(r'put (.+?) into ' + BOWL, low)):
            v = get(m.group(1))
            bowl(_bowl(m.group(2))).append(list(v))
        elif (m := re.fullmatch(r'fold (.+?) into ' + BOWL, low)):
            b = bowl(_bowl(m.group(2)))
            if not b:
                raise ChefError('fold from an empty mixing bowl')
            get(m.group(1))[0] = b.pop()[0]
        elif low.startswith('add dry ingredients'):
            m = re.fullmatch(r'add dry ingredients(?: to ' + BOWL + ')?', low)
            bowl(_bowl(m.group(1) if m else None)).append([sum(v for v, d in ings.values() if d), True])
        elif (m := re.fullmatch(r'(add|remove|combine|divide) (.+?)(?: (?:to|from|into) ' + BOWL + ')?', low)):
            op, name, n = m.group(1), m.group(2), _bowl(m.group(3))
            b, v = bowl(n), get(name)[0]
            if not b:
                raise ChefError(f'{op} on an empty mixing bowl')
            if op == 'add':
                b[-1][0] += v
            elif op == 'remove':
                b[-1][0] -= v
            elif op == 'combine':
                b[-1][0] *= v
            else:
                b[-1][0] //= v
        elif (m := re.fullmatch(r'liqu[ei]fy contents of ' + BOWL, low)):
            for item in bowl(_bowl(m.group(1))):
                item[1] = False
        elif (m := re.fullmatch(r'liqu[ei]fy (.+)', low)):
            get(m.group(1))[1] = False
        elif (m := re.fullmatch(r'stir (?:' + BOWL + r' )?for (\d+) minutes?', low)):
            _stir(bowl(_bowl(m.group(1))), int(m.group(2)))
        elif (m := re.fullmatch(r'stir (.+?) into ' + BOWL, low)):
            _stir(bowl(_bowl(m.group(2))), get(m.group(1))[0])
        elif (m := re.fullmatch(r'clean ' + BOWL, low)):
            bowls[_bowl(m.group(1))] = []
        elif (m := re.fullmatch(r'pour contents of ' + BOWL + ' into ' + DISH, low)):
            dishes.setdefault(_bowl(m.group(2)), []).extend(list(i) for i in bowl(_bowl(m.group(1))))
        elif low == 'set aside':
            depth = 0
            for j in range(pc, len(sents)):
                if kinds[j] == 'open' and j > pc:
                    depth += 1
                elif kinds[j] == 'close':
                    if depth == 0:
                        pc = j
                        break
                    depth -= 1
            else:
                raise ChefError('"Set aside" outside a loop')
        elif (m := re.fullmatch(r'refrigerate(?: for (\d+) hours?)?', low)):
            if m.group(1):
                serves = int(m.group(1))
            halt = True
        elif low.startswith('serve with'):
            raise ChefError('auxiliary recipes are not supported')
        elif kinds[pc] == 'open':
            name = re.fullmatch(r'\w+ (?:the )?(.+)', low).group(1)
            if get(name)[0] == 0:
                pc = pair[pc]
        elif kinds[pc] == 'close':
            m = re.fullmatch(r'\w+(?: (?:the )?(.+?))? until \w+', low)
            if m.group(1):
                get(m.group(1))[0] -= 1
            pc = pair[pc] - 1
        else:
            raise ChefError(f'not in the subset: {s}')
        pc += 1

    out = []
    for n in range(serves):
        for v, dry in reversed(dishes.get(n, [])):
            out.append(str(v) + ' ' if dry is not False else chr(v))
    return ''.join(out), steps


def _stir(b, n):
    if b and n:
        n = min(n, len(b) - 1)
        top = b.pop()
        b.insert(len(b) - n, top)


_FIXED = re.compile(r'^(take|put|fold|add|remove|combine|divide|liqu[ei]fy|stir|clean|pour|set aside|refrigerate|serve)\b')


def _known(low):
    return bool(_FIXED.match(low))
