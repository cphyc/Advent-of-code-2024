from dataclasses import dataclass
import enum
from pathlib import Path


test_data_0 = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

test_data = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

data = (Path(__file__).parent / "input").read_text()

class Movement(enum.Enum):
    LEFT = (-1, 0)
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)

    @classmethod
    def from_char(cls, c: str) -> "Movement":
        return {
            "^": cls.UP,
            ">": cls.RIGHT,
            "v": cls.DOWN,
            "<": cls.LEFT,
        }[c]

class Stuff(enum.Enum):
    WALL = "#"
    BOX = "O"
    EMPTY = "."
    ROBOT = "@"

    @classmethod
    def from_char(cls, c: str) -> "Stuff":
        return {
            "#": cls.WALL,
            "O": cls.BOX,
            ".": cls.EMPTY,
            "@": cls.ROBOT,
        }[c]


@dataclass
class Map:
    objects: dict[tuple[int, int], Stuff]
    robot_position: tuple[int, int]

    @staticmethod
    def from_str(objects_str: str) -> "Map":
        objects: dict[tuple[int, int], Stuff] = {}
        for i, line in enumerate(objects_str.splitlines()):
            for j, c in enumerate(line):
                s = Stuff.from_char(c)
                if s is Stuff.ROBOT:
                    robot_pos = (j, i)
                elif s != Stuff.EMPTY:
                    objects[j, i] = s

        return Map(objects, robot_pos)

    def move(self, mv: Movement):
        old_pos = self.robot_position
        new_pos = (old_pos[0] + mv.value[0], old_pos[1] + mv.value[1])

        if new_pos not in self.objects:
            # New position is empty
            return Map(self.objects, new_pos)
        # Otherwise, get a stack of boxes to push
        next_pos = new_pos
        box_stack = []

        # Get stack of box to be moved
        while (box := self.objects.get(next_pos, Stuff.EMPTY)) == Stuff.BOX:
            box_stack.append(next_pos)
            next_pos = (next_pos[0] + mv.value[0], next_pos[1] + mv.value[1])

        if box == Stuff.EMPTY:
            # If we hit an empty space, move the boxes
            new_box_stack: list[tuple[int, int]] = []
            for p in box_stack:
                new_box_stack.append((p[0] + mv.value[0], p[1] + mv.value[1]))
                self.objects.pop(p)
            # Add back the boxes at shifted positions
            for p in new_box_stack:
                self.objects[p] = Stuff.BOX
            return Map(self.objects, new_pos)
        elif box == Stuff.WALL:
            return Map(self.objects, old_pos)

    def print(self):
        imax = max(self.objects.keys(), key=lambda ij: ij[0])[0]
        jmax = max(self.objects.keys(), key=lambda ij: ij[1])[1]

        for j in range(jmax + 1):
            chars = ""
            for i in range(imax + 1):
                obj = self.objects.get((i, j), Stuff.EMPTY)

                if (i, j) == self.robot_position:
                    chars += "@"
                elif obj == Stuff.EMPTY:
                    chars += "."
                elif obj == Stuff.BOX:
                    chars += "O"
                elif obj == Stuff.WALL:
                    chars += "#"
            print(chars)

    def get_score(self) -> int:
        score = 0
        for key, val in self.objects.items():
            if val != Stuff.BOX:
                continue

            score += key[1] * 100 + key[0]
        return score


def parse(data: str) -> tuple[Map, list[Movement]]:
    map_str, movement_str = data.split("\n\n")

    movements = [Movement.from_char(c) for c in movement_str.replace("\n", "")]
    object_map = Map.from_str(map_str)

    return object_map, movements

om, movements = parse(data)

for m in movements:
    om = om.move(m)
    # print(f" {m=} ".center(40, "="))
    # om.print()

print(f"Part 1: {om.get_score()}")
