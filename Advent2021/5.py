import re

from collections import defaultdict
from typing import Tuple

TEST = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


lineRegex = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")

Coordinate = Tuple[int, int]


def displayMap(map: dict[Coordinate, int]) -> None:
    maxX = max(k[0] for k in map.keys())
    for y in range(maxX + 1):
        for x in range(maxX + 1):
            if (x, y) in map.keys():
                print(map[x, y], end="")
            else:
                print('.', end="")
        print()


def BuildMap(lines: list[str]) -> Tuple[int, int]:
    ventMap: dict[Coordinate, int] = defaultdict(int)
    for line in lines:
        lineMatch = lineRegex.match(line)
        x1 = int(lineMatch[1])  # type: ignore
        y1 = int(lineMatch[2])  # type: ignore
        x2 = int(lineMatch[3])  # type: ignore
        y2 = int(lineMatch[4])  # type: ignore

        if x1 == x2:
            y1, y2 = min(y1, y2), max(y1, y2)
            y2 += 1
            for y in range(y1, y2):
                ventMap[(x1, y)] += 1
        elif y1 == y2:
            x1, x2 = min(x1, x2), max(x1, x2)
            x2 += 1
            for x in range(x1, x2):
                ventMap[(x, y1)] += 1
    part1 = len([count for count in ventMap.values() if count >= 2])

    # Now add the diagonal lines.
    for line in lines:
        lineMatch = lineRegex.match(line)
        x1 = int(lineMatch[1])  # type: ignore
        y1 = int(lineMatch[2])  # type: ignore
        x2 = int(lineMatch[3])  # type: ignore
        y2 = int(lineMatch[4])  # type: ignore

        if x1 != x2 and y1 != y2:
            deltaX = 1 if x2 > x1 else -1
            deltaY = 1 if y2 > y1 else -1
            x = x1
            y = y1
            while (deltaX == 1 and x <= x2) or (deltaX == -1 and x >= x2):
                ventMap[(x, y)] += 1
                x += deltaX
                y += deltaY
    part2 = len([count for count in ventMap.values() if count >= 2])

    # displayMap(ventMap)
    return part1, part2


if __name__ == "__main__":
    part1, part2 = BuildMap(TEST.splitlines())
    assert part1 == 5
    assert part2 == 12

    with open("5.txt", "r") as infile:
        part1, part2 = BuildMap(infile.read().splitlines())
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
