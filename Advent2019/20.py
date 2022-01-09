from __future__ import annotations
from collections import namedtuple
from dataclasses import dataclass
from typing import Callable, Iterable, Optional, TypeVar

from generic_search import bfs, nodeToPath, Queue, Node

Location = namedtuple("Location", ("point", "level"))
T = TypeVar('T')
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


TEST3 = """             Z L X W       C
             Z P Q B       K
  ###########.#.#.#.#######.###############
  #...#.......#.#.......#.#.......#.#.#...#
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
  #.#...#.#.#...#.#.#...#...#...#.#.......#
  #.###.#######.###.###.#.###.###.#.#######
  #...#.......#.#...#...#.............#...#
  #.#########.#######.#.#######.#######.###
  #...#.#    F       R I       Z    #.#.#.#
  #.###.#    D       E C       H    #.#.#.#
  #.#...#                           #...#.#
  #.###.#                           #.###.#
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#
CJ......#                           #.....#
  #######                           #######
  #.#....CK                         #......IC
  #.###.#                           #.###.#
  #.....#                           #...#.#
  ###.###                           #.#.#.#
XF....#.#                         RF..#.#.#
  #####.#                           #######
  #......CJ                       NM..#...#
  ###.#.#                           #.###.#
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#
  #.....#        F   Q       P      #.#.#.#
  ###.###########.###.#######.#########.###
  #.....#...#.....#.......#...#.....#.#...#
  #####.#.###.#######.#######.###.###.#.#.#
  #.......#.......#.#.#.#.#...#...#...#.#.#
  #####.###.#####.#.#.#.#.###.###.#.###.###
  #.......#.....#.#...#...............#...#
  #############.#.#.###.###################
               A O F   N
               A A D   M                     """


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
        # The map of portal locations to name. (Only used for debugging.)
        self.portalNames: dict[Point, str] = {}

        self.width = max(len(line) for line in lines)
        self.height = len(lines)

        # First find all the passages. This makes it easier to build
        # portals.
        for y, line in enumerate(lines):
            if y < 2:
                continue
            for x, c in enumerate(line):
                if x < 2:
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
                        if self.PortalIsExternal(otherEnd) == self.PortalIsExternal(portalLocation):
                            raise ValueError(
                                "Portals can't both be internal or external")
                        self.portals[portalLocation] = otherEnd
                        self.portals[otherEnd] = portalLocation
                        self.portalNames[portalLocation] = portalName
                        self.portalNames[otherEnd] = portalName
                    else:
                        portalsInProgress[portalName] = portalLocation
        self.start = portalsInProgress.pop('AA')
        self.end = portalsInProgress.pop('ZZ')
        if portalsInProgress:
            raise ValueError("There are unpaired portals.")

    def PortalIsExternal(self, p: Point) -> bool:
        return p.x <= 2 or p.y <= 2 or \
            p.x >= self.width - 3 or p.y >= self.height - 3

    def Successors(self, p: Point) -> Iterable[Point]:
        for offsets in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            successor = p.offset(*offsets)
            if successor in self.passages:
                yield successor
        if p in self.portals:
            yield self.portals[p]

    def RecursiveSuccessors(self, location: Location, parent: Node[Location]) -> Iterable[Location]:
        for offsets in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            successor = location.point.offset(*offsets)
            if successor in self.passages:
                yield Location(successor, location.level)
        if location.point in self.portals:
            print(f"{self.portalNames[location.point]} ({'out' if self.PortalIsExternal(location.point) else 'in'})" +
                  f" level {location.level}")
            if self.PortalIsExternal(location.point):
                if location.level > 0:
                    # Move up a level.
                    yield Location(self.portals[location.point], location.level - 1)
            else:
                ancestor: Optional[Node[Location]] = parent.parent
                # If we've already taken this inner portal on a higher level, don't take it again.
                while ancestor is not None and ancestor.state.point != location.point:
                    ancestor = ancestor.parent
                if ancestor is None:
                    # Move down a level.
                    yield Location(self.portals[location.point], location.level + 1)

    def FindShortestPath(self) -> int:
        solution = bfs(self.start,
                       lambda p: p == self.end,
                       lambda p: self.Successors(p))
        if solution is None:
            raise ValueError("No solution found.")
        # Subtract 1 from the length because the starting
        # position doesn't count.
        return len(nodeToPath(solution)) - 1

    def AtEnd(self, location: Location) -> bool:
        return location.point == self.end and location.level == 0

    def FindShortestRecursivePath(self) -> int:
        start: Location = Location(self.start, 0)
        solution = BreadthFirstSearch(
            start,
            self.AtEnd,
            self.RecursiveSuccessors)  # type: ignore
        if solution is None:
            return -1
        return len(nodeToPath(solution)) - 1


if __name__ == '__main__':
    maze = Maze(TEST1.splitlines())
    part1 = maze.FindShortestPath()
    assert part1 == 23

    part2 = maze.FindShortestRecursivePath()
    assert part2 == 26

    maze = Maze(TEST2.splitlines())
    part1 = maze.FindShortestPath()
    assert part1 == 58

    part2 = maze.FindShortestRecursivePath()
    assert part2 == -1

    maze = Maze(TEST3.splitlines())
    part2 = maze.FindShortestRecursivePath()
    assert part2 == 396

    with open("20.txt") as infile:
        maze = Maze(infile.read().splitlines())
    part1 = maze.FindShortestPath()
    print(f"Part 1: {part1}")

    # For part 2, I cheated and used the solution at https://github.com/mebeim/aoc/blob/master/2019/solutions/day20.py
    part2 = maze.FindShortestRecursivePath()
    print(f"Part 2: {part2}")
