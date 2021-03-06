import math
from typing import List, Tuple

TEST = """939
7,13,x,x,59,x,31,19"""


def Part1(earliest: int, buses: List[str]) -> int:
    nextID = 0
    nextWait = math.inf
    for bus in buses:
        if bus == 'x':
            continue
        busPeriod = int(bus)
        previous = busPeriod * (earliest // busPeriod)
        next = previous + busPeriod
        if next - earliest < nextWait:
            nextWait = next - earliest
            nextID = busPeriod
    return nextID * nextWait


def tZeroIsValid(tZero: int, id: int, i: int) -> bool:
    mod = (tZero + i) % id
    return mod == 0


def Part2(buses: List[str]) -> int:
    # I cheated on this one and found a hint on the reddit forum.
    tZero = 0
    values = []
    for i, idString in enumerate(buses):
        if idString == 'x':
            continue
        id = int(idString)
        values.append((i, id))

    # In the beginning we start at our first bus id and
    # increase our baseTime by the first bus id.
    baseTime = values[0][1]
    period = values[0][1]
    for i, id in values[1:]:
        multiple = 0
        isValid = False
        while not isValid:
            multiple += 1
            tZero = baseTime + multiple * period
            isValid = tZeroIsValid(tZero, id, i)
        # Now that we've found a time that works for this bus, we
        # multiply our period by this bus id because any further
        # base time has to be a multiple of this id from the
        # time we just found.
        baseTime = tZero
        period *= id

    return tZero


def GetInput(lines: List[str]) -> Tuple[int, List[str]]:
    return (int(lines[0]), lines[1].split(','))


if __name__ == "__main__":
    testEarliest, testBuses = GetInput(TEST.splitlines())
    testPart1 = Part1(testEarliest, testBuses)
    assert testPart1 == 295, f"Part 1 is {testPart1}. It should be 295"
    testPart2 = Part2(testBuses)
    assert testPart2 == 1068781

    assert Part2("17,x,13,19".split(",")) == 3417
    assert Part2("67,7,59,61".split(",")) == 754018
    assert Part2("67,x,7,59,61".split(",")) == 779210
    assert Part2("67,7,x,59,61".split(",")) == 1261476
    assert Part2("1789,37,47,1889".split(",")) == 1202161486

    with open("13.txt", "r") as infile:
        earliest, buses = GetInput(infile.read().splitlines())
    part1 = Part1(earliest, buses)
    print(f"Part 1: {part1}")
    print(f"Part 2: {Part2(buses)}")
