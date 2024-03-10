from dataclasses import dataclass
from enum import Enum

TEST = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def from_character(c: str):
        match c:
            case "U":
                return Direction.UP
            case "R":
                return Direction.RIGHT
            case "D":
                return Direction.DOWN
            case "L":
                return Direction.LEFT

    @staticmethod
    def from_numeral(c: str):
        match c:
            case "0":
                return Direction.RIGHT
            case "1":
                return Direction.DOWN
            case "2":
                return Direction.LEFT
            case "3":
                return Direction.UP

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


def print_grid(grid: set[Point], left: int, right: int, top: int, bottom: int) -> None:
    for y in range(top, bottom - top + 1):
        for x in range(left, right - left + 1):
            print("#" if Point(x, y) in grid else "•", end="")
        print()


def trench_size(input: list[str]) -> int:
    location: Point = Point(0, 0)
    grid: set[Point] = set()
    grid.add(location)
    left = 0
    right = 0
    bottom = 0
    top = 0
    dug_count = 1
    for line in input:
        character, count, _ = line.split()
        direction = Direction.from_character(character)
        for _ in range(int(count)):
            location = location.next_from_direction(direction)
            grid.add(location)
            dug_count += 1
            left = min(left, location.x)
            right = max(right, location.x)
            top = min(top, location.y)
            bottom = max(bottom, location.y)

    # Perform flood fill.
    to_visit = [Point(1, 1)]
    while to_visit:
        location = to_visit.pop()
        grid.add(location)
        dug_count += 1
        for d in Direction:
            p = location.next_from_direction(d)
            if p not in grid:
                to_visit.append(p)

    # print_grid(grid, left, right, top, bottom)
    return len(grid)


def trench_size_2(input: list[str]) -> int:
    result = 0

    for line in input:
        _, val = line.split("(#")
        meters = int(val[:5], 16)
        direction = Direction.from_numeral(val[5])

    return result


if __name__ == "__main__":
    part1test = trench_size(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 62

    """ 
    part2test = trench_size_2(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 952408144115
 """
    with open("day18.txt") as infile:
        lines = infile.read().splitlines()

    part1 = trench_size(lines)
    print(f"Part 1: {part1}")
    assert part1 == 106459

    """ 
    part2 = trench_size_2(lines)
    print(f"Part 2: {part2}")
 """
