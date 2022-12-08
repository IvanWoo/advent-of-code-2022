import fileinput
from functools import reduce
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def q1():
    grid = list(get_input())
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if r in (0, rows - 1) or c in (0, cols - 1):
                count += 1
                continue
            val = grid[r][c]
            # left & right
            if max(grid[r][:c]) < val or max(grid[r][c + 1 :]) < val:
                count += 1
                continue

            col_vals = [rv[c] for rv in grid]
            # top & down
            if max(col_vals[:r]) < val or max(col_vals[r + 1 :]) < val:
                count += 1
                continue
    return count


def q2():
    grid = list(get_input())
    rows, cols = len(grid), len(grid[0])
    max_score = 0
    for r in range(rows):
        for c in range(cols):
            if r in (0, rows - 1) or c in (0, cols - 1):
                # always zero
                continue
            val = grid[r][c]
            views = []
            # left
            count = 0
            for _c in reversed(range(c)):
                count += 1
                if grid[r][_c] >= val:
                    break
            views.append(count)
            # right
            count = 0
            for _c in range(c + 1, cols):
                count += 1
                if grid[r][_c] >= val:
                    break
            views.append(count)
            # top
            count = 0
            for _r in reversed(range(r)):
                count += 1
                if grid[_r][c] >= val:
                    break
            views.append(count)
            # down
            count = 0
            for _r in range(r + 1, rows):
                count += 1
                if grid[_r][c] >= val:
                    break
            views.append(count)
            score = reduce((lambda x, y: x * y), views)
            max_score = max(max_score, score)

    return max_score


def main():
    print(q1())
    print(q2())
    assert q1() == 1801
    assert q2() == 209880


if __name__ == "__main__":
    main()
