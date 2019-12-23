from generic_search import bfs
from intcode import IntCode
from typing import Dict, NamedTuple

class Point(NamedTuple):
    x: int
    y: int

    def north(self):
        return Point(x, y - 1)

    def south(self):
        return Point(x, y + 1)

    def west(self):
        return Point(x - 1, y)

    def east(self):
        return Point(x + 1, y)

    

class Droid:
    def __init__(self, computer: IntCode):
        self.computer = computer
        self.location = Point(0, 0)
        self.status = -1
        self.map: Dict[Point, int] = {}
        self.directions: 

    def found_oxygen_system(self, point: Point) -> bool:
        return self.map.get(point, -1) == 2

    def successors(self, point: Point) -> List[Point]:
        result: List[Point] = []
        if self.location.north() not in self.map:
            self.computer.accept_input(1)
            self.computer.run()



if __name__ == '__main__':
    with open("15.txt") as infile:
        computer = IntCode(infile.readline(), interactive=False)

    droid = Droid(computer)

    solution = bfs(droid.location, droid.found_oxygen_system, droid.successors)
