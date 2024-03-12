from dataclasses import dataclass
from typing import Iterable, Self

TEST = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def neighbors(self) -> Iterable[Self]:
        yield Point(self.x, self.y - 1)
        yield Point(self.x + 1, self.y)
        yield Point(self.x, self.y + 1)
        yield Point(self.x - 1, self.y)


def build_garden_map(lines: list[str]) -> tuple[set[Point], int]:
    start: Point = Point(-1, -1)
    garden_map: set[Point] = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != "#":
                garden_map.add(Point(x, y))
            if c == "S":
                start = Point(x, y)
    if start == Point(-1, -1):
        raise ValueError("Didn't find start location.")
    return (garden_map, start)


def count_plots_after_steps(lines: list[str], target_steps: int) -> int:
    garden_map, start = build_garden_map(lines)
    locations: set[Point] = set()
    locations.add(start)

    for _ in range(target_steps):
        new_locations: set[Point] = set()
        for location in locations:
            for new_location in location.neighbors():
                if new_location in garden_map:
                    new_locations.add(new_location)
        locations = new_locations

    return len(locations)


if __name__ == "__main__":
    part1test = count_plots_after_steps(TEST.splitlines(), 6)
    print(f"Part 1 test: {part1test}")
    assert part1test == 16

    """ 
    part2test = calculate_focusing_power(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 145
 """
    with open("day21.txt") as infile:
        lines = infile.read().splitlines()

    part1 = count_plots_after_steps(lines, 64)
    print(f"Part 1: {part1}")
    # assert part1 == 510273

    """ 
    part2 = calculate_focusing_power(lines)
    print(f"Part 2: {part2}")
 """
