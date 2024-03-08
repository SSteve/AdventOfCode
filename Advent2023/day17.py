from dataclasses import dataclass
from typing import Iterable, Self

from generic_search import astar, nodeToPath

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


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Location:
    here: Point
    last_three: list[Point]

    def with_new_point(self, new_x: int, new_y: int):
        return Location(
            Point(new_x, new_y),
            [*self.last_three[1:], self.here],
        )

    def __eq__(self, other: Self):
        return self.here == other.here

    def __hash__(self):
        return hash(self.here)


class CityMap:
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

    def successors(self, location: Location) -> Iterable[Point]:
        if location.here.x > 0 and any(
            p.y != location.here.y for p in [*location.last_three[1:], location.here]
        ):
            yield location.with_new_point(location.here.x - 1, location.here.y)
        if location.here.x < self.width - 1 and any(
            p.y != location.here.y for p in [*location.last_three[1:], location.here]
        ):
            yield location.with_new_point(location.here.x + 1, location.here.y)
        if location.here.y > 0 and any(
            p.x != location.here.x for p in [*location.last_three[1:], location.here]
        ):
            yield location.with_new_point(location.here.x, location.here.y - 1)
        if location.here.y < self.height - 1 and any(
            p.x != location.here.x for p in [*location.last_three[1:], location.here]
        ):
            yield location.with_new_point(location.here.x, location.here.y + 1)

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


def find_shortest_path(lines: list[str]) -> int:
    city_map = CityMap(lines)
    initial_location = Location(
        Point(0, 0),
        [Point(-1, -1), Point(-1, -1), Point(-1, -1)],
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
    path = nodeToPath(solution)
    print(city_map.string_from_path(path))
    return int(solution.cost)


if __name__ == "__main__":
    part1test = find_shortest_path(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 102

    """ 
    part2test = find_most_tiles(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 51
 """
    with open("day17.txt") as infile:
        lines = infile.read().splitlines()

    part1 = find_shortest_path(lines)
    print(f"Part 1: {part1}")
    # 1248 is high.
    # assert part1 == 8098

    """ 
    part2 = find_most_tiles(lines)
    print(f"Part 2: {part2}")
 """
