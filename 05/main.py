import fileinput
import re
from collections import deque
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line


def parse_stack(stack):
    res = [deque() for _ in range(9)]
    n = len(stack[0])
    for row in stack[:-1]:
        for i in range(1, n, 4):
            val = row[i]
            if val == " ":
                continue
            res[i // 4].appendleft(val)
    return res


def parse_step(step):
    mv, frm, to = None, None, None
    pattern = re.compile(r"move\s([0-9]+)\sfrom\s([0-9]+)\sto\s([0-9]+)")
    match = pattern.search(step)
    if match:
        mv = int(match.group(1))
        frm = int(match.group(2))
        to = int(match.group(3))
    return (mv, frm, to)


def parse():
    stack = []
    steps = []
    stack_done = False
    for line in get_input():
        if not stack_done:
            if line == "\n":
                stack_done = True
            stack.append(line)
            continue
        steps.append(line)
    res_stack = parse_stack(stack)
    res_steps = [parse_step(s) for s in steps]
    return res_stack, res_steps


def simulate(stack, mv, frm, to):
    # moved one at a time
    for _ in range(mv):
        stack[to - 1].append(stack[frm - 1].pop())


def simulate2(stack, mv, frm, to):
    # move all at once
    temp = deque()
    for _ in range(mv):
        temp.appendleft(stack[frm - 1].pop())
    for v in temp:
        stack[to - 1].append(v)


def q1():
    stack, steps = parse()
    for step in steps:
        simulate(stack, *step)
    return "".join([row[-1] for row in stack if row])


def q2():
    stack, steps = parse()
    for step in steps:
        simulate2(stack, *step)
    return "".join([row[-1] for row in stack if row])


def main():
    print(q1())
    print(q2())
    assert q1() == "VPCDMSLWJ"
    assert q2() == "TPWCGNCCG"


if __name__ == "__main__":
    main()
