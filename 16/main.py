import fileinput
from pathlib import Path
from functools import cache

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def _parse_nxt_valves(s):
    parts = s.split()
    return set([parts[-1]] + [p[:-1] for p in parts if p.endswith(",")])


def parse():
    rates = {}
    valves = {}
    for row in get_input():
        head, tail = row.split(";")
        cur_valve = head[6:8]
        rate = int(head.split("=")[-1])
        nxt_valves = _parse_nxt_valves(tail)
        rates[cur_valve] = rate
        valves[cur_valve] = nxt_valves
    return rates, valves


def q1():
    @cache
    def backtrack(left: int, cur_valve: str, opened_valve):
        if left == 0:
            return 0
        total_flow_rate = sum(rates[v] for v in opened_valve)
        if total_flow_rate == max_rate:
            return left * total_flow_rate
        candidates = []
        if rates[cur_valve] != 0 and cur_valve not in opened_valve:
            candidates.append(
                backtrack(left - 1, cur_valve, (*opened_valve, cur_valve))
            )
        for nxt_valve in valves[cur_valve]:
            candidates.append(backtrack(left - 1, nxt_valve, opened_valve))
        return max(candidates) + total_flow_rate

    start_valve = "AA"
    rates, valves = parse()
    max_rate = sum(rates.values())
    return backtrack(30, start_valve, ())


def q2():
    @cache
    def backtrack(left: int, cur, cur_e, opened_valve):
        if left == 0:
            return 0
        total_flow_rate = sum(rates[v] for v in opened_valve)
        if total_flow_rate == max_rate:
            return left * total_flow_rate
        candidates = []
        # open open
        if (rates[cur] != 0 and cur not in opened_valve) and (
            rates[cur_e] != 0 and cur_e not in opened_valve
        ):
            if cur != cur_e:
                candidates.append(
                    backtrack(
                        left - 1, cur, cur_e, tuple(sorted((*opened_valve, cur, cur_e)))
                    )
                )
            else:
                candidates.append(
                    backtrack(left - 1, cur, cur_e, tuple(sorted((*opened_valve, cur))))
                )
        elif rates[cur] != 0 and cur not in opened_valve:
            candidates.append(
                backtrack(left - 1, cur, cur_e, tuple(sorted((*opened_valve, cur)))),
            )
        elif rates[cur_e] != 0 and cur_e not in opened_valve:
            candidates.append(
                backtrack(left - 1, cur, cur_e, tuple(sorted((*opened_valve, cur_e)))),
            )
        # open move
        if rates[cur] != 0 and cur not in opened_valve:
            for nxt_e in valves[cur_e]:
                candidates.append(
                    backtrack(left - 1, cur, nxt_e, tuple(sorted((*opened_valve, cur))))
                )
        # move open
        if rates[cur_e] != 0 and cur_e not in opened_valve:
            for nxt in valves[cur]:
                candidates.append(
                    backtrack(
                        left - 1, nxt, cur_e, tuple(sorted((*opened_valve, cur_e)))
                    )
                )
        # move move
        for nxt in valves[cur]:
            for nxt_e in valves[cur_e]:
                candidates.append(backtrack(left - 1, nxt, nxt_e, opened_valve))
        return max(candidates) + total_flow_rate

    start_valve = "AA"
    rates, valves = parse()
    max_rate = sum(rates.values())
    return backtrack(26, start_valve, start_valve, ())


def main():
    print(q1())
    print(q2())
    # assert q1() == 1460
    # not be able to compute q2 in 1 hour after using 30 GB memory
    # assert q2() == 42


if __name__ == "__main__":
    main()
