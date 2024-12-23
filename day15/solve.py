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
    BBOXL = "["
    BBOXR = "]"

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

    def move2(self, mv: Movement):
        old_pos = self.robot_position
        new_pos = (old_pos[0] + mv.value[0], old_pos[1] + mv.value[1])

        if new_pos not in self.objects:
            # New position is empty
            return Map(self.objects, new_pos)
        # Otherwise, get a stack of boxes to push
        next_pos = new_pos
        box_stack = []

        # If moving up/down, all big boxes need to align
        if mv in (Movement.UP, Movement.DOWN):
            first_box = self.objects.get(next_pos, Stuff.EMPTY)
            factor = 1
        else:
            first_box = Stuff.BBOXL if mv == Movement.RIGHT else Stuff.BBOXR
            factor = 2
        if first_box == Stuff.BBOXL:
            next_posL, next_posR = next_pos, (next_pos[0] + 1, next_pos[1])
        else:
            next_posL, next_posR = (next_pos[0] - 1, next_pos[1]), next_pos

        boxL, boxR = None, None

        # Get stack of BIG box to be moved
        while (
            (
                (boxL := self.objects.get(next_posL, Stuff.EMPTY)),
                (boxR := self.objects.get(next_posR, Stuff.EMPTY))
            ) == (Stuff.BBOXL, Stuff.BBOXR)
        ):
            box_stack.append(next_posL)
            box_stack.append(next_posR)

            next_posL = (next_posL[0] + mv.value[0] * factor, next_posL[1] + mv.value[1] * factor)
            next_posR = (next_posR[0] + mv.value[0] * factor, next_posR[1] + mv.value[1] * factor)

        # If we're moving sideways, need to subtract one step
        if mv in (Movement.RIGHT, Movement.LEFT):
            next_posL = (next_posL[0] - mv.value[0], next_posL[1] - mv.value[1])
            next_posR = (next_posR[0] - mv.value[0], next_posR[1] - mv.value[1])
            boxL = self.objects.get(next_posL, Stuff.EMPTY)
            boxR = self.objects.get(next_posR, Stuff.EMPTY)

        ok = (
            ((boxL, boxR) == (Stuff.BBOXR, Stuff.EMPTY) and mv == Movement.RIGHT) or
            ((boxL, boxR) == (Stuff.EMPTY, Stuff.BBOXL) and mv == Movement.LEFT) or
            ((boxL, boxR) == (Stuff.EMPTY, Stuff.EMPTY) and mv in (Movement.UP, Movement.DOWN))
        )
        if ok:
            # If we hit an empty space, move the boxes
            new_box_stack: list[tuple[tuple[int, int], Stuff]] = []
            for p in box_stack:
                s = self.objects.pop(p)
                new_box_stack.append(
                    ((p[0] + mv.value[0], p[1] + mv.value[1]), s)
                )
            # Add back the boxes at shifted positions
            for p, s in new_box_stack:
                self.objects[p] = s
            return Map(self.objects, new_pos)
        else:
            # Can't move if we hit a wall/unaligned boxes
            return Map(self.objects, old_pos)


    def print(self, mvmt: Movement=None):
        imax = max(self.objects.keys(), key=lambda ij: ij[0])[0]
        jmax = max(self.objects.keys(), key=lambda ij: ij[1])[1]

        for j in range(jmax + 1):
            chars = ""
            for i in range(imax + 1):
                obj = self.objects.get((i, j), Stuff.EMPTY)

                if (i, j) == self.robot_position:
                    c = {
                        None: "@",
                        Movement.LEFT: "<",
                        Movement.RIGHT: ">",
                        Movement.UP: "^",
                        Movement.DOWN: "v",
                    }[mvmt]
                    chars += c
                elif obj == Stuff.EMPTY:
                    chars += "."
                elif obj == Stuff.BOX:
                    chars += "O"
                elif obj == Stuff.WALL:
                    chars += "#"
                elif obj == Stuff.BBOXL:
                    chars += "["
                elif obj == Stuff.BBOXR:
                    chars += "]"
            print(chars)

    def get_score(self) -> int:
        score = 0
        for key, val in self.objects.items():
            if val != Stuff.BOX:
                continue

            score += key[1] * 100 + key[0]
        return score

    def double(self) -> "Map":
        new_objects: dict[tuple[int, int], Stuff] = {}

        for key, val in self.objects.items():
            key1 = (2 * key[0] + 0, key[1])
            key2 = (2 * key[0] + 1, key[1])
            val1, val2 = val, val
            if val == Stuff.WALL:
                val1, val2 = Stuff.WALL, Stuff.WALL
            elif val == Stuff.BOX:
                val1, val2 = Stuff.BBOXL, Stuff.BBOXR

            new_objects[key1] = val1
            new_objects[key2] = val2

        new_pos = self.robot_position
        new_pos = (2*new_pos[0], new_pos[1])

        return Map(new_objects, new_pos)


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


om, movements = parse(test_data)
om = om.double()

om.print()

for i, m in enumerate(movements):
    print(f" {i=:4d} {m=} ".center(40, "="))
    om.print(m)
    om = om.move2(m)
