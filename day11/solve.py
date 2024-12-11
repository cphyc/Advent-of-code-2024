from pathlib import Path


test_data = "0 1 10 99 999"

data = (Path(__file__).parent / "input").read_text().strip()

def parse(data: str) -> list[int]:
    return [int(x) for x in data.split()]

def blink(gems: list[int]):
    new_gems = []
    for gem in gems:
        Ndigit = len(str(gem))
        if gem == 0:
            new_gems.append(1)
        elif Ndigit % 2 == 0:
            lhs, rhs = int(str(gem)[:Ndigit//2]), int(str(gem)[Ndigit//2:])
            new_gems.extend((lhs, rhs))
        else:
            new_gems.append(gem * 2024)
    return new_gems


gems = parse(data)
for i in range(25):
    gems = blink(gems)
print(f"Part 1: {len(gems)}")
