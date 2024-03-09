from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from generic_search import astar

TEST = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

TEST2 = """111111111111
999999999991
999999999991
999999999991
999999999991"""


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __repr__(self):
        return str(self.value)


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def next_from_direction(self, direction: Direction):
        match direction:
            case Direction.UP:
                return Point(self.x, self.y - 1)
            case Direction.RIGHT:
                return Point(self.x + 1, self.y)
            case Direction.DOWN:
                return Point(self.x, self.y + 1)
            case Direction.LEFT:
                return Point(self.x - 1, self.y)


@dataclass(frozen=True)
class Location:
    here: Point
    last_three: tuple[Direction]

    def with_new_point(self, point: Point, direction: Direction):
        return Location(
            point,
            (*self.last_three[1:], direction),
        )


@dataclass(frozen=True)
class UltraLocation:
    # Location for ultra crucible. Needs to keep track of ten previous directions.
    here: Point
    previous: tuple[Direction]

    def with_new_point(self, point: Point, direction: Direction):
        if len(self.previous) >= 10:
            return UltraLocation(point, (*self.previous[-9:], direction))
        return UltraLocation(point, (*self.previous, direction))

    def __eq__(self, other):
        return self.here == other.here


class Part1Map:
    grid: dict[Point, int]
    width: int
    height: int
    final_location: Point

    def __init__(self, input: list[str]):
        self.grid = {}
        for y, line in enumerate(input):
            for x, c in enumerate(line):
                self.grid[Point(x, y)] = int(c)
        self.width = len(input[0])
        self.height = len(input)
        self.final_location = Point(self.width - 1, self.height - 1)

    def successors(self, location: Location) -> Iterable[Location]:
        for direction in Direction:
            if location.last_three[-1] and direction.value == (
                (location.last_three[-1].value + 2) % 4
            ):
                # Can't double back on previous direction.
                continue

            # Test to make sure this direction isn't the same as the previous three.
            if all(d == direction for d in location.last_three):
                continue

            # If the next point is valid, return the new location.
            next = location.here.next_from_direction(direction)
            if next in self.grid:
                yield location.with_new_point(next, direction)

    def cost_to_location(
        self, this_location: Location, next_location: Location
    ) -> float:
        return self.grid[next_location.here]

    def finished(self, location: Location) -> bool:
        return location.here == self.final_location

    def heuristic_to_goal(self, location: Location) -> float:
        return abs(location.here.x - self.final_location.x) + abs(
            location.here.y - self.final_location.y
        )

    def string_from_path(self, path: list[Location]):
        string: str = ""
        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)
                if any(p.here == point for p in path):
                    string += "•"
                else:
                    string += str(self.grid[point])
            string += "\n"
        return string


class Part2Map:
    grid: dict[Point, int]
    width: int
    height: int
    final_location: Point

    def __init__(self, input: list[str]):
        self.grid = {}
        for y, line in enumerate(input):
            for x, c in enumerate(line):
                self.grid[Point(x, y)] = int(c)
        self.width = len(input[0])
        self.height = len(input)
        self.final_location = Point(self.width - 1, self.height - 1)

    # UltraLocation(here=Point(x=5, y=1), previous=(1, 1, 1, 1, 2, 1))
    def successors(self, location: UltraLocation) -> Iterable[UltraLocation]:
        for direction in Direction:
            if len(location.previous) == 0:
                # If this is the first move, any direction is valid.
                next = location.here.next_from_direction(direction)
                if next in self.grid:
                    yield location.with_new_point(next, direction)
                continue

            # At this point we know there is at least one previous direction.
            if direction.value == (location.previous[-1].value + 2) % 4:
                # Can't double back on previous direction.
                continue

            if len(location.previous) < 4 and direction != location.previous[-1]:
                # Have to go four initial blocks before changing direction.
                continue

            if (
                len(location.previous) >= 4
                and any(d != location.previous[-4] for d in location.previous[-3:])
                and direction != location.previous[-1]
            ):
                # Have to go at least four blocks in one direction before turning.
                continue

            if len(location.previous) >= 10 and all(
                d == direction for d in location.previous[-10:]
            ):
                # Have to change direction after going ten blocks without turning.
                continue

            # If this direction is valid, return the new location if it's in the grid.
            next = location.here.next_from_direction(direction)
            if next in self.grid:
                yield location.with_new_point(next, direction)

    def cost_to_location(
        self, this_location: UltraLocation, next_location: UltraLocation
    ) -> float:
        return self.grid[next_location.here]

    def finished(self, location: UltraLocation) -> bool:
        return (
            location.here == self.final_location
            and len(location.previous) >= 4
            and all(d == location.previous[-4] for d in location.previous[-3:])
        )

    def heuristic_to_goal(self, location: UltraLocation) -> float:
        return abs(location.here.x - self.final_location.x) + abs(
            location.here.y - self.final_location.y
        )

    def string_from_path(self, path: list[UltraLocation]):
        string: str = ""
        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)
                if any(p.here == point for p in path):
                    string += "•"
                else:
                    string += str(self.grid[point])
            string += "\n"
        return string


def find_shortest_path(lines: list[str]) -> int:
    city_map = Part1Map(lines)
    initial_location = Location(
        Point(0, 0),
        (None, None, None),
    )
    solution = astar(
        initial_location,
        city_map.finished,
        city_map.successors,
        city_map.heuristic_to_goal,
        city_map.cost_to_location,
    )
    if solution is None:
        return None
    # path = nodeToPath(solution)
    # print(city_map.string_from_path(path))
    return int(solution.cost)


def find_ultra_crucible_path(lines: list[str]) -> int:
    city_map = Part2Map(lines)
    initial_location = UltraLocation(
        Point(0, 0),
        (),
    )
    solution = astar(
        initial_location,
        city_map.finished,
        city_map.successors,
        city_map.heuristic_to_goal,
        city_map.cost_to_location,
    )
    if solution is None:
        return None
    # path = nodeToPath(solution)
    # print(city_map.string_from_path(path))
    return int(solution.cost)


if __name__ == "__main__":
    part1test = find_shortest_path(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 102

    part2test = find_ultra_crucible_path(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 94

    part2test = find_ultra_crucible_path(TEST2.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 71

    with open("day17.txt") as infile:
        lines = infile.read().splitlines()

    part1 = find_shortest_path(lines)
    print(f"Part 1: {part1}")
    # 1248 is high.
    # 1033 is low.
    assert part1 == 1044

    part2 = find_ultra_crucible_path(lines)
    print(f"Part 2: {part2}")
