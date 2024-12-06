from pathlib import Path
import numpy as np
from itertools import cycle

test_data = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

data = (Path(__file__).parent / "input").read_text()

def parse(data: str) -> tuple[tuple[int, int], np.ndarray]:
    obstacles = np.asarray([
        [True if c == "#" else False for c in line]
        for line in data.splitlines()
    ])
    for i, line in enumerate(data.splitlines()):
        for j in range(len(line)):
            if line[j] == "^":
                start = (i, j)
                break

    return start, obstacles

# Up, right, down, left
directions = ((-1, 0), (0, 1), (1, 0), (0, -1))

def my_print(obstacles, guard_map, current_pos):
    for i in range(obstacles.shape[0]):
        for j in range(obstacles.shape[1]):
            if (i, j) == current_pos:
                print("?", end="")
            elif guard_map[i, j]:
                print("+", end="")
            elif obstacles[i, j]:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()

def part1(start: tuple[int, int], obstacles: np.ndarray):

    cycle_dirs = cycle(directions)

    # Create map of positions of the guard
    guard_map = np.zeros_like(obstacles, dtype=bool)

    # Start direction is up
    direction = next(cycle_dirs)
    istep = 0
    i, j = start
    while i >= 0 and i < obstacles.shape[0] and j >= 0 and j < obstacles.shape[1]:
        if obstacles[i, j]:
            # Backtrack one, turn right
            i, j = i - direction[0], j - direction[1]
            direction = next(cycle_dirs)
        else:
            istep += 1
            guard_map[i, j] = True
            # Move forward
            i, j = i + direction[0], j + direction[1]

            # print(f"=== Step {istep} ")
            # my_print(obstacles, guard_map, (i, j))

    print(f"Part 1: {guard_map.sum()}")

start, obstacles = parse(data)

part1(start, obstacles)
