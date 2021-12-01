import math

from collections import deque

TEST = """199
200
208
210
200
207
240
269
260
263"""


def CountIncreases(lines: list[str]) -> int:
    previousValue = math.inf
    increases = 0
    for line in lines:
        if len(line) == 0:
            continue
        currentValue = int(line)
        if currentValue > previousValue:
            increases += 1
        previousValue = currentValue
    return increases


def CountWindowIncreases(lines: list[str]) -> int:
    increases = 0
    measurements = deque()

    # Read the first three values.
    for x in range(3):
        measurements.append(int(lines[x]))

    previousValue = sum(measurements)

    for line in lines[3:]:
        measurements.popleft()
        measurements.append(int(line))
        currentValue = sum(measurements)
        if currentValue > previousValue:
            increases += 1
        previousValue = currentValue
    return increases


if __name__ == "__main__":
    test1 = CountIncreases(TEST.splitlines())
    assert test1 == 7
    test2 = CountWindowIncreases(TEST.splitlines())
    assert test2 == 5

    with open("1.txt", "r") as infile:
        part1 = CountIncreases(infile.read().splitlines())
    print(f"Part 1: {part1}")
    with open("1.txt", "r") as infile:
        part2 = CountWindowIncreases(infile.read().splitlines())
    print(f"Part 2: {part2}")
