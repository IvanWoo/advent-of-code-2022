import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def get_priority(items: list[str]) -> int:
    return sum(
        [
            ord(char) - (ord("a") - 1 if char.islower() else ord("A") - 27)
            for char in items
        ]
    )


def q1():
    overlaps = []
    for line in get_input():
        mid = len(line) // 2
        head, tail = line[:mid], line[mid:]
        overlap = list(set(head) & set(tail))[0]
        overlaps.append(overlap)
    return get_priority(overlaps)


def q2():
    lines = list(get_input())
    n = len(lines)
    overlaps = []
    for i in range(0, n, 3):
        a, b, c = lines[i : i + 3]
        overlap = list(set(a) & set(b) & set(c))[0]
        overlaps.append(overlap)
    return get_priority(overlaps)


def main():
    print(q1())
    print(q2())
    assert q1() == 7553
    assert q2() == 2758


if __name__ == "__main__":
    main()
