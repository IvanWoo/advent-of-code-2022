import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def q1():
    count = 0
    for row in get_input():
        a, b = row.split(",")
        a1, a2 = [int(x) for x in a.split("-")]
        b1, b2 = [int(x) for x in b.split("-")]
        if (a1 >= b1 and a2 <= b2) or (b1 >= a1 and b2 <= a2):
            count += 1
    return count


def q2():
    count = 0
    for row in get_input():
        a, b = row.split(",")
        a1, a2 = [int(x) for x in a.split("-")]
        b1, b2 = [int(x) for x in b.split("-")]
        if set(range(a1, a2 + 1)) & set(range(b1, b2 + 1)):
            count += 1
    return count


def main():
    print(q1())
    print(q2())
    assert q1() == 567
    assert q2() == 907


if __name__ == "__main__":
    main()
