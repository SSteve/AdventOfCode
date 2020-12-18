from typing import Dict, Tuple


def Day15(seed: str, limit: int = 2020) -> Tuple[int, int]:
    numbers: Dict[int, int] = {}
    turn = 0
    lastNumber = 0
    part1 = -1
    part2 = -1
    lastWasFound = False
    for numStr in seed.split(","):
        turn += 1
        lastNumber = int(numStr)
        lastWasFound = lastNumber in numbers
        if lastWasFound:
            nextNumber = turn - numbers[lastNumber] - 1
        else:
            nextNumber = 0
        numbers[lastNumber] = turn
        lastNumber = nextNumber

    while turn <= limit:
        turn += 1
        lastWasFound = lastNumber in numbers
        if lastWasFound:
            nextNumber = turn - numbers[lastNumber]
        else:
            nextNumber = 0
        numbers[lastNumber] = turn

        if turn == 2020:
            part1 = lastNumber
        if turn == 30_000_000:
            part2 = lastNumber

        lastNumber = nextNumber

    return part1, part2


assert Day15("0,3,6")[0] == 436
assert Day15("1,3,2")[0] == 1
assert Day15("2,1,3")[0] == 10
assert Day15("1,2,3")[0] == 27
assert Day15("2,3,1")[0] == 78
assert Day15("3,2,1")[0] == 438
assert Day15("3,1,2")[0] == 1836

part1, part2 = Day15("1,17,0,10,18,11,6", 30_000_000)
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
