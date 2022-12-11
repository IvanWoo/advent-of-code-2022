import math
from pathlib import Path
from dataclasses import dataclass, field

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with open(INPUT_FILE) as f:
        return "".join(f.read()).split("\n\n")


@dataclass
class Monkey:
    items: list[int] = field(default_factory=list)
    op_func: any = None
    divisor: int = 1
    test_func: any = None


def parse_one(content: str) -> Monkey:
    lines = content.split("\n")
    # print(lines)
    items = list(map(int, lines[1].split(":")[1].strip().split(",")))
    op_func = lambda old: eval(lines[2].split(" = ")[1])
    divisor = int(lines[3].split()[-1])
    test_func = lambda x: int(lines[4][-1]) if x % divisor == 0 else int(lines[5][-1])
    return Monkey(items, op_func, divisor, test_func)


def parse():
    monkeys = [parse_one(c) for c in get_input()]
    return monkeys


def q1():
    monkeys = parse()
    inspect_count = [0] * len(monkeys)
    for _ in range(20):
        for i, monkey in enumerate(monkeys):
            items = monkey.items
            if not items:
                continue
            for item in items:
                new_item = monkey.op_func(item)
                new_item //= 3
                nxt_monkey_idx = monkey.test_func(new_item)
                monkeys[nxt_monkey_idx].items.append(new_item)
                inspect_count[i] += 1
            monkey.items = []
        # print([m.items for m in monkeys])

    return math.prod(sorted(inspect_count)[-2:])


def q2():
    monkeys = parse()
    inspect_count = [0] * len(monkeys)
    divisor = math.prod([m.divisor for m in monkeys])
    for r in range(10000):
        # if r in [1, 20, 1000, 2000]:
        #     print(inspect_count)
        for i, monkey in enumerate(monkeys):
            items = monkey.items
            if not items:
                continue
            for item in items:
                new_item = monkey.op_func(item)
                new_item %= divisor
                nxt_monkey_idx = monkey.test_func(new_item)
                monkeys[nxt_monkey_idx].items.append(new_item)
                inspect_count[i] += 1
            monkey.items = []
        # print([m.items for m in monkeys])

    return math.prod(sorted(inspect_count)[-2:])


def main():
    print(q1())
    print(q2())
    assert q1() == 95472
    assert q2() == 17926061332


if __name__ == "__main__":
    main()
