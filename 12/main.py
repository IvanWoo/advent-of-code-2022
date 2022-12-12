import fileinput
from collections import deque
from pathlib import Path
from math import inf

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def get_grid():
    grid = []
    for row in get_input():
        grid.append(list(row))
    rows, cols = len(grid), len(grid[0])
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
                grid[r][c] = "a"
            if grid[r][c] == "E":
                end = (r, c)
                grid[r][c] = "z"
    return start, end, grid


def bfs(start, end, grid):
    rows, cols = len(grid), len(grid[0])
    visited = set([start])
    queue = deque([(start, 0)])
    while queue:
        cur, steps = queue.popleft()
        if cur == end:
            return steps
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = cur
            nr, nc = r + dr, c + dc
            if (nr, nc) in visited:
                continue
            if 0 <= nr < rows and 0 <= nc < cols:
                cur_height = grid[r][c]
                nxt_height = grid[nr][nc]
                if nxt_height <= cur_height or ord(nxt_height) - ord(cur_height) == 1:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), steps + 1))
    return inf


def q1():
    start, end, grid = get_grid()

    return bfs(start, end, grid)


def q2():
    _, end, grid = get_grid()
    rows, cols = len(grid), len(grid[0])
    starts = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "a"]

    return min([bfs(start, end, grid) for start in starts])


def main():
    print(q1())
    print(q2())
    assert q1() == 481
    assert q2() == 480


if __name__ == "__main__":
    main()
