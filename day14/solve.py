from dataclasses import dataclass
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
        print(Robot.get_mask(robots))

    @staticmethod
    def get_mask(robots: list["Robot"]):
        import numpy as np
        mask = np.zeros((robots[0].domain_x, robots[0].domain_y), dtype=int)
        for robot in robots:
            mask[robot.x, robot.y] += 1

        return mask

    def move(self) -> "Robot":
        new_x = (self.x + self.vx) % self.domain_x
        new_y = (self.y + self.vy) % self.domain_y

        return Robot(new_x, new_y, self.vx, self.vy, self.domain_x, self.domain_y)


# robots = Robot.from_lines(test_data.splitlines(), 11, 7)
robots = Robot.from_lines(data.splitlines(), 101, 103)
for t in range(100):
    robots = [robot.move() for robot in robots]

mask = Robot.get_mask(robots)
# Split by quadrant
Nx, Ny = mask.shape
Nx //= 2
Ny //= 2
quads = mask[:Nx, :Ny], mask[-Nx:, :Ny], mask[:Nx, -Ny:], mask[-Nx:, -Ny:]
total = np.prod([q.sum() for q in quads])
print(f"Part 1: {total}")
