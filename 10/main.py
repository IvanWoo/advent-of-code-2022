import fileinput
from pathlib import Path
from collections import deque

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def get_registry_history():
    registry = 1
    cycle = 1
    history = dict({registry: cycle})
    queue = deque()
    programs = deque(get_input())
    while programs or queue:
        if not queue:
            program = programs.popleft()
            queue.append((program, cycle))
        cycle += 1
        cur_program, timestamp = queue[0]
        if cur_program.startswith("noop"):
            queue.popleft()
        else:
            if cycle - timestamp == 2:
                delta = int(cur_program.split()[1])
                registry += delta
                queue.popleft()
        history[cycle] = registry
    return history


def q1():
    history = get_registry_history()
    return sum([history[cycle] * cycle for cycle in range(20, 221, 40)])


def q2():
    def draw(pixels):
        count = 0
        cur_row = []
        for pixel in pixels:
            if count == 40:
                print("".join(cur_row))
                count = 0
                cur_row = []
            cur_row.append(pixel)
            count += 1
        print("".join(cur_row))

    history = get_registry_history()
    sprite_pos = 1
    pixels = []
    for cycle in range(1, 241):
        registry = history[cycle + 1]
        pixel = "."
        if abs(len(pixels) % 40 - sprite_pos) <= 1:
            pixel = "#"
        pixels.append(pixel)
        sprite_pos = registry
    draw(pixels)
    return "".join(pixels)


def main():
    print(q1())
    # print(q2())
    assert q1() == 17380
    # FGCUZREC
    assert (
        q2()
        == "####..##...##..#..#.####.###..####..##..#....#..#.#..#.#..#....#.#..#.#....#..#.###..#....#....#..#...#..#..#.###..#....#....#.##.#....#..#..#...###..#....#....#....#..#.#..#.#..#.#....#.#..#....#..#.#.....###..##...##..####.#..#.####..##.."
    )


if __name__ == "__main__":
    main()
