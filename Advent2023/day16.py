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


def build_grid(lines: list[str]) -> dict[Point, TileType]:
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
    return grid


def count_energized_tiles(lines: list[str]) -> int:
    grid = build_grid(lines)
    max_x = max(p.x for p in grid)
    max_y = max(p.y for p in grid)
    energized: dict[Point, Direction] = defaultdict(set)
    beams: list[Beam] = [Beam(Point(0, 0), Direction.RIGHT)]

    while beams:
        beam = beams.pop()
        while (
            0 <= beam.location.x <= max_x
            and 0 <= beam.location.y <= max_y
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


if __name__ == "__main__":
    part1test = count_energized_tiles(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 46

    """ 
    part2test = calculate_focusing_power(TEST)
    print(f"Part 2 test: {part2test}")
    assert part2test == 145
 """

    with open("day16.txt") as infile:
        lines = infile.read().splitlines()

    part1 = count_energized_tiles(lines)
    print(f"Part 1: {part1}")
    # assert part1 == 510273

    """ 
    part2 = calculate_focusing_power(lines)
    print(f"Part 2: {part2}")
 """
