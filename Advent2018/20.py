from __future__ import annotations
from collections import defaultdict, namedtuple
from typing import Callable, List

from sortedcontainers import SortedSet

Point = namedtuple('Point', ['x', 'y'])


class Location(Point):
    def __repr__(self):
        return f"Location({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Location(self.x + other[0], self.y + other[1])

    def __mul__(self, other):
        return Location(self.x * other, self.y * other)

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __lt__(self, other):
        return self.y < other[1] or \
            self.y == other[1] and self.x < other[0]

    def __hash__(self):
        return hash((self.x, self.y))


class Map:
    def __init__(self):
        self.doors = SortedSet()
        self.walls = SortedSet()
        self.unknown = SortedSet()
        self.currentLocation = Location(0, 0)
        self.addLocation(self.currentLocation)
        self.moveDictionary = {"W": self.moveLeft, "N": self.moveUp,
                               "E": self.moveRight, "S": self.moveDown}
        self.goal = Location(0, 0)
        self.extentsCache = None

    def findExtents(self):
        if not self.extentsCache:
            minX = 1e12
            maxX = -1e12
            minY = 1e12
            maxY = -1e12
            all = self.doors | self.walls | self.unknown
            for coord in all:
                minX = min(minX, coord.x)
                maxX = max(maxX, coord.x)
                minY = min(minY, coord.y)
                maxY = max(maxY, coord.y)
            self.extentsCache = (minX, maxX, minY, maxY)
        return self.extentsCache

    def addLocation(self, location: Location):
        self.extentsCache = None
        left = Location(location.x - 1, location.y)
        if left not in self.doors and left not in self.walls:
            self.unknown.add(left)
        up = Location(location.x, location.y + 1)
        if up not in self.doors and up not in self.walls:
            self.unknown.add(up)
        right = Location(location.x + 1, location.y)
        if right not in self.doors and right not in self.walls:
            self.unknown.add(right)
        down = Location(location.x, location.y - 1)
        if down not in self.doors and down not in self.walls:
            self.unknown.add(down)

    def addDoor(self, doorLocation: Location):
        self.unknown.discard(doorLocation)
        self.doors.add(doorLocation)

    def move(self, offset):
        self.addDoor(self.currentLocation + offset)
        self.currentLocation = self.currentLocation + offset * 2
        self.addLocation(self.currentLocation)

    def moveLeft(self):
        self.move(Location(-1, 0))

    def moveUp(self):
        self.move(Location(0, 1))

    def moveRight(self):
        self.move(Location(1, 0))

    def moveDown(self):
        self.move(Location(0, -1))

    def moveInDirection(self, direction):
        self.moveDictionary[direction]()

    def moveTo(self, location):
        """
        Move back to a previously-visited location
        """
        self.currentLocation = location

    def successors(self, location: Location) -> List[Location]:
        locations: List[Location] = []
        # Left
        if location + Location(-1, 0) in self.doors:
            locations.append(location + Location(-2, 0))
        # Up
        if location + Location(0, 1) in self.doors:
            locations.append(location + Location(0, 2))
        # Right
        if location + Location(1, 0) in self.doors:
            locations.append(location + Location(2, 0))
        # Down
        if location + Location(0, -1) in self.doors:
            locations.append(location + Location(0, -2))
        return locations

    def finish(self):
        self.walls = self.unknown
        self.unknown = SortedSet()

    def print(self):
        minX, maxX, minY, maxY = self.findExtents()
        for y in range(maxY, minY - 1, -1):
            for x in range(minX, maxX + 1):
                if (y == 0) and (x == 0):
                    # Starting point
                    print('X', end='')
                elif (y & 1 == 0) and (x & 1 == 0):
                    # When both coordinates are even, it's a space we can move to
                    print('.', end='')
                elif(y & 1 == 1) and (x & 1 == 1):
                    # When both coordinates are odd, it's the corner of a wall
                    print('#', end='')
                else:
                    location = Location(x, y)
                    if location in self.walls:
                        print("#", end='')
                    elif location in self.unknown:
                        print("?", end='')
                    elif location in self.doors:
                        if y & 1 == 1:
                            # Doors in odd-numbered rows are horizontal
                            print('-', end='')
                        else:
                            # Doors in even-numbered rows are vertical
                            print('|', end='')
                    else:
                        print(' ', end='')
            print()
        print()

    def goalTest(self, location: Location) -> bool:
        return location == self.goal


def manhattanDistance(goal: Location) -> Callable[[Location], float]:
    def distance(location: Location) -> float:
        xdist: int = abs(location.x - goal.x)
        ydist: int = abs(location.y - goal.y)
        return xdist + ydist
    return distance

    """
    def countDoors(self):
        minX, maxX, minY, maxY = self.findExtents()
        for x in range(minX + 1, maxX, 2):
            for y in range(minY + 1, maxY, 2):
                doorCount = 0
                if Location(x - 1, y) in self.doors:
                    doorCount += 1
                if Location(x, y + 1) in self.doors:
                    doorCount += 1
                if Location(x + 1, y) in self.doors:
                    doorCount += 1
                if Location(x, y - 1) in self.doors:
                    doorCount += 1
                if doorCount != 2:
                    print(f"{Location(x, y)} has {doorCount} doors")
    """


def a20(fileName):
    with open(fileName, "r") as infile:
        inputLine = infile.readline()

    map = Map()
    locationStack = []
    distances = defaultdict(int)
    previousLocation = Location(0, 0)

    for char in inputLine:
        if char in "NEWS":
            map.moveInDirection(char)
            if distances[(map.currentLocation)] != 0:
                distances[map.currentLocation] = min(distances[map.currentLocation], distances[previousLocation] + 1)
            else:
                distances[map.currentLocation] = distances[previousLocation] + 1
        elif char == "(":
            locationStack.append(map.currentLocation)
        elif char == ")":
            map.moveTo(locationStack.pop())
        elif char == "|":
            map.moveTo(locationStack[-1])
        elif char == "^":
            continue
        elif char == "$":
            map.finish()
            # map.print()
            break
        else:
            raise ValueError(f"Encountered unexpected character: '{char}")
        previousLocation = map.currentLocation

    print(f"Furthest room requires passing {max(distances.values())} doors")
    print(f"Rooms at least 1000 steps away: {len([x for x in distances.values() if x >= 1000])}")


if __name__ == "__main__":
    a20("20.txt")
