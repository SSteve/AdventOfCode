from __future__ import annotations
from enum import IntEnum
from generic_search import bfs
from intcode import IntCode
from typing import Dict, NamedTuple

class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

class Point(NamedTuple):
    x: int
    y: int

    def north(self) -> Point:
        return Point(self.x, self.y - 1)

    def south(self) -> Point:
        return Point(self.x, self.y + 1)

    def west(self) -> Point:
        return Point(self.x - 1, self.y)

    def east(self) -> Point:
        return Point(self.x + 1, self.y)
        
    def around(self) -> Dict[Direction, Point]:
        return {Direction.NORTH: self.north(), Direction.SOUTH: self.south(), Direction.WEST: self.west(), Direction.EAST: self.east()}

class Droid:
    def __init__(self, computer: IntCode):
        self.computer = computer
        self.map: Dict[Point, int] = {}

    def found_oxygen_system(self, point: Point) -> bool:
        return self.map.get(point, -1) == 2

    def successors(self, point: Point) -> List[Point]:
        result: List[Point] = []
        for direction, new_point in point.around().items():
            location_code = self.map.get(new_point, -1)
            if location_code == -1:
                print(f"Direction: {direction}")
                self.computer.accept_input(direction)
                self.computer.run()
                location_code == self.computer.output_values.pop(0)
                self.map[new_point] = location_code
                print(new_point)
            if location_code != 0:
                result.append(new_point)
        return result

if __name__ == '__main__':
    with open("15.txt") as infile:
        computer = IntCode(infile.readline(), interactive=False)

    droid = Droid(computer)

    solution = bfs(Point(0, 0), droid.found_oxygen_system, droid.successors)
    print(solution)
