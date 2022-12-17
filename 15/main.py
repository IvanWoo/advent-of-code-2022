import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def extract(s):
    head, tail = s.split(",")
    return int(head.split("=")[-1]), int(tail.split("=")[-1])


def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def parse():
    reports = []
    for row in get_input():
        sensor, beacon = row.split(":")
        sp, bp = extract(sensor), extract(beacon)
        reports.append((sp, bp, dist(sp, bp)))
    return reports


def merge(intervals):
    if len(intervals) == 0:
        return []
    ans = []
    for s, e in sorted(intervals):
        if not ans or s > ans[-1][1]:
            ans.append([s, e])
        else:
            ans[-1][1] = max(ans[-1][1], e)
    return ans


def get_safe_zone(reports, target_y: int):
    safe_zone = []
    for sp, _, distance in reports:
        x, y = sp
        buffer = abs(y - target_y)
        if buffer < distance:
            diff = distance - buffer
            safe_zone.append([x - diff, x + diff + 1])
    return merge(safe_zone)


def q1():
    reports = parse()
    safe_zone = []
    target_y = 2000000
    occupied = set()
    for sp, bp, distance in reports:
        if sp[1] == target_y:
            occupied.add(sp)
        if bp[1] == target_y:
            occupied.add(bp)
    safe_zone = get_safe_zone(reports, target_y)
    res = 0
    for s, e in safe_zone:
        res += e - s
    return res - len(occupied)


def q2():
    reports = parse()
    for target_y in range(4000000 + 1):
        safe_zone = get_safe_zone(reports, target_y)
        if len(safe_zone) == 2:
            return safe_zone[0][1] * 4000000 + target_y


def main():
    print(q1())
    print(q2())
    assert q1() == 5256611
    assert q2() == 13337919186981


if __name__ == "__main__":
    main()
