from pathlib import Path
import re
from typing import Literal

MUL_RE = re.compile(r"mul\((\d+),(\d+)\)")
DO_RE = re.compile(r"do\(\)")
DONT_RE = re.compile(r"don't\(\)")


test_data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


data = (Path(__file__).parent / "input").read_text()


def part1(data: str):
    sum = 0
    for a, b in MUL_RE.findall(data):
        sum += int(a) * int(b)
    print(f"Part 1: {sum}")

def part2(data: str):
    state: Literal["DO", "DONT"] = "DO"
    sum = 0
    i = 0

    while i < len(data):
        if state == "DO":
            # Find next DONT
            match = DONT_RE.search(data, i)
            if not match:
                iend = len(data)
            else:
                iend = match.end()

            # Search for operations in between
            for match in MUL_RE.finditer(data, i, iend):
                sum += int(match.group(1)) * int(match.group(2))

            i = iend
            # print(f"At position {i=}, switching to DONT")
            state = "DONT"
        else:
            # Find next DO
            match = DO_RE.search(data, i)
            if not match:
                break

            i = match.end()
            # print(f"At position {i=}, switching to DO")
            state = "DO"
    print(f"Part 2: {sum}")

part1(data)
part2(data)
