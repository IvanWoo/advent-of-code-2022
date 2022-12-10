import fileinput
from itertools import product
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip().split()


DIR_MAPPING = dict(R=(1, 0), L=(-1, 0), U=(0, 1), D=(0, -1))


def move(pos, dir_v):
    return (pos[0] + dir_v[0], pos[1] + dir_v[1])


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x2 - x1) ** 2 + (y2 - y1) ** 2


def q1():
    def sim(head, tail, dir: str, step: int):
        visited = set()
        visited.add(tail)
        dir_v = DIR_MAPPING[dir]
        for _ in range(step):
            prev_head = head
            head = move(head, dir_v)
            dist = distance(head, tail)
            if dist < 4:
                # no move
                continue
            tail = prev_head
            visited.add(tail)
        return head, tail, visited

    head = tail = (0, 0)
    visited = set()
    for dir, step in get_input():
        head, tail, new_visited = sim(head, tail, dir, int(step))
        visited |= new_visited
    return len(visited)


def q2():
    def get_new_tail(head, tail):
        dist = distance(head, tail)
        if dist < 4:
            # no move
            return tail
        res = tail
        min_dist = dist
        for dx, dy in product([-1, 0, 1], repeat=2):
            tx, ty = tail
            new_tail = tx + dx, ty + dy
            new_dist = distance(head, new_tail)
            if new_dist < min_dist:
                min_dist = new_dist
                res = new_tail
        return res

    total = 10
    knots = [(0, 0)] * total
    visited = set([(0, 0)])
    for dir, step in get_input():
        dir_v = DIR_MAPPING[dir]
        for _ in range(int(step)):
            knots[0] = move(knots[0], dir_v)
            for i in range(total - 1):
                head, tail = knots[i], knots[i + 1]
                knots[i + 1] = get_new_tail(head, tail)
            visited.add(knots[-1])
    return len(visited)


def main():
    print(q1())
    print(q2())
    assert q1() == 6090
    assert q2() == 2566


if __name__ == "__main__":
    main()
