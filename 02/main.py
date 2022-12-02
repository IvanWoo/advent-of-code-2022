import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def convert(s: str) -> int:
    mapping = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}
    return mapping[s]


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield [convert(x) for x in line.split()]


def get_score(diff: int) -> int:
    match diff % 3:
        case 1:
            return 6
        case 0:
            return 3
        case 2:
            return 0


def q1():
    score = 0
    for op, me in get_input():
        score += get_score(me - op) + me + 1
    return score


def q2():
    score = 0
    for op, result in get_input():
        me = (op + result - 1) % 3
        score += get_score(me - op) + me + 1
    return score


def main():
    print(q1())
    print(q2())
    assert q1() == 11449
    assert q2() == 13187


if __name__ == "__main__":
    main()
