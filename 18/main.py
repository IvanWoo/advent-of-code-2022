import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    cubes = set()
    for row in get_input():
        cubes.add(tuple(map(int, row.split(","))))
    return cubes


DIRS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def q1():
    def surface_area(cubes):
        count = 0
        for x, y, z in cubes:
            for dx, dy, dz in DIRS:
                if (x + dx, y + dy, z + dz) not in cubes:
                    count += 1
        return count

    cubes = parse()
    return surface_area(cubes)


def q2():
    cubes = parse()
    xs, ys, zs = (
        [x for x, y, z in cubes],
        [y for x, y, z in cubes],
        [z for x, y, z in cubes],
    )
    minx, maxx = min(xs) - 1, max(xs) + 2
    miny, maxy = min(ys) - 1, max(ys) + 2
    minz, maxz = min(zs) - 1, max(zs) + 2

    water = set()
    tofill = [(minx, miny, minz)]
    while tofill:
        wx, wy, wz = tofill.pop()
        if (wx, wy, wz) in water or (wx, wy, wz) in cubes:
            continue
        water.add((wx, wy, wz))
        for dx, dy, dz in DIRS:
            nx, ny, nz = wx + dx, wy + dy, wz + dz
            if minx <= nx < maxx and miny <= ny < maxy and minz <= nz < maxz:
                tofill.append((nx, ny, nz))

    count = 0
    for x, y, z in cubes:
        for dx, dy, dz in DIRS:
            if (x + dx, y + dy, z + dz) in water:
                count += 1
    return count


def main():
    print(q1())
    print(q2())
    assert q1() == 3636
    assert q2() == 2102


if __name__ == "__main__":
    main()
