from dataclasses import dataclass
from itertools import combinations

TEST = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def create_universe(lines: list[str], empty_increment=1) -> set[Point]:
    universe: set[Point] = set()

    # Find which columns cause expansion.
    empty_columns = set(range(len(lines[0])))
    for line in lines:
        for x, c in enumerate(line):
            if c == "#":
                empty_columns.discard(x)

    y_offset = 0

    for y, line in enumerate(lines):
        if "#" not in line:
            y_offset += empty_increment
            continue
        x_offset = 0
        for x, c in enumerate(line):
            if x in empty_columns:
                x_offset += empty_increment
            if c == "#":
                universe.add(Point(x + x_offset, y + y_offset))

    return universe


def manhattan_distance(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def shortest_path_length(lines: list[str], empty_increment=1) -> int:
    universe = create_universe(lines, empty_increment)
    total_distance = 0
    for start, end in combinations(universe, 2):
        total_distance += manhattan_distance(start, end)
    return total_distance


if __name__ == "__main__":
    part1test = shortest_path_length(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 374

    part2test = shortest_path_length(TEST.splitlines(), 9)
    print(f"Part 2 test: {part2test}")
    assert part2test == 1030

    part2test = shortest_path_length(TEST.splitlines(), 99)
    print(f"Part 2 test: {part2test}")
    assert part2test == 8410

    with open("day11.txt") as infile:
        lines = infile.read().splitlines()

    part1 = shortest_path_length(lines)
    print(f"Part 1: {part1}")
    assert part1 == 9403026

    part2 = shortest_path_length(lines, 1_000_000 - 1)
    print(f"Part 2: {part2}")
