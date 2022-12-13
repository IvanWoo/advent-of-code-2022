import math
from typing import Tuple
from functools import cmp_to_key
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with open(INPUT_FILE) as f:
        return "".join(f.read()).split("\n\n")


def compare(left, right) -> int:
    # this hack makes the code more readable
    t_left, t_right = type(left).__name__, type(right).__name__
    match (t_left, t_right):
        case ("int", "int"):
            return left - right
        case ("int", "list"):
            return compare([left], right)
        case ("list", "int"):
            return compare(left, [right])
        case ("list", "list"):
            for i in range(len(left)):
                if i >= len(right):
                    return 1
                head = compare(left[i], right[i])
                if head != 0:
                    return head
            if len(left) < len(right):
                return -1
    return 0


def q1():
    right_orders = []
    for i, pair in enumerate(get_input()):
        left, right = pair.split("\n")
        left, right = eval(left), eval(right)
        if compare(left, right) < 0:
            right_orders.append(i + 1)
    return sum(right_orders)


def q2():
    dividers = [[[2]], [[6]]]
    pairs = dividers[:]
    for pair in get_input():
        pairs.extend(map(eval, pair.split("\n")))
    pairs.sort(key=cmp_to_key(compare))
    return math.prod([i + 1 for i, p in enumerate(pairs) if p in dividers])


def main():
    print(q1())
    print(q2())
    assert q1() == 6072
    assert q2() == 22184


if __name__ == "__main__":
    main()
