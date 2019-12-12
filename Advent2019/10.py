# Using NamedTuple and typing for the first time this season

from __future__ import annotations
from collections import defaultdict
from itertools import chain
from math import gcd, atan2, tau, inf, sqrt
from typing import NamedTuple, List, Iterable, Set, Tuple, DefaultDict


class Point(NamedTuple):
    x: int = 0
    y: int = 0

    def simplified(self) -> Point:
        """
        Returns the point divided by the gcd of x and y

        e.g. simplified(Point(6, 2)) returns Point(3, 1)
        simplified(Point(-12, 4)) returns Point(-3, 1)
        """
        common_divisor = abs(gcd(self.x, self.y))
        return Point(self.x // common_divisor, self.y // common_divisor)

    def within_bounds(self, x: int, y: int) -> bool:
        return 0 <= self.x < x and 0 <= self.y < y

    def distance_to(self, other: Point) -> Point:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: object) -> Point:
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        raise TypeError("Points can only be multiplied by an int")

    def __div__(self, other:object) -> Point:
        if isinstance(other, int):
            return Point(self.x // other, self.y // other)
        raise TypeError("Points can only be divided by ints")

class AsteroidMap:
    def __init__(self, asteroid_map: Iterable[str]):
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

        # I'm sure there's a more pythonic way of doing this
        for p in self.locations:
            if p not in blocked:
                result += 1

        return result

    def best_location(self) -> Tuple[Point, int]:
        result = Point(-1, -1)
        max_count = -1
        for location in self.locations:
            visible = self.visible_count(location)
            if visible > max_count:
                max_count = visible
                result = location

        return result, max_count

    def nearest(self, origin: Point, indices: Iterable[int]):
        """Return the index of the point closest to origin"""
        lowest_distance: int = inf
        nearest_index: int = -1
        for index in indices:
            distance = origin.distance_to(self.locations[index])
            if distance < lowest_distance:
                lowest_distance = distance
                nearest_index = index
        return nearest_index

    def vaporize_asteroids(self, origin: Point, stop_count = 200) -> Point:
        """Vaporize visible asteroids until reaching stop_count and return the location of the last vaporized asteroid"""
        angles: DefaultDict[float, List[int]] = defaultdict(list)
        up_angle = atan2(1, 0)
        # Create a dictionary of all the asteroids at a given angle.
        for index, point in enumerate(self.locations):
            if point == origin:
                pass
            difference = point - origin
            # Negate y because y goes up in trig but y goes down in the map.
            # Spending a lot of time before figuring this out was my stupid mistake for this problem.
            angle = atan2(-difference.y, difference.x)
            # We want 90° to be 0 and everything else to go up from there.
            # atan2 returns -pi to pi. This converts it to -3*pi/2 to pi/2.
            if angle > up_angle:
                angle = angle - tau
            # Now rotate 90° so up is 0.
            angle -= up_angle
            # Negate to switch from counter-clockwise to clockwise.
            angle = -angle
            angles[angle].append(index)
        sortedAngles = dict(sorted(angles.items()))
        vaporized = 0
        while vaporized < stop_count:
            for angle in sortedAngles.keys():
                indices = sortedAngles[angle]
                if len(indices) > 0:
                    vaporized_index = indices[0] if len(indices) == 1 else self.nearest(origin, indices)
                    indices.remove(vaporized_index)
                    vaporized += 1
                    if vaporized >= stop_count:
                        break
        return self.locations[vaporized_index]


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

TEST6 = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##"""

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

    asteroids = AsteroidMap(TEST6.split('\n'))
    assert asteroids.vaporize_asteroids(Point(8, 3), 9) == Point(15, 1)

    with open("10.txt") as infile:
        asteroids = AsteroidMap(infile)
    location, visible = asteroids.best_location()
    print(f"{visible} asteroids visible from {location}")
    
    print(f"200th vaporized asteroid is at {asteroids.vaporize_asteroids(location)}")
