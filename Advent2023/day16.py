from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Self

TEST = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class TileType(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    DOWN_RIGHT = 2
    DOWN_LEFT = 3


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def next_location(self, direction: Direction) -> Self:
        match direction:
            case Direction.UP:
                return Point(self.x, self.y - 1)
            case Direction.DOWN:
                return Point(self.x, self.y + 1)
            case Direction.LEFT:
                return Point(self.x - 1, self.y)
            case Direction.RIGHT:
                return Point(self.x + 1, self.y)


@dataclass(frozen=True)
class Beam:
    location: Point
    direction: Direction


def build_grid(lines: list[str]) -> tuple[dict[Point, TileType], int, int]:
    # Returns the grid and its width and height
    grid: dict[Point, TileType] = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            match c:
                case ".":
                    continue
                case "|":
                    grid[Point(x, y)] = TileType.VERTICAL
                case "-":
                    grid[Point(x, y)] = TileType.HORIZONTAL
                case "\\":
                    grid[Point(x, y)] = TileType.DOWN_RIGHT
                case "/":
                    grid[Point(x, y)] = TileType.DOWN_LEFT
    return grid, len(lines[0]), len(lines)


def count_energized_tiles(
    grid: dict[Point, TileType], width: int, height: int, start: Beam
) -> int:
    """Count the number of energized tiles with the given starting beam.

    Args:
        grid (dict[Point, TileType]): The grid of tiles.
        width (int): Width of the grid.
        height (int): Height of the grid.
        start (Beam): Initial beam state.

    Returns:
        int: Runs the grid with the initial beam state and returns the
        number of energized tiles.
    """
    energized: dict[Point, Direction] = defaultdict(set)
    beams: list[Beam] = [start]

    while beams:
        beam = beams.pop()
        while (
            0 <= beam.location.x < width
            and 0 <= beam.location.y < height
            and beam.direction not in energized[beam.location]
        ):
            energized[beam.location].add(beam.direction)
            if tile := grid.get(beam.location):
                match tile:
                    case TileType.VERTICAL:
                        match beam.direction:
                            case Direction.UP | Direction.DOWN:
                                # Up or Down continues in same direction.
                                beam = Beam(
                                    beam.location.next_location(beam.direction),
                                    beam.direction,
                                )
                            case Direction.RIGHT | Direction.LEFT:
                                # Left or Right splits into two beams: one going up and one going down.
                                beams.append(
                                    Beam(
                                        beam.location.next_location(Direction.UP),
                                        Direction.UP,
                                    )
                                )
                                beam = Beam(
                                    beam.location.next_location(Direction.DOWN),
                                    Direction.DOWN,
                                )
                    case TileType.HORIZONTAL:
                        match beam.direction:
                            case Direction.UP | Direction.DOWN:
                                # Up or Down splits into two beams: one going left and one going right.
                                beams.append(
                                    Beam(
                                        beam.location.next_location(Direction.LEFT),
                                        Direction.LEFT,
                                    )
                                )
                                beam = Beam(
                                    beam.location.next_location(Direction.RIGHT),
                                    Direction.RIGHT,
                                )
                            case Direction.RIGHT | Direction.LEFT:
                                # Left or Right continues in same direction.
                                beam = Beam(
                                    beam.location.next_location(beam.direction),
                                    beam.direction,
                                )
                    case TileType.DOWN_LEFT:
                        match beam.direction:
                            case Direction.UP:
                                beam = Beam(
                                    beam.location.next_location(Direction.RIGHT),
                                    Direction.RIGHT,
                                )
                            case Direction.RIGHT:
                                beam = Beam(
                                    beam.location.next_location(Direction.UP),
                                    Direction.UP,
                                )
                            case Direction.DOWN:
                                beam = Beam(
                                    beam.location.next_location(Direction.LEFT),
                                    Direction.LEFT,
                                )
                            case Direction.LEFT:
                                beam = Beam(
                                    beam.location.next_location(Direction.DOWN),
                                    Direction.DOWN,
                                )
                    case TileType.DOWN_RIGHT:
                        match beam.direction:
                            case Direction.UP:
                                beam = Beam(
                                    beam.location.next_location(Direction.LEFT),
                                    Direction.LEFT,
                                )
                            case Direction.RIGHT:
                                beam = Beam(
                                    beam.location.next_location(Direction.DOWN),
                                    Direction.DOWN,
                                )
                            case Direction.DOWN:
                                beam = Beam(
                                    beam.location.next_location(Direction.RIGHT),
                                    Direction.RIGHT,
                                )
                            case Direction.LEFT:
                                beam = Beam(
                                    beam.location.next_location(Direction.UP),
                                    Direction.UP,
                                )
            else:
                # Empty grid location. Beam continues in same direction.
                beam = Beam(beam.location.next_location(beam.direction), beam.direction)

    return len(energized)


def count_tiles_part_1(lines: list[str]) -> int:
    grid, width, height = build_grid(lines)
    return count_energized_tiles(
        grid, width, height, Beam(Point(0, 0), Direction.RIGHT)
    )


def find_most_tiles(lines: list[str]) -> int:
    grid, width, height = build_grid(lines)
    max_values: list[int] = []
    max_values.append(
        max(
            count_energized_tiles(
                grid, width, height, Beam(Point(0, y), Direction.RIGHT)
            )
            for y in range(height)
        )
    )

    max_values.append(
        max(
            count_energized_tiles(
                grid, width, height, Beam(Point(width - 1, y), Direction.LEFT)
            )
            for y in range(height)
        )
    )

    max_values.append(
        max(
            count_energized_tiles(
                grid, width, height, Beam(Point(x, 0), Direction.DOWN)
            )
            for x in range(width)
        )
    )

    max_values.append(
        max(
            count_energized_tiles(
                grid, width, height, Beam(Point(x, height - 1), Direction.UP)
            )
            for x in range(width)
        )
    )

    return max(max_values)


if __name__ == "__main__":
    part1test = count_tiles_part_1(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 46

    part2test = find_most_tiles(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 51

    with open("day16.txt") as infile:
        lines = infile.read().splitlines()

    part1 = count_tiles_part_1(lines)
    print(f"Part 1: {part1}")
    assert part1 == 8098

    part2 = find_most_tiles(lines)
    print(f"Part 2: {part2}")
