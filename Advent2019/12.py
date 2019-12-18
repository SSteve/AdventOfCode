from __future__ import annotations
import re
from itertools import combinations
from math import sqrt
from typing import Iterable, NamedTuple, Pattern

class SpacePoint:
    """Because everything was a Space Thing yesterday"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other: SpacePoint) -> SpacePoint:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

    def __add__(self, other: SpacePoint) -> SpacePoint:
        return SpacePoint(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other: SpacePoint):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}"

class Moon:
    def __init__(self, x: int, y: int, z: int, velX: int = 0, velY: int = 0, velZ: int = 0):
        self.position: SpacePoint = SpacePoint(x, y, z)
        self.velocity: SpacePoint = SpacePoint(velX, velY, velZ)

    def __repr__(self):
        return (f"Position: {self.position}, Velocity: {self.velocity}")

    def __eq__(self, other: Moon):
        return self.position == other.position and self.velocity == other.velocity

    def __hash__(self):
        return hash((self.position, self.velocity))

    def applyGravity(self, other: Moon):
        if other.position.x > self.position.x:
            self.velocity.x += 1
        elif other.position.x < self.position.x:
            self.velocity.x -= 1
        if other.position.y > self.position.y:
            self.velocity.y += 1
        elif other.position.y < self.position.y:
            self.velocity.y -= 1
        if other.position.z > self.position.z:
            self.velocity.z += 1
        elif other.position.z < self.position.z:
            self.velocity.z -= 1

    def applyVelocity(self):
        self.position += self.velocity

    def energy(self):
        return (abs(self.position.x) + abs(self.position.y) + abs(self.position.z)) * \
            (abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z))

TEST_POSITIONS = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

def applyGravity(moons: Iterable[Moon]):
    for pair in combinations(moons, 2):
        pair[0].applyGravity(pair[1])
        pair[1].applyGravity(pair[0])
    for moon in moons:
        moon.applyVelocity()


if __name__ == '__main__':
    positionCompiler: Pattern = re.compile(r"<x=([\-\d]+), y=([\-\d]+), z=([\-\d]+)>")

    moons = []
    for line in TEST_POSITIONS.split('\n'):
        match = positionCompiler.match(line)
        if match:
            moons.append(Moon(int(match[1]), int(match[2]), int(match[3])))
    assert(moons[0] == Moon(-1, 0, 2))
    assert(moons[1] == Moon(2, -10, -7))
    assert(moons[2] == Moon(4, -8, 8))
    assert(moons[3] == Moon(3, 5, -1))
    applyGravity(moons)
    assert(moons[0] == Moon(2, -1, 1, 3, -1, -1))
    assert(moons[1] == Moon(3, -7, -4, 1, 3, 3))
    assert(moons[2] == Moon(1, -7, 5, -3, 1, -3))
    assert(moons[3] == Moon(2, 2, 0, -1, -3, 1))
    applyGravity(moons)
    assert(moons[0] == Moon(5, -3, -1, 3, -2, -2))
    assert(moons[1] == Moon(1, -2, 2, -2, 5, 6))
    assert(moons[2] == Moon(1, -4, -1, 0, 3, -6))
    assert(moons[3] == Moon(1, -4, 2, -1, -6, 2))
    for _ in range(8):
        applyGravity(moons)
    assert(sum((moon.energy() for moon in moons)) == 179)
    

    moons = []
    with open("12.txt") as infile:
        for line in infile:
            match = positionCompiler.match(line)
            if match:
                moons.append(Moon(int(match[1]), int(match[2]), int(match[3])))
    for _ in range(1000):
        applyGravity(moons)
    print(sum((moon.energy() for moon in moons)))

    #print(moons)
