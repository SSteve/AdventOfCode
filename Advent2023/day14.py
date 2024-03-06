from dataclasses import dataclass

TEST = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class RockMap:
    rocks: set[Point]
    cubes: set[Point]
    width: int
    height: int

    def __init__(self, lines: list[str]):
        self.rocks = set()
        self.cubes = set()
        self.width = len(lines[0])
        self.height = len(lines)
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    self.cubes.add(Point(x, y))
                elif c == "O":
                    self.rocks.add(Point(x, y))

    def cube_at_coordinate(self, x: int, y: int) -> bool:
        point = Point(x, y)
        return point in self.cubes

    def rock_at_coordinate(self, x: int, y: int) -> bool:
        point = Point(x, y)
        return point in self.rocks

    def remove_rock_at_coordinate(self, x: int, y: int) -> None:
        self.rocks.remove(Point(x, y))

    def add_rock_at_coordinate(self, x: int, y: int) -> None:
        self.rocks.add(Point(x, y))


def calculate_north_load(lines: list[str]) -> int:
    rock_map = RockMap(lines)

    for x in range(rock_map.width):
        previous_cube = -1
        y = 0
        rock_coordinates: set[int] = set()
        while y <= rock_map.height:
            if rock_map.rock_at_coordinate(x, y):
                rock_coordinates.add(y)
            elif rock_map.cube_at_coordinate(x, y) or y == rock_map.height:
                for rock_y in rock_coordinates:
                    rock_map.remove_rock_at_coordinate(x, rock_y)
                for rock_y in range(previous_cube + 1, previous_cube + 1 + len(rock_coordinates)):
                    rock_map.add_rock_at_coordinate(x, rock_y)
                rock_coordinates.clear()
                previous_cube = y
            y += 1

    load = 0
    for rock in rock_map.rocks:
        load += rock_map.height - rock.y

    return load


if __name__ == "__main__":
    part1test = calculate_north_load(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 136

    """ 
    part2test = calculate_north_load(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 1030
 """

    with open("day14.txt") as infile:
        lines = infile.read().splitlines()

    part1 = calculate_north_load(lines)
    print(f"Part 1: {part1}")
    # assert part1 == 9403026

    """ 
    part2 = calculate_north_load(lines)
    print(f"Part 2: {part2}")
 """
