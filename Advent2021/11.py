from collections import namedtuple

TEST = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

Point = namedtuple('Point', ['x', 'y'])


class Octopuses:
    def __init__(self, lines: list[str]) -> None:
        self.energies: list[list[int]] = []
        for line in lines:
            self.energies.append([int(c) for c in line])
        self.rows = len(lines)
        self.columns = len(lines[0])
        self.flashedPoints: set[Point] = set()

    def Neighbors(self, point: Point) -> set[Point]:
        neighbors: set[Point] = set()
        for newX in [point.x - 1, point.x, point.x + 1]:
            for newY in [point.y - 1, point.y, point.y + 1]:
                if newX == point.x and newY == point.y:
                    continue
                if newX >= 0 and newX < self.columns and newY >= 0 and newY < self.columns:
                    neighbors.add(Point(newX, newY))
        return neighbors

    def ValueAtPoint(self, point: Point):
        return self.energies[point.y][point.x]

    def IncrementPoint(self, point: Point) -> None:
        self.energies[point.y][point.x] += 1

    def ClearFlashedPoints(self) -> None:
        for c in range(self.columns):
            for r in range(self.rows):
                thisPoint: Point = Point(c, r)
                if self.ValueAtPoint(thisPoint) > 9:
                    self.energies[thisPoint.y][thisPoint.x] = 0

    def Flash(self, point: Point):
        self.flashedPoints.add(point)
        for p in self.Neighbors(point):
            self.IncrementPoint(p)
        for p in self.Neighbors(point):
            if self.ValueAtPoint(p) > 9 and p not in self.flashedPoints:
                self.Flash(p)

    def Step(self) -> int:
        self.flashedPoints = set()
        for line in self.energies:
            for i in range(len(line)):
                line[i] += 1
        for c in range(self.columns):
            for r in range(self.rows):
                thisPoint: Point = Point(c, r)
                if self.ValueAtPoint(thisPoint) > 9 and thisPoint not in self.flashedPoints:
                    self.Flash(thisPoint)
        self.ClearFlashedPoints()
        return len(self.flashedPoints)

    def IsSynchronized(self) -> bool:
        return sum(sum(line) for line in self.energies) == 0


if __name__ == "__main__":
    octopuses = Octopuses(TEST.splitlines())
    part1 = 0
    i = 0
    while not octopuses.IsSynchronized():
        stepValue = octopuses.Step()
        if i < 100:
            part1 += stepValue
        i += 1
    assert part1 == 1656
    assert i == 195

    with open("11.txt", "r") as infile:
        octopuses = Octopuses(infile.read().splitlines())
    part1 = 0
    i = 0
    while not octopuses.IsSynchronized():
        stepValue = octopuses.Step()
        if i < 100:
            part1 += stepValue
        i += 1
    print(f"Part 1: {part1}")
    print(f"Part 2: {i}")
