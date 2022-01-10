from collections import namedtuple
from typing import Iterable

TEST = """....#
#..#.
#..##
..#..
#...."""


class Eris:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)

    def BiodiversityRating(self) -> int:
        rating = 0
        for i in range(self.width * self.height):
            c = self.lines[i // self.width][i % self.width]
            if c == '#':
                rating += pow(2, i)
        return rating

    def NeighborCount(self, x: int, y: int) -> int:
        count = 0
        for neighborX, neighborY in ((x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)):
            if neighborX >= 0 and neighborX < self.width and \
                    neighborY >= 0 and neighborY < self.height and \
                    self.lines[neighborY][neighborX] == '#':
                count += 1
        return count

    def Generation(self) -> None:
        line: list[str] = [' '] * 5
        nextGeneration: list[list[str]] = []
        for _ in range(self.height):
            nextGeneration.append(line[:])
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.NeighborCount(x, y)
                if self.lines[y][x] == '#':
                    nextGeneration[y][x] = '#' if neighbors == 1 else '.'
                else:
                    nextGeneration[y][x] = '#' if 1 <= neighbors <= 2 else '.'
        self.lines = [''.join(line) for line in nextGeneration]

    def __repr__(self) -> str:
        return '\n'.join(self.lines)

    def FindDuplicateRating(self) -> int:
        ratings: set[int] = set([self.BiodiversityRating()])
        while True:
            self.Generation()
            rating = self.BiodiversityRating()
            if rating in ratings:
                return rating
            ratings.add(rating)


Location = namedtuple('Location', ('level', 'x', 'y'))
MAX_COORDINATE = 4


class InfiniteEris:
    def __init__(self, lines: list[str]) -> None:
        self.levels: dict[int, list[str]] = {0: lines}

    def Neighbors(self, level: int, x: int, y: int) -> Iterable[Location]:
        # Above
        if y == 0:
            # The upper neighbor is the center tile on the second row of the level outside this one.
            yield Location(level - 1, 2, 1)
        elif y == 1 or y == 2 or (y == 3 and x != 2) or (y == 4):
            # The upper neighbor is on the same level.
            yield Location(level, x, y - 1)
        elif y == 3 and x == 2:
            # The upper neighbors are the bottom row of the level inside this one.
            for neighborX in range(5):
                yield Location(level + 1, x, 4)


eris = Eris(TEST.splitlines())
part1 = eris.FindDuplicateRating()
assert part1 == 2129920

with open('24.txt', 'r') as infile:
    eris = Eris(infile.read().splitlines())
part1 = eris.FindDuplicateRating()
print(f"Part 1: {part1}")
# print(f"Part 2: {part2}")
