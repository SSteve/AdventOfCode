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
    map: list[str]
    finish: Point
    use_slopes: bool
    states: set[str]

    def __init__(self, input: list[str], use_slopes):
        self.map = input
        self.finish = Point(len(input[0]) - 2, len(input) - 1)
        self.use_slopes = use_slopes
        self.states = set()

    @cache
    def location_is_on_trail(self, location: Point):
        return (
            0 <= location.x < len(self.map[0])
            and 0 <= location.y < len(self.map)
            and self.map[location.y][location.x] != "#"
        )

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
            next = list(
                filter(lambda p: p not in previous, self.next_from_location(location))
            )

            if len(next) == 0:
                # Dead end.
                return 0

            if len(next) > 1:
                # If this is a fork, return the longest path from here to the end.
                state = f"{len(previous)} steps. Location: {location}. Fork: {next}"
                # print(state)
                if state in self.states:
                    # raise ValueError("We've seen this state before.")
                    # print("We've seen this state before.")
                    return 0
                    pass
                self.states.add(state)
                return max(
                    self.find_longest_hike(p, set([*previous, location])) for p in next
                )

            if len(next) == 1:
                # There's only one possible next step, so move to that step and continue looking
                # at next steps.
                previous.add(location)
                location = next[0]
                if location == self.finish:
                    return len(previous)


def find_longest_hike(lines: list[str], part2: bool) -> int:
    trail_map = TrailMap(lines, part2)
    return trail_map.find_longest_hike(Point(1, 0), set())


if __name__ == "__main__":
    part1test = find_longest_hike(TEST.splitlines(), True)
    print(f"Part 1 test: {part1test}")
    assert part1test == 94

    part2test = find_longest_hike(TEST.splitlines(), False)
    print(f"Part 2 test: {part2test}")
    assert part2test == 154

    with open("day23.txt") as infile:
        lines = infile.read().splitlines()

    part1 = find_longest_hike(lines, True)
    print(f"Part 1: {part1}")
    assert part1 == 2402

    part2 = find_longest_hike(lines, False)
    print(f"Part 2: {part2}")
    assert part2 > 6098
