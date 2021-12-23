from collections import namedtuple
from generic_search import astar, Node
from typing import Callable, Iterable, Optional

TEST = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

Point = namedtuple('Point', ['x', 'y'])


class ChitonMap:
    def __init__(self, lines: list[str]) -> None:
        self.locations: dict[Point, int] = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                self.locations[Point(x, y)] = int(char)
        # The cave is square so we only need the length of one dimension.
        self.caveSize = len(lines)

    def IsBottomRight(self, point: Point) -> bool:
        return point.x == self.caveSize - 1 and point.y == self.caveSize - 1

    def IsExtendedBottomRight(self, point: Point) -> bool:
        return point.x == self.caveSize * 5 - 1 and point.y == self.caveSize * 5 - 1

    def Successors(self, point: Point) -> Iterable[Point]:
        if point.x > 0:
            yield Point(point.x - 1, point.y)
        if point.y > 0:
            yield Point(point.x, point.y - 1)
        if point.x < self.caveSize - 1:
            yield Point(point.x + 1, point.y)
        if point.y < self.caveSize - 1:
            yield Point(point.x, point.y + 1)

    def ExtendedSuccessors(self, point: Point) -> Iterable[Point]:
        if point.x > 0:
            yield Point(point.x - 1, point.y)
        if point.y > 0:
            yield Point(point.x, point.y - 1)
        if point.x < self.caveSize * 5 - 1:
            yield Point(point.x + 1, point.y)
        if point.y < self.caveSize * 5 - 1:
            yield Point(point.x, point.y + 1)

    def CostToLocation(self, thisPoint: Point, nextPoint: Point) -> float:
        return self.locations[nextPoint]

    def ExtendedCostToLocation(self, thisPoint: Point, nextPoint: Point) -> float:
        xIncrement = nextPoint.x // self.caveSize
        yIncrement = nextPoint.y // self.caveSize
        normalizedPoint = Point(nextPoint.x %
                                self.caveSize, nextPoint.y % self.caveSize)
        cost = self.locations[normalizedPoint] + xIncrement + yIncrement
        cost = (cost - 1) % 9 + 1
        return cost

    @staticmethod
    def ManhattanDistanceToGoal(goal: Point) -> Callable[[Point], float]:
        def distance(point: Point) -> float:
            deltaX = abs(goal.x - point.x)
            deltaY = abs(goal.y - point.y)
            return deltaX + deltaY
        return distance

    def FindPath(self) -> Optional[Node[Point]]:
        solution = astar(Point(0, 0), self.IsBottomRight, self.Successors,
                         ChitonMap.ManhattanDistanceToGoal(Point(self.caveSize - 1, self.caveSize - 1)), self.CostToLocation)
        return solution

    def FindExtendedPath(self) -> Optional[Node[Point]]:
        solution = astar(Point(0, 0), self.IsExtendedBottomRight, self.ExtendedSuccessors,
                         ChitonMap.ManhattanDistanceToGoal(
                             Point(self.caveSize * 5 - 1, self.caveSize * 5 - 1)),
                         self.ExtendedCostToLocation)
        return solution


if __name__ == "__main__":
    chitonMap = ChitonMap(TEST.splitlines())

    """
    for y in range(chitonMap.caveSize * 5):
        for x in range(chitonMap.caveSize * 5):
            print(chitonMap.ExtendedCostToLocation(
                Point(x, y), Point(0, 0)), end="")
        print()
    """
    solution = chitonMap.FindPath()
    assert solution and solution.cost == 40
    solution = chitonMap.FindExtendedPath()
    assert solution and solution.cost == 315

    with open("15.txt", "r") as infile:
        chitonMap = ChitonMap(infile.read().splitlines())
    solution = chitonMap.FindPath()
    part1 = 0 if solution is None else int(solution.cost)
    print(f"Part 1: {part1}")

    solution = chitonMap.FindExtendedPath()
    part2 = 0 if solution is None else int(solution.cost)
    print(f"Part 2: {part2}")
