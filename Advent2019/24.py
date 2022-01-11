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
        nextGeneration: list[list[str]] = []
        for _ in range(self.height):
            nextGeneration.append([' '] * 5)
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


class InfiniteEris:
    def __init__(self, lines: list[str]) -> None:
        self.levels: dict[int, list[str]] = {0: lines}

    def Neighbors(self, level: int, x: int, y: int) -> Iterable[Location]:
        """
        Return the locations of the neighbors around this cell.
        The smaller grid inside the center is a higher level number. The larger grid outside
        a grid is a lower level number.
        """
        # Above
        if y == 0:
            # The upper neighbor is the center tile on the second row of the level outside this one.
            yield Location(level - 1, 2, 1)
        elif y == 1 or y == 2 or (y == 3 and x != 2) or y == 4:
            # The upper neighbor is on the same level.
            yield Location(level, x, y - 1)
        elif y == 3 and x == 2:
            # The upper neighbors are the bottom row of the level inside this one.
            for neighborX in range(5):
                yield Location(level + 1, neighborX, 4)
        else:
            raise ValueError("Unknown case for upper neighbor.")

        # Below
        if y == 0 or (y == 1 and x != 2) or y == 2 or y == 3:
            # The lower neighbor is on the same level.
            yield Location(level, x, y + 1)
        elif y == 1 and x == 2:
            # The lower neighbors are the top row of the level inside this one.
            for neighborX in range(5):
                yield Location(level + 1, neighborX, 0)
        elif y == 4:
            # The lower neighbor is the center tile on the fourth row of the level outside this one.
            yield Location(level - 1, 2, 3)
        else:
            raise ValueError("Unknown case for lower neighbor.")

        # Left
        if x == 0:
            # The left neighbor is the center tile in the second column of the level outside this one.
            yield Location(level - 1, 1, 2)
        elif x == 1 or x == 2 or (x == 3 and y != 2) or x == 4:
            # The left neighbor is on the same level.
            yield Location(level, x - 1, y)
        elif x == 3 and y == 2:
            # The left neighbors are the right column of the level inside this one.
            for neighborY in range(5):
                yield Location(level + 1, 4, neighborY)
        else:
            raise ValueError("Unknown case for left neighbor.")

        # Right
        if x == 0 or (x == 1 and y != 2) or x == 2 or x == 3:
            # The right neighbor is on the same level.
            yield Location(level, x + 1, y)
        elif x == 1 and y == 2:
            # The right neighbors are the left column of the level inside this one.
            for neighborY in range(5):
                yield Location(level + 1, 0, neighborY)
        elif x == 4:
            # The right neighbor is the center tile in the fourth column of the level outside this one.
            yield Location(level - 1, 3, 2)

    def NeighborCount(self, level: int, x: int, y: int) -> int:
        count = 0
        for neighbor in self.Neighbors(level, x, y):
            if neighbor.level in self.levels and self.levels[neighbor.level][neighbor.y][neighbor.x] == '#':
                count += 1
        return count

    def Generation(self) -> None:
        newLevels: dict[int, list[str]] = {}
        # We need to check one level above and below the highest and lowest levels.
        minLevel = min(self.levels.keys()) - 1
        maxLevel = max(self.levels.keys()) + 1
        for level in range(minLevel, maxLevel + 1):
            nextGeneration: list[list[str]] = []
            for _ in range(5):
                nextGeneration.append([' '] * 5)
            for y in range(5):
                for x in range(5):
                    if x == 2 and y == 2:
                        continue
                    neighbors = self.NeighborCount(level, x, y)
                    if level in self.levels and self.levels[level][y][x] == '#':
                        nextGeneration[y][x] = '#' if neighbors == 1 else '.'
                    else:
                        nextGeneration[y][x] = '#' if 1 <= neighbors <= 2 else '.'
            newLevel = [''.join(line) for line in nextGeneration]
            levelCount = sum(sum(int(c == '#') for c in line)
                             for line in newLevel)
            # If this level is above or below the highest or lowest levels, we only
            # add it to the collection if it has a bug.
            if levelCount or level > minLevel or level < maxLevel:
                newLevels[level] = newLevel
        self.levels = newLevels

    def BugCount(self) -> int:
        count = 0
        for level in range(min(self.levels.keys()), max(self.levels.keys()) + 1):
            for y in range(5):
                for x in range(5):
                    if x == 2 and y == 2:
                        continue
                    count += int(self.levels[level][y][x] == '#')
        return count


if __name__ == '__main__':
    eris = Eris(TEST.splitlines())
    part1 = eris.FindDuplicateRating()
    assert part1 == 2129920

    with open('24.txt', 'r') as infile:
        eris = Eris(infile.read().splitlines())
    part1 = eris.FindDuplicateRating()
    assert part1 == 18842609
    print(f"Part 1: {part1}")

    eris = InfiniteEris(TEST.splitlines())
    for _ in range(10):
        eris.Generation()
    assert eris.BugCount() == 99

    with open('24.txt', 'r') as infile:
        eris = InfiniteEris(infile.read().splitlines())
    for _ in range(200):
        eris.Generation()
    part2 = eris.BugCount()
    print(f"Part 2: {part2}")
