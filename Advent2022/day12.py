from dataclasses import dataclass
from typing import Iterable, TypeVar

from generic_search import bfs, nodeToPath

TEST = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int


T = TypeVar('T')


def rindex(lst: list[T], value: T):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1


class HeightMap:
    def __init__(self, lines: list[str]) -> None:
        self.locations: dict[Point, int] = {}
        for y, line in enumerate(lines):
            for x, character in enumerate(line):
                match character:
                    case 'S':
                        self.start = Point(x, y)
                        character = 'a'
                    case 'E':
                        self.end = Point(x, y)
                        character = 'z'
                self.locations[Point(x, y)] = ord(character) - ord('a')

    def is_at_end(self, point: Point) -> bool:
        return point == self.end

    def successors(self, point: Point) -> Iterable[Point]:
        surrounding = [Point(point.x-1, point.y), Point(point.x+1, point.y),
                       Point(point.x, point.y-1), Point(point.x, point.y+1)]
        reachable_height = self.locations[point] + 1
        return filter(lambda p: p in surrounding and
                      self.locations[p] <= reachable_height, self.locations)

    def is_at_a(self, point: Point) -> bool:
        return self.locations[point] == 0

    def reverse_successors(self, point: Point) -> Iterable[Point]:
        surrounding = [Point(point.x-1, point.y), Point(point.x+1, point.y),
                       Point(point.x, point.y-1), Point(point.x, point.y+1)]
        reachable_height = self.locations[point] - 1
        return filter(lambda p: p in surrounding and
                      self.locations[p] >= reachable_height, self.locations)

    def find_shortest_path_length(self) -> int:
        path = self.find_shortest_path_from_point(self.start)
        return len(path) - 1

    def find_shortest_path_from_point(self, point: Point) -> list[Point]:
        solution_node = bfs(point, self.is_at_end, self.successors)
        if solution_node is None:
            raise ValueError("No solution found.")
        return nodeToPath(solution_node)

    def find_shortest_path_from_a(self) -> int:
        # Start at the end and find the shortest path to an 'a' location.
        solution_node = bfs(self.end, self.is_at_a, self.reverse_successors)
        if solution_node is None:
            raise ValueError("No solution found.")
        return len(nodeToPath(solution_node)) - 1


if __name__ == "__main__":
    height_map = HeightMap(TEST.splitlines())
    part1test = height_map.find_shortest_path_length()
    print(f"Part 1 test: {part1test}")
    assert (part1test == 31)
    part2test = height_map.find_shortest_path_from_a()
    print(f"Part 2 test: {part2test}")
    assert (part2test == 29)

    with open("day12.txt") as infile:
        height_map = HeightMap(infile.read().splitlines())

    part1 = height_map.find_shortest_path_length()
    print(f"Part 1: {part1}")
    assert (part1 == 456)

    part2 = height_map.find_shortest_path_from_a()
    print(f"Part 2: {part2}")
    assert (part2 == 454)
