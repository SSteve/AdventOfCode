from dataclasses import dataclass
from functools import cache
from typing import Iterable, Self

TEST = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

"""
Part One approach: Whenever there's a fork in the path, look for the longest path from that fork.

Recursive algorithm:
Get a list of next steps. Next steps have to be an available path location and must not
have been previously visited.
- If there are no next steps it means we hit a dead end.
- If there are multiple next steps, start a new path at each and return the length of the longest.
- If there's one next step, mark it as visited. If it's the finish point, return the length of this path.
  If not, go back to getting the list of next steps.
"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def neighbors(self) -> Iterable[Self]:
        yield Point(self.x + 1, self.y)
        yield Point(self.x, self.y - 1)
        yield Point(self.x - 1, self.y)
        yield Point(self.x, self.y + 1)

    def right(self) -> Self:
        return Point(self.x + 1, self.y)

    def up(self) -> Self:
        return Point(self.x, self.y - 1)

    def left(self) -> Self:
        return Point(self.x - 1, self.y)

    def down(self) -> Self:
        return Point(self.x, self.y + 1)


class TrailMap:
    # TrailMap is used for Part 1.
    map: list[str]
    finish: Point
    use_slopes: bool

    def __init__(self, input: list[str], use_slopes):
        self.map = input
        self.finish = Point(len(input[0]) - 2, len(input) - 1)
        self.use_slopes = use_slopes

    @cache
    def location_is_on_trail(self, location: Point):
        return 0 <= location.x < len(self.map[0]) and 0 <= location.y < len(self.map) and self.map[location.y][location.x] != "#"

    @cache
    def next_from_location(self, location: Point) -> list[Point]:
        # Return the possible next locations.
        next_locations: list[Point] = []
        current_tile = self.map[location.y][location.x]
        if current_tile == "." or self.use_slopes is False:
            for p in location.neighbors():
                if self.location_is_on_trail(p):
                    next_locations.append(p)
        elif current_tile == ">":
            p = location.right()
            if self.location_is_on_trail(p):
                next_locations.append(p)
        elif current_tile == "v":
            p = location.down()
            if self.location_is_on_trail(p):
                next_locations.append(p)
        elif current_tile == "<":
            p = location.left()
            if self.location_is_on_trail(p):
                next_locations.append(p)
        elif current_tile == "^":
            p = location.up()
            if self.location_is_on_trail(p):
                next_locations.append(p)

        return next_locations

    def find_longest_hike(self, location: Point, previous: set[Point]) -> int:
        while True:
            # Find all the possible next steps. We can't return to a previous location.
            next = list(filter(lambda p: p not in previous, self.next_from_location(location)))

            if len(next) == 0:
                # Dead end.
                return 0

            if len(next) > 1:
                # If this is a fork, return the longest path from here to the end.
                return max(self.find_longest_hike(p, set([*previous, location])) for p in next)

            if len(next) == 1:
                # There's only one possible next step, so move to that step and continue looking
                # at next steps.
                previous.add(location)
                location = next[0]
                if location == self.finish:
                    return len(previous)

    def find_longest_hike2(self) -> int:
        return 0


class Tile:
    adjacent: list[Self]
    visited: bool
    is_start: bool
    is_end: bool

    def __init__(self, is_start: bool = False, is_end: bool = False):
        self.adjacent: list[Self] = []
        self.visited = False
        self.is_start = is_start
        self.is_end = is_end

    @property
    def is_node(self) -> bool:
        # Return true if this tile isn't in the middle of a path.
        return len(self.adjacent) != 2

    def connect(self, other: Self):
        # Connect this tile to another.
        self.adjacent.append((1, other))
        other.adjacent.append((1, self))

    def join(self):
        # Called when there are exactly two tiles connected to this one. Joins the two directly and retains
        # the distance between them.
        len_a, tile_a = self.adjacent[0]
        len_b, tile_b = self.adjacent[1]
        tile_a._replace((len_a, self), (len_a + len_b, tile_b))
        tile_b._replace((len_b, self), (len_a + len_b, tile_a))

    def _replace(self, other: Self, new: Self):
        index = self.adjacent.index(other)
        self.adjacent[index] = new

    def find_path(self) -> int:
        # Find the longest path to the end tile.
        if self.is_end:
            return 1
        self.visited = True
        path_len = 0
        for dist, next in self.adjacent:
            if not next.visited:
                d = next.find_path()
                if d > 0:
                    path_len = max(path_len, dist + d)
        self.visited = False
        return path_len


def find_longest_hike(lines: list[str]) -> int:
    trail_map = TrailMap(lines, True)
    return trail_map.find_longest_hike(Point(1, 0), set())


def find_longest_hike2(lines: list[str]) -> int:
    # Part 2 is adapted from https://github.com/fdouw/aoc-python/blob/master/2023/day23.py
    tiles2: dict[Point, Tile] = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                continue
            last_tile2 = Tile(is_start=(y == 0))
            this_location = Point(x, y)
            tiles2[this_location] = last_tile2
            above = this_location.up()
            if above in tiles2:
                last_tile2.connect(tiles2[above])
            before = this_location.left()
            if before in tiles2:
                last_tile2.connect(tiles2[before])
    last_tile2.is_end = True

    first_tile2 = (tile for tile in tiles2.values() if tile.is_start).__next__()

    for tile in tiles2.values():
        if not tile.is_node:
            tile.join()

    return first_tile2.find_path() - 1


if __name__ == "__main__":
    part1test = find_longest_hike(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 94

    part2test = find_longest_hike2(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 154

    with open("day23.txt") as infile:
        lines = infile.read().splitlines()

    part1 = find_longest_hike(lines)
    print(f"Part 1: {part1}")
    assert part1 == 2402

    part2 = find_longest_hike2(lines)
    print(f"Part 2: {part2}")
    assert part2 == 6450
