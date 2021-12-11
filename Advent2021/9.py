from collections import namedtuple

TEST = """2199943210
3987894921
9856789892
8767896789
9899965678"""


Point = namedtuple('Point', ['x', 'y'])


class Caves:
    def __init__(self, lines: list[str]) -> None:
        self.heightMap: list[list[int]] = []
        for line in lines:
            self.heightMap.append([int(c) for c in line])
        self.rows = len(lines)
        self.columns = len(lines[0])
        self.basins: set[frozenset[Point]] = set()
        self.lowPoints: set[Point] = set()

    def ValueAtPoint(self, point: Point):
        return self.heightMap[point.y][point.x]

    def Neighbors(self, point: Point) -> set[Point]:
        neighbors: set[Point] = set()
        if point.x > 0:
            neighbors.add(Point(point.x - 1, point.y))
        if point.x < self.columns - 1:
            neighbors.add(Point(point.x + 1, point.y))
        if point.y > 0:
            neighbors.add(Point(point.x, point.y - 1))
        if point.y < self.rows - 1:
            neighbors.add(Point(point.x, point.y + 1))
        return neighbors

    def FindLowPoints(self) -> None:
        for c in range(self.columns):
            for r in range(self.rows):
                thisPoint: Point = Point(c, r)
                thisValue = self.ValueAtPoint(thisPoint)
                if all(self.ValueAtPoint(p) > thisValue for p in self.Neighbors(thisPoint)):
                    self.lowPoints.add(thisPoint)

    def RiskLevelSum(self) -> int:
        result = len(self.lowPoints)
        result += sum(self.ValueAtPoint(p) for p in self.lowPoints)
        return result

    def PointInAnyBasin(self, point: Point):
        return any(point in basin for basin in self.basins)

    def AddPointToBasin(self, point: Point, basin: set[Point]):
        basin.add(point)
        for p in self.Neighbors(point):
            if self.ValueAtPoint(p) != 9 and p not in basin and not self.PointInAnyBasin(p):
                self.AddPointToBasin(p, basin)

    def FindBasins(self) -> None:
        for p in self.lowPoints:
            if not self.PointInAnyBasin(p):
                basin: set[Point] = set()
                self.AddPointToBasin(p, basin)
                self.basins.add(frozenset(basin))

    def ThreeLargestBasinsSum(self) -> int:
        basinsInOrder = sorted(self.basins, key=len)
        result = 1
        for basin in basinsInOrder[-3:]:
            result *= len(basin)
        return result


if __name__ == "__main__":
    caves = Caves(TEST.splitlines())
    caves.FindLowPoints()
    part1 = caves.RiskLevelSum()
    assert part1 == 15
    caves.FindBasins()
    part2 = caves.ThreeLargestBasinsSum()
    assert part2 == 1134

    with open("9.txt", "r") as infile:
        caves = Caves(infile.read().splitlines())
    caves.FindLowPoints()
    part1 = caves.RiskLevelSum()
    assert part1 == 458
    print(f"Part 1: {part1}")
    caves.FindBasins()
    part2 = caves.ThreeLargestBasinsSum()
    print(f"Part 2: {part2}")
