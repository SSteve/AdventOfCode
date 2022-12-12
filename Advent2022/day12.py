from dataclasses import dataclass
from typing import TypeVar

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

    def successors(self, point: Point) -> list[Point]:
        surrounding = [Point(point.x-1, point.y), Point(point.x+1, point.y),
                       Point(point.x, point.y-1), Point(point.x, point.y+1)]
        reachable_height = self.locations[point] + 1
        successors = list(filter(lambda p: p in surrounding and
                                p not in self.bad_starts and
                                self.locations[p] <= reachable_height, self.locations))
        return successors

    def find_shortest_path_length(self) -> int:
        path = self.find_shortest_path_from_point(self.start)
        return len(path) - 1

    def find_shortest_path_from_point(self, point: Point) -> list[Point]:
        self.bad_starts: set[Point] = set()
        solution_node = bfs(point, self.is_at_end, self.successors)
        if solution_node is None:
            raise ValueError("No solution found.")
        return nodeToPath(solution_node)

    def find_shortest_path_from_a(self) -> int:
        paths: list[list[Point]] = []
        self.bad_starts: set[Point] = set()
        for start in filter(lambda p: self.locations[p] == 0 and
                            p not in self.bad_starts and
                            (p not in path for path in paths), self.locations):
            try:
                paths.append(self.find_shortest_path_from_point(start))
                print(f"length at {start}: {len(paths[-1]) - 1}")
            except:
                print(f"No solution found starting at {start}.")
                self.bad_starts.add(start)
                continue
        print(f"Finished collecting paths. Found {len(paths)}.")
        # Now we have all of the paths that start at an 'a' location.
        shortest_path_length = len(self.locations)
        for path in paths:
            last_a_location = list(filter(lambda p: self.locations[p] == 0, path))[-1]
            last_a_index = path.index(last_a_location)
            if len(path) - last_a_index < shortest_path_length:
                shortest_path_length = len(path) - last_a_index
        # The shortest path includes the start point, but we don't count the
        # start point in our solution.
        return shortest_path_length - 1


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

    # part1 = height_map.find_shortest_path_length()
    # print(f"Part 1: {part1}")
    # assert (part1 == 456)

    part2 = height_map.find_shortest_path_from_a()
    print(f"Part 2: {part2}")
    # assert (part2 == 29)
