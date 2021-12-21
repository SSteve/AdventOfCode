from collections import namedtuple
from dataclasses import dataclass
from typing import Tuple

Point = namedtuple('Point', ['x', 'y'])


@dataclass
class Extents:
    minX: int
    maxX: int
    minY: int
    maxY: int


TEST = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


def LoadAlgorithm(line: str) -> set[int]:
    algorithm: set[int] = set()
    for i, c in enumerate(line):
        if c == '#':
            algorithm.add(i)
    return algorithm


def LoadImage(lines: list[str]) -> set[Point]:
    image: set[Point] = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                image.add(Point(x, y))

    return image


def imageValue(x: int, y: int, image: set[Point], extents: Extents, defaultValue: int) -> int:

    result = 0
    for testY in range(y - 1, y + 2):
        for testX in range(x - 1, x + 2):
            if testY < extents.minY or testY > extents.maxY or testX < extents.minX or testX > extents.maxX:
                thisPoint = defaultValue
            else:
                thisPoint = int(Point(testX, testY) in image)

            result = (result << 1) + thisPoint
    return result


def ImageExtents(image: set[Point]) -> Tuple[int, int, int, int]:
    minX = min(p.x for p in image)
    maxX = max(p.x for p in image)
    minY = min(p.y for p in image)
    maxY = max(p.y for p in image)
    return (minX, maxX, minY, maxY)


def Generation(algorithm: set[int], image: set[Point], generationCount: int) -> set[Point]:
    newImage: set[Point] = set()
    extents = Extents(*ImageExtents(image))
    if 0 in algorithm:
        if 511 in algorithm:
            raise ValueError(
                "Bit 511 can't be set in the algorithm if bit 0 is set.")
        # If value 0 maps to a set bit in the algorithm, all the values
        # outside the image extent are 1 for odd-numbered generations
        # and 0 for even-numbered generations
        defaultValue = generationCount & 1
    else:
        defaultValue = 0
    for x in range(extents.minX - 1, extents.maxX + 2):
        for y in range(extents.minY - 1, extents.maxY + 2):
            value = imageValue(x, y, image, extents, defaultValue)
            if value in algorithm:
                newImage.add(Point(x, y))
    return newImage


def Day20(lines: list[str]) -> Tuple[int, int]:
    algorithm = LoadAlgorithm(lines[0])
    image = LoadImage(lines[2:])
    for i in range(2):
        image = Generation(algorithm, image, i)
    part1 = len(image)
    for i in range(2, 50):
        image = Generation(algorithm, image, i)
    part2 = len(image)
    # PrintImage(image)
    return part1, part2


def PrintImage(image: set[Point]) -> None:
    minX, maxX, minY, maxY = ImageExtents(image)
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            print("#" if Point(x, y) in image else " ", end="")
        print()
    print()


if __name__ == "__main__":
    part1, part2 = Day20(TEST.splitlines())
    assert part1 == 35
    assert part2 == 3351

    with open("20.txt", "r") as infile:
        part1, part2 = Day20(infile.read().splitlines())
    # 5776 too high
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
