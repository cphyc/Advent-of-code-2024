from pathlib import Path
import re

MUL_RE = re.compile(r"mul\((\d+),(\d+)\)")


test_data = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"


data = (Path(__file__).parent / "input").read_text()


def part1(data: str):
    sum = 0
    for a, b in MUL_RE.findall(data):
        sum += int(a) * int(b)
    print(f"Part 1: {sum}")

part1(data)
