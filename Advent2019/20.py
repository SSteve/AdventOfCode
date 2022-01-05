from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

from generic_search import bfs, nodeToPath

TEST1 = """         A
         A
  #######.#########
  #######.........#
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C    ###.#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######...###.#
  #.#########.###.#
FG..#########.....#
  ###########.#####
             Z
             Z      """

TEST2 = """                   A
                   A
  #################.#############
  #.#...#...................#.#.#
  #.#.#.###.###.###.#########.#.#
  #.#.#.......#...#.....#.#.#...#
  #.#########.###.#####.#.#.###.#
  #.............#.#.....#.......#
  ###.###########.###.#####.#.#.#
  #.....#        A   C    #.#.#.#
  #######        S   P    #####.#
  #.#...#                 #......VT
  #.#.#.#                 #.#####
  #...#.#               YN....#.#
  #.###.#                 #####.#
DI....#.#                 #.....#
  #####.#                 #.###.#
ZZ......#               QG....#..AS
  ###.###                 #######
JO..#.#.#                 #.....#
  #.#.#.#                 ###.#.#
  #...#..DI             BU....#..LF
  #####.#                 #.#####
YN......#               VT..#....QG
  #.###.#                 #.###.#
  #.#...#                 #.....#
  ###.###    J L     J    #.#.###
  #.....#    O F     P    #.#...#
  #.###.#####.#.#####.#####.###.#
  #...#.#.#...#.....#.....#.#...#
  #.#####.###.###.#.#.#########.#
  #...#.#.....#...#.#.#.#.....#.#
  #.###.#####.###.###.#.#.#######
  #.#.........#...#.............#
  #########.###.###.#############
           B   J   C
           U   P   P              """


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def offset(self, deltaX, deltaY) -> Point:
        return Point(self.x + deltaX, self.y + deltaY)


class Maze:
    def __init__(self, lines: list[str]) -> None:
        # The passage coordinates.
        self.passages: set[Point] = set()
        # The pairs of coordinates that are portals. Each portal
        # is in the dictionary twice. One for each direction.
        self.portals: dict[Point, Point] = {}

        # First find all the passages. This makes it easier to build
        # portals.
        for y, line in enumerate(lines):
            if y < 2 or y >= len(lines):
                continue
            for x, c in enumerate(line):
                if x < 2 or x >= len(lines):
                    continue
                if c == '.':
                    # This is a passage.
                    self.passages.add(Point(x, y))

        # The first letter of a portal and its location.
        incompletePortalNames: dict[Point, str] = {}
        # One end of an unpaired portal.
        portalsInProgress: dict[str, Point] = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c.isupper():
                    testPointLeft = Point(x - 1, y)
                    testPointUp = Point(x, y - 1)
                    if testPointLeft in incompletePortalNames:
                        portalName = incompletePortalNames.pop(
                            testPointLeft) + c
                        if Point(x-2, y) in self.passages:
                            portalLocation = Point(x-2, y)
                        else:
                            portalLocation = Point(x+1, y)
                    elif testPointUp in incompletePortalNames:
                        portalName = incompletePortalNames.pop(testPointUp) + c
                        if Point(x, y-2) in self.passages:
                            portalLocation = Point(x, y-2)
                        else:
                            portalLocation = Point(x, y+1)
                    else:
                        incompletePortalNames[Point(x, y)] = c
                        continue
                    # We've found a portal. Identify its twin if it exists, otherwise
                    # store it in portalsInProgress.
                    if portalName in portalsInProgress:
                        otherEnd = portalsInProgress.pop(portalName)
                        self.portals[portalLocation] = otherEnd
                        self.portals[otherEnd] = portalLocation
                    else:
                        portalsInProgress[portalName] = portalLocation
        self.start = portalsInProgress['AA']
        self.end = portalsInProgress['ZZ']

    def Successors(self, p: Point) -> Iterable[Point]:
        for offsets in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            successor = p.offset(*offsets)
            if successor in self.passages:
                yield successor
        if p in self.portals:
            yield self.portals[p]

    def FindShortestPath(self) -> int:
        solution = bfs(self.start,
                       lambda p: p == self.end,
                       lambda p: self.Successors(p))
        if solution is None:
            raise ValueError("No solution found.")
        # Subtract 1 from the length because the starting
        # position doesn't count.
        return len(nodeToPath(solution)) - 1

    def FindShortestRecursivePath(self) -> int:
        # start: Tuple[Point, int] = (self.start, 0)
        raise NotImplementedError


if __name__ == '__main__':
    maze = Maze(TEST1.splitlines())
    part1 = maze.FindShortestPath()
    assert part1 == 23

    maze = Maze(TEST2.splitlines())
    part1 = maze.FindShortestPath()
    assert part1 == 58

    with open("20.txt") as infile:
        maze = Maze(infile.read().splitlines())
    part1 = maze.FindShortestPath()
    print(f"Part 1: {part1}")
