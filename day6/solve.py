from pathlib import Path
import numpy as np
from itertools import cycle

from tqdm import tqdm

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
            elif guard_map[i, j].any():
                print("+", end="")
            elif obstacles[i, j]:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()

def walk(start: tuple[int, int], obstacles: np.ndarray):

    cycle_dirs = cycle(enumerate(directions))

    # Create map of positions of the guard
    guard_map = np.zeros((*obstacles.shape, 4), dtype=bool)

    # Start direction is up
    idir, direction = next(cycle_dirs)
    istep = 0
    i, j = start
    loop = False
    while i >= 0 and i < obstacles.shape[0] and j >= 0 and j < obstacles.shape[1]:
        if obstacles[i, j]:
            # Backtrack one, turn right
            i, j = i - direction[0], j - direction[1]
            idir, direction = next(cycle_dirs)
        else:
            istep += 1
            if guard_map[i, j, idir]:
                # We found a loop
                loop = True
                break

            # Mark position
            guard_map[i, j, idir] = True

            # Move forward
            i, j = i + direction[0], j + direction[1]

    return guard_map, loop

def part1(start: tuple[int, int], obstacles: np.ndarray):
    guard_map, _ = walk(start, obstacles)
    print(f"Part 1: {guard_map.max(axis=-1).sum()}")

def part2(start: tuple[int, int], obstacles: np.ndarray):
    Nloop = 0
    for i in tqdm(range(obstacles.shape[0])):
        for j in range(obstacles.shape[1]):
            if obstacles[i, j]:
                # There is already an obstacle, do nothing
                continue
            elif (i, j) == start:
                # The guard starts here, do nothing
                continue

            # Otherwise, add a new (temporary) obstacle
            new_obstacles = obstacles.copy()
            new_obstacles[i, j] = True

            _, loop = walk(start, new_obstacles)
            Nloop += loop
    print(f"part 2: {Nloop}")

start, obstacles = parse(data)

part1(start, obstacles)
part2(start, obstacles)
