"""Piet (David Morgan-Mar): an interpreter and a generator.

A program is a grid of codels in 18 colours plus white and black. The
command is chosen by how far hue and lightness change between two colour
blocks; a push pushes the size of the block it leaves.
"""

HUES = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
RGB = {  # (lightness 0 light, 1 normal, 2 dark) x hue
    (0, 0): 'FFC0C0', (0, 1): 'FFFFC0', (0, 2): 'C0FFC0', (0, 3): 'C0FFFF', (0, 4): 'C0C0FF', (0, 5): 'FFC0FF',
    (1, 0): 'FF0000', (1, 1): 'FFFF00', (1, 2): '00FF00', (1, 3): '00FFFF', (1, 4): '0000FF', (1, 5): 'FF00FF',
    (2, 0): 'C00000', (2, 1): 'C0C000', (2, 2): '00C000', (2, 3): '00C0C0', (2, 4): '0000C0', (2, 5): 'C000C0',
}
WHITE, BLACK = 'W', 'K'
COMMANDS = [['none', 'push', 'pop'], ['add', 'sub', 'mul'], ['div', 'mod', 'not'],
            ['greater', 'pointer', 'switch'], ['dup', 'roll', 'in_n'], ['in_c', 'out_n', 'out_c']]
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # DP: right, down, left, up (clockwise)


def block(grid, x, y):
    h, w = len(grid), len(grid[0])
    col, seen, todo = grid[y][x], {(x, y)}, [(x, y)]
    while todo:
        cx, cy = todo.pop()
        for dx, dy in DIRS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and grid[ny][nx] == col:
                seen.add((nx, ny))
                todo.append((nx, ny))
    return seen


def exit_codel(cells, dp, cc):
    dx, dy = DIRS[dp]
    edge = max(x * dx + y * dy for x, y in cells)
    front = [(x, y) for x, y in cells if x * dx + y * dy == edge]
    # CC left is DP turned anticlockwise, CC right clockwise
    ax, ay = DIRS[(dp + (1 if cc else -1)) % 4]
    return max(front, key=lambda p: p[0] * ax + p[1] * ay)


def run(grid, stdin='', max_steps=100_000, log=None):
    h, w = len(grid), len(grid[0])
    ok = lambda x, y: 0 <= x < w and 0 <= y < h and grid[y][x] != BLACK
    x = y = dp = cc = 0  # cc 0 = left, 1 = right
    stack, out, inp, steps = [], [], list(stdin), 0
    while steps < max_steps:
        cells = block(grid, x, y)
        size = len(cells)
        for attempt in range(8):
            ex, ey = exit_codel(cells, dp, cc)
            nx, ny = ex + DIRS[dp][0], ey + DIRS[dp][1]
            if ok(nx, ny):
                break
            if attempt % 2 == 0:
                cc ^= 1
            else:
                dp = (dp + 1) % 4
        else:
            return ''.join(out), steps
        if grid[ny][nx] == WHITE:  # slide through white without a command
            while ok(nx + DIRS[dp][0], ny + DIRS[dp][1]) and grid[ny][nx] == WHITE:
                nx, ny = nx + DIRS[dp][0], ny + DIRS[dp][1]
            x, y = nx, ny
            continue
        a, b = grid[y][x], grid[ny][nx]
        if a != WHITE:
            cmd = COMMANDS[(b[1] - a[1]) % 6][(b[0] - a[0]) % 3]
            steps += 1
            if log is not None:
                log.append((a, b, size, cmd))
            try:
                if cmd == 'push':
                    stack.append(size)
                elif cmd == 'pop':
                    stack.pop()
                elif cmd in ('add', 'sub', 'mul', 'div', 'mod', 'greater'):
                    if len(stack) >= 2:
                        q, p = stack.pop(), stack.pop()
                        stack.append({'add': p + q, 'sub': p - q, 'mul': p * q, 'div': p // q if q else 0,
                                      'mod': p % q if q else 0, 'greater': int(p > q)}[cmd])
                elif cmd == 'not':
                    stack.append(int(not stack.pop()))
                elif cmd == 'pointer':
                    dp = (dp + stack.pop()) % 4
                elif cmd == 'switch':
                    cc = (cc + stack.pop()) % 2
                elif cmd == 'dup':
                    stack.append(stack[-1])
                elif cmd == 'out_n':
                    out.append(str(stack.pop()))
                elif cmd == 'out_c':
                    out.append(chr(stack.pop()))
                elif cmd == 'in_c':
                    stack.append(ord(inp.pop(0)) if inp else 0)
            except IndexError:
                pass  # a command with too few values is ignored
        x, y = nx, ny
    raise RuntimeError('step limit')


def generate(text, height=24, hue=0, light=1):
    """Two blocks per character: a block whose size is the character code, then
    a single codel. Leaving the big block is a push (lightness +1); leaving the
    single codel is out(char) (hue +5, lightness +2). The program runs along
    row 1; row 0 is black except the start codel and the closing trap."""
    H = height + 1
    cols = []  # each column: list of H cells

    def colour(l, hh):
        return (l % 3, hh % 6)

    cur = (light, hue)
    first = True
    for ch in text:
        n = ord(ch) - (1 if first else 0)  # the start codel at (0,0) belongs to the first block
        full, rest = divmod(n, height)
        for _ in range(full):
            cols.append([BLACK] + [cur] * height)
        if rest:
            cols.append([BLACK] + [cur] * rest + [BLACK] * (height - rest))
        if first:
            cols[0][0] = cur
            first = False
        one = colour(cur[0] + 1, cur[1])
        cols.append([BLACK, one] + [BLACK] * (height - 1))
        cur = colour(one[0] + 2, one[1] + 5)
    # the closing trap: the last block wraps up over the final single codel
    cols[-1][0] = cur
    cols.append([cur, cur] + [BLACK] * (height - 1))
    return [[cols[x][y] for x in range(len(cols))] for y in range(H)]


def to_svg(grid, codel=4, cls='piet'):
    h, w = len(grid), len(grid[0])
    rects = []
    for y in range(h):
        x = 0
        while x < w:  # merge horizontal runs to keep the file small
            c, x0 = grid[y][x], x
            while x < w and grid[y][x] == c:
                x += 1
            fill = {'K': '000000', 'W': 'FFFFFF'}.get(c) if isinstance(c, str) else RGB[c]
            rects.append(f'<rect x="{x0 * codel}" y="{y * codel}" width="{(x - x0) * codel}" height="{codel}" fill="#{fill}"/>')
    return (f'<svg class="{cls}" viewBox="0 0 {w * codel} {h * codel}" xmlns="http://www.w3.org/2000/svg" '
            f'shape-rendering="crispEdges" preserveAspectRatio="xMinYMax meet" aria-hidden="true" focusable="false">{"".join(rects)}</svg>')


def to_png(grid, path, codel=10):
    from PIL import Image
    h, w = len(grid), len(grid[0])
    img = Image.new('RGB', (w * codel, h * codel))
    px = img.load()
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            hx = {'K': '000000', 'W': 'FFFFFF'}.get(c) if isinstance(c, str) else RGB[c]
            rgb = tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))
            for yy in range(codel):
                for xx in range(codel):
                    px[x * codel + xx, y * codel + yy] = rgb
    img.save(path)


def from_png(path, codel=10):
    from PIL import Image
    img = Image.open(path).convert('RGB')
    inv = {v: k for k, v in RGB.items()}
    w, h = img.width // codel, img.height // codel
    grid = []
    for y in range(h):
        row = []
        for x in range(w):
            hx = '%02X%02X%02X' % img.getpixel((x * codel, y * codel))
            row.append(inv.get(hx, BLACK if hx == '000000' else WHITE))
        grid.append(row)
    return grid
