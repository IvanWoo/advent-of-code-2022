import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def get_first_marker_idx(total_distinct: int) -> int:
    packets = list(get_input())[0]
    n = len(packets)
    for i in range(total_distinct, n):
        window = packets[i - total_distinct : i]
        if len(set(window)) == len(window):
            return i


def q1():
    return get_first_marker_idx(4)


def q2():
    return get_first_marker_idx(14)


def main():
    print(q1())
    print(q2())
    assert q1() == 1623
    assert q2() == 3774


if __name__ == "__main__":
    main()
