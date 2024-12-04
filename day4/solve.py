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

part1(parse(data))
