"""Run any program the site shows and print its output and step count.

    python _src/eso/run.py site/programs/hello.bf
    python _src/eso/run.py site/programs/hello-piet.png
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import langs  # noqa: E402
import malbolge  # noqa: E402
import piet  # noqa: E402

RUNNERS = {
    '.bf': lambda p: langs.bf_run(p.read_text(encoding='utf-8')),
    '.ook': lambda p: langs.ook_run(p.read_text(encoding='utf-8')),
    '.befunge': lambda p: langs.befunge_run(p.read_text(encoding='utf-8'))[:2],
    '.ws': lambda p: langs.ws_run(p.read_bytes().decode('ascii')),
    '.mb': lambda p: malbolge.run(p.read_text(encoding='utf-8')),
    '.lol': lambda p: langs.lol_run(p.read_text(encoding='utf-8')),
    '.png': lambda p: piet.run(piet.from_png(p)),
}


def run_file(path):
    path = pathlib.Path(path)
    return RUNNERS[path.suffix](path)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        out, steps = run_file(arg)
        print(f'{arg}: {out!r} in {steps} steps')
