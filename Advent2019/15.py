from generic_search import bfs
from intcode import IntCode
from typing import Dict, NamedTuple

class Point(NamedTuple):
    x: int
    y: int


class Droid:
    def __init__(self, computer: IntCode):
        self.computer = computer
        self.location = Point(0, 0)
        self.status = -1
        self.map: Dict[Point, int] = {}

    def found_oxygen_system(self, point: Point) -> bool:
        return self.map.get(point, -1) == 2

if __name__ == '__main__':
    with open("15.txt") as infile:
        computer = IntCode(infile.readline(), interactive=False)

    droid = Droid(computer)

    solution = bfs(droid.location, droid.found_oxygen_system, droid.successors)
