from pathlib import Path
import numpy as np


test_data = """\
3   4
4   3
2   5
1   3
3   9
3   3"""

def part1(data):
    data = np.array([[int(_) for _ in line.split()] for line in data.splitlines()])

    L, R = data.T
    L, R = np.sort(L), np.sort(R)

    print(f"Part 1: {np.abs(R - L).sum()}")

data = Path("input").read_text()
part1(data)