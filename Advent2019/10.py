# Using NamedTuple and typing for the first time this season

from __future__ import annotations
from itertools import chain
from math import gcd
from typing import NamedTuple, List, Iterable, Set, Tuple


class Point(NamedTuple):
    x: int = 0
    y: int = 0

    def simplified(self) -> Point:
        """
        Returns the point divided by the gcd of x and y

        e.g. simplified(Point(6, 2)) return Point(3, 1)
        """
        common_divisor = abs(gcd(self.x, self.y))
        return Point(self.x // common_divisor, self.y // common_divisor)

    def within_bounds(self, x: int, y: int) -> bool:
        return 0 <= self.x < x and 0 <= self.y < y

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: object):
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        raise TypeError("Points can only be multiplied by an int")

    def __div__(self, other:object):
        if isinstance(other, int):
            return Point(self.x // other, self.y // other)
        raise TypeError("Points can only be divided by ints")

class AsteroidMap:
    def __init__(self, asteroid_map: Iterable[str]) -> List[Point]:
        self.locations = []
        self.height = 0
        self.width = 0
        for y, row in enumerate(asteroid_map):
            row = row.strip()
            if len(row) > 0:
                self.height += 1
                self.width = len(row)
                for x, map_char in enumerate(row.strip()):
                    if map_char == "#":
                        self.locations.append(Point(x, y))

    def visible_count(self, location: Point) -> int:
        i = self.locations.index(location)
        blocked: Set[Point] = set()
        # As a naive form of optimization, check the nearer neighbors first as they will block
        # more distant neighbors
        for other_asteroid_index in chain(range(i-1, -1, -1), range(i+1, len(self.locations))):
            other_asteroid = self.locations[other_asteroid_index]
            if other_asteroid in blocked:
                continue
            offset = other_asteroid - location
            delta = offset.simplified()
            test_location = other_asteroid
            while (test_location + delta).within_bounds(self.width, self.height):
                test_location += delta
                blocked.update([test_location])
        result = -1 # Start at -1 because the location does not block itself
        for p in self.locations:
            if p not in blocked:
                result += 1
        return result

    def best_location(self) -> Tuple[Point, count]:
        result = Point(-1, -1)
        max_count = -1
        for location in self.locations:
            visible = self.visible_count(location)
            if visible > max_count:
                max_count = visible
                result = location

        return result, max_count

TEST1 = """.#..#
.....
#####
....#
...##"""

TEST2 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

TEST3 = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""

TEST4 = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""

TEST5 = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

if __name__ == '__main__':
    asteroids = AsteroidMap(TEST1.split('\n'))
    location, visible = asteroids.best_location()
    assert asteroids.visible_count(Point(1, 0)) == 7, "Wrong visible count for 1, 0"
    assert asteroids.visible_count(Point(4, 0)) == 7, "Wrong visible count for 4, 0"
    assert asteroids.visible_count(Point(0, 2)) == 6, "Wrong visible count for 0, 2"
    assert asteroids.visible_count(Point(1, 2)) == 7, "Wrong visible count for 1, 2"
    assert asteroids.visible_count(Point(2, 2)) == 7, "Wrong visible count for 2, 2"
    assert asteroids.visible_count(Point(3, 2)) == 7, "Wrong visible count for 3, 2"
    assert asteroids.visible_count(Point(4, 2)) == 5, "Wrong visible count for 4, 2"
    assert asteroids.visible_count(Point(4, 3)) == 7, "Wrong visible count for 4, 3"
    assert asteroids.visible_count(Point(3, 4)) == 8, "Wrong visible count for 3, 4"
    assert asteroids.visible_count(Point(4, 4)) == 7, "Wrong visible count for 4, 4"
    assert location == Point(3, 4), f"Wrong location for test 1: {location}"
    assert visible == 8, f"Wrong count for test 1: {visible}"
    
    asteroids = AsteroidMap(TEST2.split('\n'))
    location, visible = asteroids.best_location()
    assert location == Point(5, 8)
    assert visible == 33
    
    asteroids = AsteroidMap(TEST3.split('\n'))
    location, visible = asteroids.best_location()
    assert location == Point(1, 2)
    assert visible == 35

    asteroids = AsteroidMap(TEST4.split('\n'))
    location, visible = asteroids.best_location()
    assert location == Point(6, 3)
    assert visible == 41
    
    asteroids = AsteroidMap(TEST5.split('\n'))
    location, visible = asteroids.best_location()
    assert location == Point(11, 13)
    assert visible == 210

    with open("10.txt") as infile:
        asteroids = AsteroidMap(infile)
    location, visible = asteroids.best_location()
    print(f"{visible} asteroids visible from {location}")
    