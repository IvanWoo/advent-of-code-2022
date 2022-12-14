import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line


def get_count():
    count = []
    cur_total = 0
    for line in get_input():
        if line == "\n":
            count.append(cur_total)
            cur_total = 0
            continue
        cur_total += int(line)
    count.append(cur_total)
    return sorted(count)


def q1():
    count = get_count()
    return count[-1]


def q2():
    count = get_count()
    return sum(count[-3:])


def main():
    print(q1())
    print(q2())
    assert q1() == 71471
    assert q2() == 211189


if __name__ == "__main__":
    main()
