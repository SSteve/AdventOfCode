from __future__ import annotations

import copy

from enum import IntEnum
from generic_search import bfs, nodeToPath
from intcode import IntCode
from typing import Dict, List, NamedTuple, Set

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
    master_map: Dict[Point, int] = {}

    def __init__(self, computer: IntCode):
        self.computer = computer
        self.map: Dict[Point, int] = {}
        self.position = Point(0, 0)

    def __eq__(self, other: Droid) -> bool:
        return self.position == other.position

    def __hash__(self) -> int:
        return hash(self.position)

    def clone(self) -> Droid:
        new_droid = Droid(copy.deepcopy(self.computer))
        new_droid.map = copy.deepcopy(self.map)
        new_droid.position = self.position
        return new_droid

    def move(self, direction: Direction, new_point: Point) -> int:
        self.computer.accept_input(direction)
        self.computer.run()
        location_code = self.computer.output_values.pop(0)
        self.map[new_point] = location_code
        Droid.master_map[new_point] = location_code
        if location_code != 0:
            self.position = new_point
        return location_code

    @classmethod
    def found_oxygen_system(cls, droid: Droid) -> bool:
        return droid.map.get(droid.position, -1) == 2

    @classmethod
    def successors(cls, droid: Droid) -> List[Droid]:
        result: List[Droid] = []
        for direction, new_point in droid.position.around().items():
            new_droid = droid.clone()
            location_code = new_droid.move(direction, new_point)
            if location_code != 0:
                result.append(new_droid)
        return result

def always_false(droid: Droid) -> bool:
    return False

TILES: Dict[int, str] = {0: "X", 1: " ", 2: "o"}

if __name__ == '__main__':
    with open("15.txt") as infile:
        computer = IntCode(infile.readline(), interactive=False)

    droid = Droid(computer)

    solution = bfs(droid, Droid.found_oxygen_system, Droid.successors)
    path = nodeToPath(solution)

    # 217 is too high.
    # Subtract 1 because we don't count the initial location. (This is the stupid
    # mistake that took a lot of time on this problem.)
    print(f"{len(path) - 1} steps to oxygen system")

    # Now do it again.
    with open("15.txt") as infile:
        computer = IntCode(infile.readline(), interactive=False)

    droid = Droid(computer)
    Droid.master_map = {}
    # This time always return false for the solution so that it explores the entire maze.
    solution = bfs(droid, always_false, Droid.successors)

    min_x = min(p.x for p in Droid.master_map.keys())
    min_y = min(p.y for p in Droid.master_map.keys())
    max_y = max(p.y for p in Droid.master_map.keys())
    x_offset = 5 - min_x
    y_offset = 8 - min_y
    for point, location_code in Droid.master_map.items():
        print(f"\033[{point.y + y_offset};{point.x + x_offset}H{TILES[location_code]}", end='')
        if location_code == 2:
            next_round = [point]

    rounds = 0
    while len(next_round) > 0:
        current_round = next_round[:]
        next_round.clear()
        for point in current_round:
            for new_point in point.around().values():
                if Droid.master_map[new_point] == 1:
                    next_round.append(new_point)
                    Droid.master_map[new_point] = 2
        for point in next_round:
            print(f"\033[{point.y + y_offset};{point.x + x_offset}H{TILES[Droid.master_map[point]]}", end='')
        rounds += 1

    # 327 is too high
    # 326 is right. Another off-by-one error.
    print(f"\033[{max_y - min_y + 9};0H{rounds - 1} rounds for oxygen to spread")
        



    print(f"\033[{max_y - min_y + 10};0H ")
