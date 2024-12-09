from pathlib import Path


test_data = "2333133121414131402"
data = (Path(__file__).parent / "input").read_text().strip()

def parse(data: str) -> list[str]:
    disk: list[str] = []

    iblock = 0
    for i in range(len(data)):
        if i % 2 == 0:
            disk.extend([str(iblock)] * int(data[i]))
            iblock += 1
        else:
            disk.extend(["."] * int(data[i]))

    return disk

def part1(disk: list[str]):
    # Find first non-zero block
    ifree = disk.index(".")

    for ilast in range(len(disk)-1, -1, -1):
        if disk[ilast] != ".":
            break

    ifree = 0
    ilast = len(disk) -1
    # Move chunks until ifree >= ilast
    while True:
        # Find first free block
        while disk[ifree] != ".":
            ifree += 1

        # Find next non-zero block
        while disk[ilast] == ".":
            ilast -= 1

        if ifree >= ilast:
            break

        # Move chunk
        disk[ifree], disk[ilast] = disk[ilast], disk[ifree]

    # Compute checksum
    checksum = 0
    i = 0
    while disk[i] != ".":
        checksum += int(disk[i]) * i
        i += 1

    print(f"Part 1: {checksum}")

disk = parse(data)
part1(disk)
# print("".join(disk))
