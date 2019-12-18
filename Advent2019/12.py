from __future__ import annotations

import copy
import re

from dataclasses import dataclass
from itertools import combinations
from math import gcd, sqrt
from typing import Iterable, List, NamedTuple, Pattern

@dataclass
class SpacePoint:
    """Because everything was a Space Thing yesterday"""
    x: int
    y: int
    z: int

    def distance_to(self, other: SpacePoint) -> SpacePoint:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

    def __add__(self, other: SpacePoint) -> SpacePoint:
        return SpacePoint(self.x + other.x, self.y + other.y, self.z + other.z)

@dataclass
class CoordinateState:
    pos: int
    vel: int

    def applyGravity(self, other: CoordinateState):
        if other.pos > self.pos:
            self.vel += 1
        elif other.pos < self.pos:
            self.vel -= 1
        
    def applyVelocity(self):
        self.pos += self.vel

class Moon:
    def __init__(self, x: int, y: int, z: int, velX: int = 0, velY: int = 0, velZ: int = 0):
        self.coordinates = []
        self.coordinates.append(CoordinateState(x, velX))
        self.coordinates.append(CoordinateState(y, velY))
        self.coordinates.append(CoordinateState(z, velZ))

    @property
    def x(self) -> int:
        return self.coordinates[0].pos
    
    @property
    def y(self) -> int:
        return self.coordinates[1].pos

    @property
    def z(self) -> int:
        return self.coordinates[2].pos

    @property
    def velX(self) -> int:
        return self.coordinates[0].vel

    @property
    def velY(self) -> int:
        return self.coordinates[1].vel

    @property
    def velZ(self) -> int:
        return self.coordinates[2].vel

    @property
    def position(self) -> SpacePoint:
        return SpacePoint(self.x, self.y, self.z)

    @property
    def velocity(self) -> SpacePoint:
        return SpacePoint(self.velX, self.velY, self.velZ)

    def __repr__(self):
        return (f"Position: ({self.position}), Velocity: ({self.velocity})")

    def __eq__(self, other: Moon):
        return self.position == other.position and self.velocity == other.velocity

    def __hash__(self):
        return hash((self.position, self.velocity))

    def applyGravity(self, other: Moon):
        """Adjust this moon's velocity based on the relative position with the other moon"""
        for i in range(len(self.coordinates)):
            self.coordinates[i].applyGravity(other.coordinates[i])

    def applyVelocity(self):
        """Use this moon's velocity to update its position"""
        for coordinate in self.coordinates:
            coordinate.applyVelocity()

    def energy(self):
        posEnergy = sum((abs(coord.pos) for coord in self.coordinates))
        velEnergy = sum((abs(coord.vel) for coord in self.coordinates))
        return posEnergy * velEnergy

TEST_POSITIONS = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

TEST_POSITIONS_2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""

def performMoonStep(moons: Iterable[Moon]):
    for pair in combinations(moons, 2):
        pair[0].applyGravity(pair[1])
        pair[1].applyGravity(pair[0])
    for moon in moons:
        moon.applyVelocity()

def performCoordStep(coords: Iterable[CoordinateState]):
    for pair in combinations(coords, 2):
        pair[0].applyGravity(pair[1])
        pair[1].applyGravity(pair[0])
    for coord in coords:
        coord.applyVelocity()

def calculateCoordCycle(coords: Iterable[CoordinateState]) -> int:
    originalCoords: Iterable[CoordinateState] = copy.deepcopy(coords)
    cycleLength: int = 1
    performCoordStep(coords)
    while coords != originalCoords:
        performCoordStep(coords)
        cycleLength += 1
    return cycleLength

def calculateMoonCycle(moons: Iterable[Moon]) -> int:
    xCoords: List[CoordinateState] = []
    yCoords: List[CoordinateState] = []
    zCoords: List[CoordinateState] = []
    for moon in moons:
        xCoords.append(CoordinateState(moon.x, moon.velX))
        yCoords.append(CoordinateState(moon.y, moon.velY))
        zCoords.append(CoordinateState(moon.z, moon.velZ))

    xCycleLength = calculateCoordCycle(xCoords)
    yCycleLength = calculateCoordCycle(yCoords)
    zCycleLength = calculateCoordCycle(zCoords)

    return lcm(lcm(xCycleLength, yCycleLength), zCycleLength)

def lcm(a: int, b:int) -> int:
    return abs(a * b) // gcd(a, b)

if __name__ == '__main__':
    positionCompiler: Pattern = re.compile(r"<x=([\-\d]+), y=([\-\d]+), z=([\-\d]+)>")

    moons: List[Moon] = []
    originalMoons: List[Moon] = []
    for line in TEST_POSITIONS.split('\n'):
        match = positionCompiler.match(line)
        if match:
            moons.append(Moon(int(match[1]), int(match[2]), int(match[3])))
    originalMoons = copy.deepcopy(moons)

    assert(moons[0] == Moon(-1, 0, 2))
    assert(moons[1] == Moon(2, -10, -7))
    assert(moons[2] == Moon(4, -8, 8))
    assert(moons[3] == Moon(3, 5, -1))
    performMoonStep(moons)
    assert(moons[0] == Moon(2, -1, 1, 3, -1, -1))
    assert(moons[1] == Moon(3, -7, -4, 1, 3, 3))
    assert(moons[2] == Moon(1, -7, 5, -3, 1, -3))
    assert(moons[3] == Moon(2, 2, 0, -1, -3, 1))
    performMoonStep(moons)
    assert(moons[0] == Moon(5, -3, -1, 3, -2, -2))
    assert(moons[1] == Moon(1, -2, 2, -2, 5, 6))
    assert(moons[2] == Moon(1, -4, -1, 0, 3, -6))
    assert(moons[3] == Moon(1, -4, 2, -1, -6, 2))

    # Make sure original moons didn't get modified
    assert(originalMoons[0] == Moon(-1, 0, 2))
    assert(originalMoons[1] == Moon(2, -10, -7))
    assert(originalMoons[2] == Moon(4, -8, 8))
    assert(originalMoons[3] == Moon(3, 5, -1))

    for _ in range(8):
        performMoonStep(moons)
    assert(sum((moon.energy() for moon in moons)) == 179)

    assert(calculateMoonCycle(originalMoons) == 2772)

    moons.clear()
    for line in TEST_POSITIONS_2.split('\n'):
        match = positionCompiler.match(line)
        if match:
            moons.append(Moon(int(match[1]), int(match[2]), int(match[3])))
    assert(calculateMoonCycle(moons) == 4686774924)

    moons.clear()
    with open("12.txt") as infile:
        for line in infile:
            match = positionCompiler.match(line)
            if match:
                moons.append(Moon(int(match[1]), int(match[2]), int(match[3])))
    originalMoons = copy.deepcopy(moons)
    for _ in range(1000):
        performMoonStep(moons)
    print(f"Energy after 1000 steps: {sum((moon.energy() for moon in moons))}")

    print(f"Cycle length: {calculateMoonCycle(originalMoons)}")
