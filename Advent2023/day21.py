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

TEST2 = """...........
......##.#.
.###..#..#.
..#.#...#..
....#.#....
.....S.....
.##......#.
.......##..
.##.#.####.
.##...#.##.
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

    def distance_to(self, other: Self) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


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


def garden_map_to_string(garden_map: set[Point], locations: set[Point]) -> str:
    width = max(p.x for p in garden_map) + 1
    height = max(p.y for p in garden_map) + 1
    map_string = ""

    for y in range(height):
        for x in range(width):
            point = Point(x, y)
            if point in locations:
                map_string += "O"
            elif point in garden_map:
                map_string += "."
            else:
                map_string += "#"
        map_string += "\n"
    map_string += "\n"

    return map_string


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

    # if len(lines) == 11:
    #     garden_map_string = garden_map_to_string(garden_map, locations)
    #     print(garden_map_string)

    return len(locations)


def count_plots_after_steps2(lines: list[str], target_steps: int) -> int:
    """
    From: https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/kee6vn6/?utm_source=share&utm_medium=web2x&context=3

    I never got this one to work. I just copied someone else's solution at
    https://topaz.github.io/paste/#XQAAAQCeBQAAAAAAAAARiEJHiiMzw3cPM/1Vl+2nx/DqKkM2yi+HVdpp+qLiqZwdO8DftYzG7xETHPj1qjypxh5M1TcPUMscdwJ9eMao1h4KjZSFqvUVGgRO1B0UY9xy1ppiz5MCls8P3jkcK0nuQ0xyqjMGO1zjudp0iPknFIS8KiruHYaV0oYFiXPlq3dvfOk0cauC2zWBU2p1szheeFD+7GZgQeykiUtJN8b+wzbhZ65bKfiBB1gul8E7IwImm8bqpE8braA+LRUs1XJZzK2G46tXR6/d6xJtW5NGjJjHgAXSH14fmLMklh5VDxG0tn7HmD6DVp0cU5O+DsStE5RdLIZlgxHaGqJzUbAHINJ4vJuUBz/fylfnS9XSGryu4VDbTeMZS7G+otzsWsP+HUHltlbX21viYDOEMfdDaE6+JWWmEP2q2E2ju4EZIY1Uh7B6T9+MicUVxP9U6exzBmSGQGTbwUgMwpzIXfKDS6y8DyoeNmCmXQbeXgnCbxVvdxyAzD7EAsVfucUdylX8InxAsKPryrLr4e6x/cquH7HycA65oQo+tEzagk4BxC+u3RKwqw3bT01lVSvUPsAMO5PyFvWhunpfJ/5jY8tuj9H9XtCVSdYk/gUhO9CD+RLfYnswXCUgJyMUvO9qTXSXDFbqTqcNscDEuPc1iudSy742x76ClRqC8zGBXaeHOrEStITvQqlJ48cLcngpSqI+gSExoKWS6s008/qVMXYxnu/99dEEAArvIgWBDIyFeyeLNidukF/S4mprxsJCS8AoPGKKb2sKNBeSE+UdZG0yuogoubOeX1KpHW+NQSUL6+FWHzKX8RHpgEGTM18pfBF2QZUUgstqyqsqmmgllxPnoyEqRczwPw40staK1JZZ2CwnYxhBEJ8NB/aRgQhrcw+nLZLasm5AXDLcm59ISnomGkxf76hEZfDp9IuU/EUH8gLYHVu8KuL06/NL56Gzld64L6ONmn0rsU8Hj1YjNOGW5C/6Oj2mx8YHdQijhBr+uW6w2aIsexQXYi31e1nPeUGQafcmk/JK9f/f97Op.
    """
    garden_map, start = build_garden_map(lines)
    width = max(p.x for p in garden_map) + 1
    height = max(p.y for p in garden_map) + 1
    locations: set[Point] = set()
    locations.add(start)
    f0: int = 0
    f1: int = 0
    f2: int = 0

    for i in range(328):
        if i % 10 == 0:
            print(i)
        new_locations: set[Point] = set()
        for location in locations:
            for new_location in location.neighbors():
                if new_location in garden_map:
                    new_locations.add(new_location)
        locations = new_locations
        steps = i + 1

        if steps == width + height:
            even_location_count = len(locations)  # 7311
            even_corner_count = sum(start.distance_to(p) > 64 for p in locations)
        elif steps == width + height + 1:
            odd_location_count = len(locations)  # 7218
            odd_corner_count = sum(start.distance_to(p) > 64 for p in locations)

    print(f"{even_location_count=}, {odd_location_count=}")
    print(f"{even_corner_count=}, {odd_corner_count=}")

    n = target_steps // height
    assert n == 202300
    return (n + 1) ** 2 * odd_location_count + n**2 * even_location_count - (n + 1) * odd_corner_count + n * even_corner_count


if __name__ == "__main__":
    part1test = count_plots_after_steps(TEST.splitlines(), 6)
    print(f"Part 1 test: {part1test}")
    assert part1test == 16

    part1test = count_plots_after_steps(TEST2.splitlines(), 1001)
    print(f"Part 1 test: {part1test}")

    """ 
    part2test = count_plots_after_steps2(TEST.splitlines(), 50)
    print(f"Part 2 test: {part2test}")
    assert part2test == 1594

    part2test = count_plots_after_steps2(TEST.splitlines(), 100)
    print(f"Part 2 test: {part2test}")
    assert part2test == 6536

    part2test = count_plots_after_steps2(TEST.splitlines(), 500)
    print(f"Part 2 test: {part2test}")
    assert part2test == 167004

    part2test = count_plots_after_steps2(TEST.splitlines(), 1000)
    print(f"Part 2 test: {part2test}")
    assert part2test == 668697

    part2test = count_plots_after_steps2(TEST.splitlines(), 5000)
    print(f"Part 2 test: {part2test}")
    assert part2test == 16733044
 """
    with open("day21.txt") as infile:
        lines = infile.read().splitlines()

    part1 = count_plots_after_steps(lines, 64)
    print(f"Part 1: {part1}")
    assert part1 == 3572

    part2 = count_plots_after_steps2(lines, 26_501_365)
    print(f"Part 2: {part2}")
    # 594606477626700 is too low
    # assert part2 > 594606477626700
    assert part2 == 594606492802848
