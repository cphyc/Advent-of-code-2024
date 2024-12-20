from dataclasses import dataclass
from math import gcd
from pathlib import Path
import numpy as np

test_data = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
data = (Path(__file__).parent / "input").read_text()

@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int
    domain_x: int
    domain_y: int

    @staticmethod
    def from_str(line: str, domain_x: int, domain_y: int) -> "Robot":
        xx, vv = line.split()
        X = xx.split("=")[1].split(",")
        V = vv.split("=")[1].split(",")

        assert len(X) == 2
        assert len(V) == 2

        return Robot(*map(int, X), *map(int, V), domain_x, domain_y)

    @staticmethod
    def from_lines(lines: list[str], domain_x, domain_y) -> list["Robot"]:
        return [Robot.from_str(line, domain_x, domain_y) for line in lines]

    @staticmethod
    def plot(robots: list["Robot"]):
        mask = Robot.get_mask(robots).T
        for line in mask:
            column = np.where(line == 0, ".", line)
            print("".join(column))

    @staticmethod
    def get_mask(robots: list["Robot"]):
        import numpy as np
        mask = np.zeros((robots[0].domain_x, robots[0].domain_y), dtype=int)
        for robot in robots:
            mask[robot.x, robot.y] += 1

        return mask

    @staticmethod
    def get_quads(robots: list["Robot"]):
        mask = Robot.get_mask(robots)
        Nx, Ny = mask.shape
        Nx //= 2
        Ny //= 2
        quads = mask[:Nx, :Ny], mask[-Nx:, :Ny], mask[:Nx, -Ny:], mask[-Nx:, -Ny:]

        return quads

    def move(self) -> "Robot":
        new_x = (self.x + self.vx) % self.domain_x
        new_y = (self.y + self.vy) % self.domain_y

        return Robot(new_x, new_y, self.vx, self.vy, self.domain_x, self.domain_y)


# robots = Robot.from_lines(test_data.splitlines(), 11, 7)
robots = Robot.from_lines(data.splitlines(), 101, 103)
for t in range(100):
    robots = [robot.move() for robot in robots]

quads = Robot.get_quads(robots)
total = np.prod([q.sum() for q in quads])
print(f"Part 1: {total}")

Nstep_all = []
for robot in robots:
    robot0 = robot
    # Compute number of iterations to get back to own place
    Nstep = 1
    robot = robot.move()
    while robot0 != robot:
        robot = robot.move()
        Nstep += 1
    Nstep_all.append(Nstep)

Nstep_to_test = gcd(*Nstep_all)
print(Nstep_to_test)


robots = Robot.from_lines(data.splitlines(), 101, 103)
step = 0
for i in range(Nstep_to_test):
    robots = [robot.move() for robot in robots]
    step += 1
    mask = Robot.get_mask(robots)
    quads = Robot.get_quads(robots)

    # Look for a line of robots
    if ((mask > 0).sum(axis=1) > 20).any():
        print(f" {step=} ".center(80))
        Robot.plot(robots)
