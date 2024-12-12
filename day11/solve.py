from functools import cache
from itertools import chain
from pathlib import Path
from tqdm import tqdm


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

@cache
def compute(i: int):
    gems = [i]
    for _ in range(25):
        gems = blink(gems)

    return gems


# Not efficient, but works in ~5min
twosteps = chain.from_iterable(compute(j) for i in tqdm(data) for j in compute(i))
sss = set(twosteps)

my_len = {}
for i in tqdm(sss):
    my_len[i] = len(compute(i))

twosteps = chain.from_iterable(compute(j) for i in tqdm(data) for j in compute(i))
print(f"Part 2: {sum(my_len[i] for i in twosteps)}")
