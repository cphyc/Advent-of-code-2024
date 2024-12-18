from copy import copy
from pathlib import Path
import numpy as np


test_data = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

data = (Path(__file__).parent / "input").read_text()

def parse(data: str) -> list[list[int]]:
    return [[int(_) for _ in line.split()] for line in data.splitlines()]

def part1(data: list[list[int]]) -> int:
    count = 0
    for report in data:
        diff = np.diff(report)
        sign = np.sign(diff[0])
        if np.all(diff * sign >= 1) & np.all(diff * sign <= 3):
            count += 1

    print(f"Part 1: {count}")
    return count

def part2(data: list[list[int]]) -> int:
    count = 0
    for report in data:
        for i in range(len(report)):
            subreport = copy(report)
            if i >= 0:
                subreport.pop(i)
            diff = np.diff(subreport)
            sign = np.sign(diff[0])
            if np.all(diff * sign >= 1) & np.all(diff * sign <= 3):
                count += 1
                break

    print(f"Part 2: {count}")
    return count


part1(parse(data))
part2(parse(data))
