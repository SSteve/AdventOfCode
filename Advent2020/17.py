import math
from collections import namedtuple
from typing import Iterable, List, Set, Tuple

Point = namedtuple('Point','x, y, z')
Point4d = namedtuple('Point4d','x, y, z, w')

TEST = """.#.
..#
###"""

def BuildSpace(lines: List[str]) -> Set[Point]:
    space = set()
    y = 0
    for line in lines:
        x = 0
        for chr in line:
            if chr == '#':
                space.add(Point(x, y, 0))
            x += 1
        y += 1
    return space
    
def BuildSpace4d(lines: List[str]) -> Set[Point4d]:
    space = set()
    y = 0
    for line in lines:
        x = 0
        for chr in line:
            if chr == '#':
                space.add(Point4d(x, y, 0, 0))
            x += 1
        y += 1
    return space
    

def MinMaxCoord(coordIndex: int, space: Set[Tuple]) -> Tuple[int, int]:
    minCoord = min(p[coordIndex] for p in space)
    maxCoord = max(p[coordIndex] for p in space)
    return (minCoord, maxCoord)
    
    
def Surround(point: Point) -> Iterable[Point]:
    for x in range(point.x - 1, point.x + 2):
        for y in range(point.y - 1, point.y + 2):
            for z in range(point.z - 1, point.z + 2):
                if not (x == point.x and y == point.y and z == point.z):
                    yield Point(x, y, z)
                    
def Surround4d(point: Point4d) -> Iterable[Point4d]:
    for x in range(point.x - 1, point.x + 2):
        for y in range(point.y - 1, point.y + 2):
            for z in range(point.z - 1, point.z + 2):
                for w in range(point.w - 1, point.w + 2):
                    if not (x == point.x and y == point.y and z == point.z and w == point.w):
                        yield Point4d(x, y, z, w)
                    

def Generation(space: Set[Point]) -> Set[Point]:
    newSpace = set()
    minX, maxX = MinMaxCoord(0, space)
    minY, maxY = MinMaxCoord(1, space)
    minZ, maxZ = MinMaxCoord(2, space)
    for x in range(minX - 1, maxX + 2):
        for y in range(minY - 1, maxY + 2):
            for z in range(minZ - 1, maxZ + 2):
                thisPoint = Point(x, y, z)
                neighbors = sum(p in space for p in Surround(thisPoint))
                if neighbors == 3 and not(thisPoint in space):
                    newSpace.add(thisPoint)
                elif neighbors in (2, 3) and thisPoint in space:
                    newSpace.add(thisPoint)
    return newSpace
    
def Generation4d(space: Set[Point4d]) -> Set[Point4d]:
    newSpace = set()
    minX, maxX = MinMaxCoord(0, space)
    minY, maxY = MinMaxCoord(1, space)
    minZ, maxZ = MinMaxCoord(2, space)
    minW, maxW = MinMaxCoord(3, space)
    for x in range(minX - 1, maxX + 2):
        for y in range(minY - 1, maxY + 2):
            for z in range(minZ - 1, maxZ + 2):
                for w in range(minW - 1, maxW + 2):
                    thisPoint = Point4d(x, y, z, w)
                    neighbors = sum(p in space for p in Surround4d(thisPoint))
                    if neighbors == 3 and not(thisPoint in space):
                        newSpace.add(thisPoint)
                    elif neighbors in (2, 3) and thisPoint in space:
                        newSpace.add(thisPoint)
    return newSpace

def PrintSpace(space: Set[Point]) -> None:
    minX, maxX = MinMaxCoord(0, space)
    minY, maxY = MinMaxCoord(1, space)
    minZ, maxZ = MinMaxCoord(2, space)
    for z in range(minZ, maxZ + 1):
        print(f"z={z}")
        for y in range(minY, maxY + 1):
            for x in range(minX, maxX + 1):
                if Point(x, y, z) in space:
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        print()
        
def PrintSpace4d(space: Set[Point4d]) -> None:
    minX, maxX = MinMaxCoord(0, space)
    minY, maxY = MinMaxCoord(1, space)
    minZ, maxZ = MinMaxCoord(2, space)
    minW, maxW = MinMaxCoord(3, space)
    for w in range(minW, maxW + 1):
        for z in range(minZ, maxZ + 1):
            print(f"z={z}, w={w}")
            for y in range(minY, maxY + 1):
                for x in range(minX, maxX + 1):
                    if Point4d(x, y, z, w) in space:
                        print('#', end='')
                    else:
                        print('.', end='')
                print()
            print()
        

testSpace = BuildSpace(TEST.splitlines())
for _ in range(6):
    testSpace = Generation(testSpace)
assert len(testSpace) == 112

testSpace = BuildSpace4d(TEST.splitlines())
for i in range(6):
    if i < 3:
        PrintSpace4d(testSpace)
    testSpace = Generation4d(testSpace)
assert len(testSpace) == 848

with open("17.txt", "r") as infile:
    space = BuildSpace(infile.read().splitlines())
for _ in range(6):
    space = Generation(space)
print(len(space))

with open("17.txt", "r") as infile:
    space = BuildSpace4d(infile.read().splitlines())
for _ in range(6):
    space = Generation4d(space)
print(len(space))

