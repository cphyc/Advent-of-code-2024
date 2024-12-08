from itertools import combinations
from pathlib import Path
import numpy as np

test_data = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
data = (Path(__file__).parent / "input").read_text()


def parse(data: str) -> np.ndarray:
    return np.asarray([
        [-1 if c == "." else ord(c) for c in line]
        for line in data.splitlines()
    ])

def part1(antennas: np.ndarray):
    antinodes = np.zeros_like(antennas)
    # Find unique antennas
    ids = np.unique(antennas[antennas != -1])
    for id in ids:
        all_i, all_j = np.asarray(np.nonzero(antennas == id))
        for ij1, ij2 in combinations(zip(all_i, all_j), r=2):
            di = ij2[0] - ij1[0]
            dj = ij2[1] - ij1[1]

            if ij1[0] - di >= 0 and ij1[0] - di < antennas.shape[0] and ij1[1] - dj >= 0 and ij1[1] - dj < antennas.shape[1]:
                antinodes[ij1[0] - di, ij1[1] - dj] = 1
            if ij2[0] + di >= 0 and ij2[0] + di < antennas.shape[0] and ij2[1] + dj >= 0 and ij2[1] + dj < antennas.shape[1]:
                antinodes[ij2[0] + di, ij2[1] + dj] = 1

    print(f"Part 1: {np.sum(antinodes)}")

antennas = parse(data)
part1(antennas)
