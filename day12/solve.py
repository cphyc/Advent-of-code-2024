from pathlib import Path
import numpy as np

test_data = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

data = (Path(__file__).parent / "input").read_text()


def parse(data: str) -> np.ndarray:
    return np.asarray([[ord(c) for c in line] for line in data.splitlines()])


def walk(garden: np.ndarray, i: int, j: int, label: int, labels: np.ndarray) -> tuple[int, int]:
    if labels[i, j] != -1:
        return 0, 0
    labels[i, j] = label
    surface, edge = 1, 0
    if i > 0 and garden[i-1, j] == garden[i, j]:
        s, e = walk(garden, i-1, j, label, labels)
        surface += s
        edge += e
    else:
        edge += 1
    if i < garden.shape[0] - 1 and garden[i+1, j] == garden[i, j]:
        s, e = walk(garden, i+1, j, label, labels)
        surface += s
        edge += e
    else:
        edge += 1
    if j > 0 and garden[i, j-1] == garden[i, j]:
        s, e = walk(garden, i, j-1, label, labels)
        surface += s
        edge += e
    else:
        edge += 1
    if j < garden.shape[1] - 1 and garden[i, j+1] == garden[i, j]:
        s, e = walk(garden, i, j+1, label, labels)
        surface += s
        edge += e
    else:
        edge += 1
    return surface, edge


def part1(garden: np.ndarray):
    labels = np.full_like(garden, -1, dtype=int)

    ilabel = 0
    total = 0
    for i in range(garden.shape[0]):
        for j in range(garden.shape[1]):
            surface, edge = walk(garden, i, j, ilabel, labels)
            if surface > 0:
                # v = chr(garden[i, j])
                # print(f"{v}, {surface=:3d} {edge=:3d}")
                total += surface * edge
                ilabel += 1

    print(f"Part 1: {total}")


garden = parse(data)
part1(garden)
