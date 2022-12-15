import fileinput
from pathlib import Path

from sortedcontainers import SortedSet

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def min_max(v1, v2):
    return (min(v1, v2), max(v1, v2) + 1)


def debug(boundary, sands):
    xs, ys = [x for x, _ in boundary], [y for _, y in boundary]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = 0, max(ys)
    grid = [["."] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for y in range(max_y - min_y + 1):
        for x in range(max_x - min_x + 1):
            if (x + min_x, y + min_y) in boundary:
                grid[y][x] = "#"
            if (x + min_x, y + min_y) in sands:
                grid[y][x] = "o"
    print("\n".join(["".join(row) for row in grid]))
    print("\n")


def get_all_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        return set([(x1, y) for y in range(*min_max(y1, y2))])
    if y1 == y2:
        return set([(x, y1) for x in range(*min_max(x1, x2))])


def get_boundary():
    boundary = SortedSet()
    for line in get_input():
        pts = [eval(pt) for pt in line.split(" -> ")]
        for i in range(1, len(pts)):
            boundary |= get_all_points(pts[i - 1], pts[i])
    return boundary


def simulate(start, boundary):
    xs = [x for x, _ in boundary]
    min_x, max_x = min(xs), max(xs)
    sands = set()
    # debug(boundary, sands)
    while True:
        cx, cy = start
        if start in sands:
            break
        added = False
        while True:
            still = True
            for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
                if not still:
                    continue
                nx, ny = cx + dx, cy + dy
                if (nx, ny) not in boundary:
                    cx, cy = nx, ny
                    still = False
            if not (min_x <= cx <= max_x):
                break
            if still:
                boundary.add((cx, cy))
                sands.add((cx, cy))
                added = True
                # print(f"added {cx, cy}")
                # debug(boundary, sands)
                break
        if not added:
            break
    return sands


def q1():
    start = (500, 0)
    boundary = get_boundary()
    sands = simulate(start, boundary)
    return len(sands)


def q2():
    start = (500, 0)
    boundary = get_boundary()
    xs = [x for x, _ in boundary]
    ys = [y for _, y in boundary]
    min_x, max_x = min(xs), max(xs)
    max_y = max(ys)
    padding = max_y * 2
    new_boundary = set(boundary)
    for x in range(min_x - padding, max_x + padding):
        new_boundary.add((x, max_y + 2))
    sands = simulate(start, new_boundary)
    return len(sands)


def main():
    print(q1())
    print(q2())
    assert q1() == 994
    assert q2() == 26283


if __name__ == "__main__":
    main()
