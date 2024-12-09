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


def part2(disk: list[str]):
    ifree = 0
    iblock_max = max(iblock := int(d) for d in disk if d != ".")

    # Precompute map of empty spots
    empty: dict[int, int] = {}
    files: dict[int, tuple[int, int]] = {}
    i = 0
    iblock_max = 0
    while i < len(disk):
        if disk[i] == ".":
            for j in range(i+1, len(disk)):
                if disk[j] != ".":
                    break
            print(f"Empty spot [{i}, {j}[")
            empty[i] = j - i
        else:
            for j in range(i+1, len(disk)+1):
                if j == len(disk) or disk[j] != disk[i]:
                    break

            assert iblock_max == int(disk[i])
            print(f"Data {iblock_max}     [{i}, {j}[")
            files[iblock_max] = (i, j - i)
            iblock_max += 1
        i = max(j, i + 1)

    for iblock in range(iblock_max-1, -1, -1):
        # Look for the block
        istart, block_len = files[iblock]

        # Find first free block that's large enough
        for ifree, empty_block_len in empty.items():
            if empty_block_len >= block_len and ifree < istart:
                break
        else:
            # No free block
            continue

        # Move block
        disk[ifree:ifree+block_len] = [str(iblock)]*block_len
        disk[istart:istart+block_len] = ["."]*block_len

        # Update empty spot
        del empty[ifree]
        empty_block_len -= block_len
        if empty_block_len > 0:
            empty[ifree+block_len] = empty_block_len
            empty = dict(sorted(empty.items()))


    # Compute checksum
    checksum = 0
    block_len = 0
    for block_len in range(len(disk)):
        if disk[block_len] != ".":
            checksum += int(disk[block_len]) * block_len
        block_len += 1

    print(f"Part 2: {checksum}")

disk = parse(data)
part1(disk.copy())
part2(disk.copy())
