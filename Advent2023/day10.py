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

TEST_C = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

TEST_D = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

TEST_E = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Tile:
    a: Point
    b: Point
    shape: str
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
                return Tile(Point(point.x, point.y - 1), Point(point.x, point.y + 1), c)
            case "-":
                return Tile(Point(point.x - 1, point.y), Point(point.x + 1, point.y), c)
            case "L":
                return Tile(Point(point.x, point.y - 1), Point(point.x + 1, point.y), c)
            case "J":
                return Tile(Point(point.x, point.y - 1), Point(point.x - 1, point.y), c)
            case "7":
                return Tile(Point(point.x, point.y + 1), Point(point.x - 1, point.y), c)
            case "F":
                return Tile(Point(point.x, point.y + 1), Point(point.x + 1, point.y), c)
            case _:
                raise ValueError(f"Unexpected character '{c}'.")


def build_grid(lines: list[str]) -> tuple[dict[Point, Tile], Point]:
    start_point: Point
    grid: dict[Point, Tile] = {}
    points_to_travel: deque[Point] = deque()

    for y, line in enumerate(lines):
        for x, this_tile in enumerate(line):
            if this_tile == ".":
                continue
            if this_tile == "S":
                start_point = Point(x, y)
                continue
            point = Point(x, y)
            grid[point] = Tile.from_character(this_tile, point)

    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            point = Point(start_point.x + x, start_point.y + y)
            if point in grid and grid[point].connects_to(start_point):
                points_to_travel.append(point)
                grid[point].count = 1

    is_vertical = points_to_travel[0].x == 0 and points_to_travel[1].x == 0
    grid[start_point] = Tile(points_to_travel[0], points_to_travel[1], is_vertical, 0)

    while points_to_travel:
        point = points_to_travel.popleft()
        this_tile = grid[point]
        for next_point in this_tile.next_points():
            next_tile = grid[next_point]
            if next_tile.count == -1:
                next_tile.count = this_tile.count + 1
                points_to_travel.append(next_point)

    return grid, start_point


def find_furthest(lines: list[str]) -> int:
    grid, _ = build_grid(lines)

    return max(t.count for t in grid.values())


def get_previous_point(i, verticies: list[Point]) -> Point:
    if i > 0:
        return verticies[i - 1]
    # The start point is duplicated at the beginning and end, so return the point before the start point.
    return verticies[-2]


def get_next_point(i, verticies: list[Point]) -> Point:
    if i < len(verticies) - 1:
        return verticies[i + 1]
    # The start point is duplicated at the beginning and end, so return the point before the start point.
    return verticies[1]


def point_is_inside(point: Point, verticies: list[Point]):
    is_inside = False
    for i, (s, e) in enumerate(verticies[i : i + 2] for i in range(0, len(verticies) - 1)):
        if s.y > point.y and e.y > point.y or s.y < point.y and e.y < point.y:
            # This segment is above or below the point.
            continue
        if point.x < s.x:
            # This point is to the left of the segment.
            continue
        if not (s.y == point.y and e.y == point.y):
            # This is a vertical segment so it changes is_inside.
            is_inside = not is_inside
            continue
        # This is a horizontal segment. It only changes is_inside if it doesn't change direction.
        previous_point = get_previous_point(i, verticies)
        next_point = get_next_point(i + 1, verticies)
        # A horizontal segment changes direction if both next verticies are below or both are above.
        changes_direction = previous_point.y > s.y and next_point.y > s.y or previous_point.y < s.y and next_point.y < s.y
        if not changes_direction:
            is_inside = not is_inside

    return is_inside


def count_interior(lines: list[str]) -> int:
    grid, start_point = build_grid(lines)
    max_x = max(p.x for p in grid)
    max_y = max(p.y for p in grid)

    start_tile = grid[start_point]
    start_point_is_vertex = not (start_tile.a.y == start_tile.b.y or start_tile.a.x == start_tile.b.x)

    # Build an ordered list of vertices in the path.
    previous_point = start_point
    current_point = grid[start_point].a
    verticies: list[Point] = []
    # If the start point is part of a vertical or horizontal segment, we don't want to add it to the vertices.
    if start_point_is_vertex:
        verticies.append(start_point)
    path_points = set([start_point, current_point])
    current_tile = grid[current_point]
    while current_point != start_point:
        current_tile = grid[current_point]
        if current_tile.shape not in ["|", "-"]:
            verticies.append(current_point)
        path_points.add(current_point)
        new_point = current_tile.a if current_tile.a != previous_point else current_tile.b
        previous_point, current_point = current_point, new_point
    verticies.append(verticies[0])

    interior_count = 0

    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            current_point = Point(x, y)
            if current_point in path_points:
                continue
            if point_is_inside(current_point, verticies):
                interior_count += 1

    return interior_count


if __name__ == "__main__":
    part1test = find_furthest(TEST_A.splitlines())
    print(f"Part 1 test a: {part1test}")
    assert part1test == 4

    part1test = find_furthest(TEST_B.splitlines())
    print(f"Part 1 test b: {part1test}")
    assert part1test == 8

    part2test = count_interior(TEST_C.splitlines())
    print(f"Part 2 test c: {part2test}")
    assert part2test == 4

    part2test = count_interior(TEST_D.splitlines())
    print(f"Part 2 test d: {part2test}")
    assert part2test == 8

    part2test = count_interior(TEST_E.splitlines())
    print(f"Part 2 test e: {part2test}")
    assert part2test == 10

    with open("day10.txt") as infile:
        lines = infile.read().splitlines()

    part1 = find_furthest(lines)
    print(f"Part 1: {part1}")
    assert part1 == 7093

    part2 = count_interior(lines)
    # 356 is too low.
    print(f"Part 2: {part2}")
