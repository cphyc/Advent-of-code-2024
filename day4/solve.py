from itertools import product
from pathlib import Path


test_data = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

data = (Path(__file__).parent / "input").read_text()

def parse(data: str) -> list[list[str]]:
    return [list(row) for row in data.splitlines()]

def _search(data: list[list[str]], i: int, j: int) -> int:
    if data[i][j] != "X":
        return 0

    hits = 0
    for di, dj in product((-1, 0, 1), repeat=2):
        if di == dj == 0:
            continue
        ii = i + di
        jj = j + dj
        my_list = []
        step = 0
        while step < 3 and ii >= 0 and ii < len(data) and jj >= 0 and jj < len(data[ii]):
            my_list.append(data[ii][jj])
            ii += di
            jj += dj
            step += 1

        if "".join(my_list) == "MAS":
            hits += 1
    return hits

def part1(data: list[list[str]]):
    hits = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            hits += _search(data, i, j)
    print(f"Part 1: {hits}")

def search_X(data: list[list[str]], i: int, j: int) -> bool:
    # Can't have an X-MAS without a central A
    if data[i][j] != "A":
        return False
    # Can't have an X-MAS on the border
    if i == 0 or i == len(data) - 1 or j == 0 or j == len(data[i]) - 1:
        return False

    diag_1 = "".join((data[i-1][j-1], data[i][j], data[i+1][j+1]))
    diag_2 = "".join((data[i-1][j+1], data[i][j], data[i+1][j-1]))

    if diag_1 in ("MAS", "SAM") and diag_2 in ("MAS", "SAM"):
        return True

    return False

def part2(data: list[list[str]]):
    hits = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if search_X(data, i, j):
                hits += 1
    print(f"Part 2: {hits}")

part1(parse(data))
part2(parse(data))
