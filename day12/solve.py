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


def walk(
    garden: np.ndarray, i: int, j: int, label: int, labels: np.ndarray
) -> tuple[int, int, list[tuple[int, int]]]:
    if labels[i, j] != -1:
        return 0, 0, []
    labels[i, j] = label
    cells = [(i, j)]
    surface, edge = 1, 0
    if i > 0 and garden[i - 1, j] == garden[i, j]:
        s, e, c = walk(garden, i - 1, j, label, labels)
        surface += s
        edge += e
        cells += c
    else:
        edge += 1
    if i < garden.shape[0] - 1 and garden[i + 1, j] == garden[i, j]:
        s, e, c = walk(garden, i + 1, j, label, labels)
        surface += s
        edge += e
        cells += c
    else:
        edge += 1
    if j > 0 and garden[i, j - 1] == garden[i, j]:
        s, e, c = walk(garden, i, j - 1, label, labels)
        surface += s
        edge += e
        cells += c
    else:
        edge += 1
    if j < garden.shape[1] - 1 and garden[i, j + 1] == garden[i, j]:
        s, e, c = walk(garden, i, j + 1, label, labels)
        surface += s
        edge += e
        cells += c
    else:
        edge += 1

    assert len(cells) == surface
    return surface, edge, cells


def part1(garden: np.ndarray):
    labels = np.full_like(garden, -1, dtype=int)

    ilabel = 0
    total = 0
    for i in range(garden.shape[0]):
        for j in range(garden.shape[1]):
            surface, edge, _ = walk(garden, i, j, ilabel, labels)
            if surface > 0:
                total += surface * edge
                ilabel += 1

    print(f"Part 1: {total}")


def part2(garden: np.ndarray):
    labels = np.full_like(garden, -1, dtype=int)

    ilabel = 0
    total = 0
    for i in range(garden.shape[0]):
        for j in range(garden.shape[1]):
            surface, edge, cells = walk(garden, i, j, ilabel, labels)
            if not surface:
                continue

            Nfaces = 0
            for d in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                # Normal vector
                n = (d[1], d[0])

                # Find cells that are at the edge
                tmp = {
                    (i, j)
                    for i, j in cells
                    if (i + d[0], j + d[1]) not in cells
                }

                # Count number of contiguous cells
                while tmp:
                    ii, jj = tmp.pop()
                    Nfaces += 1
                    iii, jjj = ii, jj
                    while (iii + n[0], jjj + n[1]) in tmp:
                        iii += n[0]
                        jjj += n[1]
                        tmp.remove((iii, jjj))
                    iii, jjj = ii, jj
                    while (iii - n[0], jjj - n[1]) in tmp:
                        iii -= n[0]
                        jjj -= n[1]
                        tmp.remove((iii, jjj))

            total += surface * Nfaces
            ilabel += 1


    print(f"Part 2: {total}")


garden = parse(data)
part1(garden)
part2(garden)
