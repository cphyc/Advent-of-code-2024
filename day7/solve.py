from itertools import product
from operator import add, mul
from pathlib import Path

from tqdm import tqdm

test_data = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

data = (Path(__file__).parent / "input").read_text()

def parse(data: str) -> dict[int, list[int]]:
    ret = {}

    for line in data.splitlines():
        k, v = line.split(": ")
        ret[int(k)] = [int(x) for x in v.split()]

    return ret

def part1(equations: dict[int, list[int]]):
    ok: dict[int, bool] = {}

    for key, values in equations.items():
        ok[key] = False
        tot = values[0]
        for operations in product((mul, add), repeat=len(values) - 1):
            tot = values[0]
            for op, val in zip(operations, values[1:]):
                tot = op(tot, val)

            if tot == key:
                ok[key] = True
                break

    print(f"Part 1: {sum(k for k, v in ok.items() if v)}")

def concat(a, b):
    return int(str(a) + str(b))

def part2(equations: dict[int, list[int]]):
    ok: dict[int, bool] = {}

    for key, values in tqdm(equations.items()):
        ok[key] = False
        tot = values[0]
        for operations in product((mul, add, concat), repeat=len(values) - 1):
            tot = values[0]
            for op, val in zip(operations, values[1:]):
                tot = op(tot, val)
                if tot > key:
                    break

            if tot == key:
                ok[key] = True
                break

    print(f"Part 2: {sum(k for k, v in ok.items() if v)}")

equations = parse(data)
part1(equations)
part2(equations)
