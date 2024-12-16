from collections import namedtuple
from itertools import batched
from pathlib import Path

test_data = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

data = (Path(__file__).parent / "input").read_text()

Point = namedtuple("Point", ["x", "y"])

def parse(data: str):
    lines = data.splitlines()

    def parse_button(line):
        name, coords = line.split(":")
        x, y = coords.split(", ")
        return Point(int(x.split("+")[1]), int(y.split("+")[1]))
    def parse_prize(line):
        x, y = line.split(": ")[1].split(", ")
        return Point(int(x.split("=")[1]), int(y.split("=")[1]))

    for lA, lB, lprize, *_skip in batched(lines, 4):
        A = parse_button(lA)
        B = parse_button(lB)
        prize = parse_prize(lprize)

        yield A, B, prize

def solve(A: Point, B: Point, prize: Point):
    nA = max(min(prize.x // A.x, prize.y // A.y), 100)
    nB = max(min(prize.x // B.x, prize.y // B.y), 100)

    solutions = []
    for i in range(nA + 1):
        for j in range(nB + 1):
            if i * A.x + j * B.x == prize.x and i * A.y + j * B.y == prize.y:
                solutions.append((i, j))

    if solutions:
        # Find the solution with the smallest number of steps
        return min(solutions, key=sum)
    else:
        return (-1, -1)


def part1(data):
    total = 0
    for A, B, prize in data:
        i, j = solve(A, B, prize)
        if i == -1:
            # print(f"No solution for {A=}, {B=}, {prize=}")
            continue
        total += 3 * i + j
        print(f"Button A: {i}, Button B: {j}, cost = {3 * i + j}")

    print(f"Part 1: {total}")



part1(parse(data))
