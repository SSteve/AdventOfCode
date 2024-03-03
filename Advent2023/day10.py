from collections import deque
from dataclasses import dataclass
from typing import Iterator, Self

TEST_A = """.....
.S-7.
.|.|.
.L-J.
....."""

TEST_B = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Tile:
    a: Point
    b: Point
    count: int = -1

    def connects_to(self, point: Point):
        return self.a == point or self.b == point

    def next_points(self) -> Iterator[Point]:
        yield self.a
        yield self.b

    @staticmethod
    def from_character(c: str, point: Point) -> Self:
        match c:
            case "|":
                return Tile(Point(point.x, point.y - 1), Point(point.x, point.y + 1))
            case "-":
                return Tile(Point(point.x - 1, point.y), Point(point.x + 1, point.y))
            case "L":
                return Tile(Point(point.x, point.y - 1), Point(point.x + 1, point.y))
            case "J":
                return Tile(Point(point.x, point.y - 1), Point(point.x - 1, point.y))
            case "7":
                return Tile(Point(point.x, point.y + 1), Point(point.x - 1, point.y))
            case "F":
                return Tile(Point(point.x, point.y + 1), Point(point.x + 1, point.y))
            case _:
                raise ValueError(f"Unexpected character '{c}'.")


def find_furthest(lines: list[str]) -> int:
    start_point: Point
    grid: dict[Point, Tile] = {}

    for y, line in enumerate(lines):
        for x, this_tile in enumerate(line):
            if this_tile == ".":
                continue
            if this_tile == "S":
                start_point = Point(x, y)
                continue
            point = Point(x, y)
            grid[point] = Tile.from_character(this_tile, point)

    points_to_travel: deque[Point] = deque()

    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            point = Point(start_point.x + x, start_point.y + y)
            if point in grid and grid[point].connects_to(start_point):
                points_to_travel.append(point)
                grid[point].count = 1
    grid[start_point] = Tile(points_to_travel[0], points_to_travel[1], 0)

    while points_to_travel:
        point = points_to_travel.popleft()
        this_tile = grid[point]
        for next_point in this_tile.next_points():
            next_tile = grid[next_point]
            if next_tile.count == -1:
                next_tile.count = this_tile.count + 1
                points_to_travel.append(next_point)

    return max(t.count for t in grid.values())


if __name__ == "__main__":
    part1test = find_furthest(TEST_A.splitlines())
    print(f"Part 1 test a: {part1test}")
    assert part1test == 4

    part1test = find_furthest(TEST_B.splitlines())
    print(f"Part 1 test b: {part1test}")
    assert part1test == 8

    """ 
    part2test = sum_of_left_extrapolations(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 2
    """

    with open("day10.txt") as infile:
        lines = infile.read().splitlines()

    part1 = find_furthest(lines)
    print(f"Part 1: {part1}")
    # assert part1 == 1789635132

    """ 
    part2 = sum_of_left_extrapolations(lines)
    print(f"Part 2: {part2}")
    """
