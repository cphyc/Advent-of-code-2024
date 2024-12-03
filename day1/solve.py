from pathlib import Path
import numpy as np


test_data = """\
3   4
4   3
2   5
1   3
3   9
3   3"""

def parse(data):
    return np.array([[int(_) for _ in line.split()] for line in data.splitlines()])

def part1(data):
    data = parse(data)

    L, R = data.T
    L, R = np.sort(L), np.sort(R)

    print(f"Part 1: {np.abs(R - L).sum()}")

def part2(data):
    data = parse(data)

    L, R = data.T

    count = 0
    for n in L:
        count += n * (R == n).sum()

    print(f"Part 2: {count}")

data = Path("input").read_text()
part1(data)
part2(data)