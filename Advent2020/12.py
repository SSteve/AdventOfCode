import math
import re
from dataclasses import dataclass
from typing import Any, List

TEST = """F10
N3
F7
R90
F11"""


instructionRegex = re.compile(r"(.)(\d+)")


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Any) -> 'Point':
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        raise TypeError

    def __mul__(self, other: Any) -> 'Point':
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        raise TypeError


class Direction:
    directions = ['N', 'E', 'S', 'W']

    def __init__(self) -> None:
        # Start out heading East
        self.directionIndex = 1

    def Turn(self, instruction: str) -> None:
        match = instructionRegex.match(instruction)
        if not match:
            raise ValueError

        action = match[1]
        value = int(match[2]) // 90
        if action == 'L':
            value = -value
        self.directionIndex = (self.directionIndex + value) % 4

    def CurrentDirection(self) -> str:
        return Direction.directions[self.directionIndex]


class Ship:
    movementVectors = {'N': Point(0, 1), 'E': Point(1, 0), 'S': Point(0, -1), 'W': Point(-1, 0)}

    def __init__(self, shipType: int) -> None:
        self.position = Point(0, 0)
        self.direction = Direction()
        self.shipType = shipType
        self.waypoint = Point(10, 1)

    def Move(self, instruction: str) -> None:
        match = instructionRegex.match(instruction)
        if not match:
            raise ValueError

        moveVector = Ship.movementVectors[match[1]]
        moveAmount = int(match[2])
        if self.shipType == 1:
            self.position += moveVector * moveAmount
        else:
            self.waypoint += moveVector * moveAmount

    def GoForward(self, instruction: str) -> None:
        match = instructionRegex.match(instruction)
        if not match:
            raise ValueError

        if self.shipType == 1:
            moveVector = Ship.movementVectors[self.direction.CurrentDirection()]
        else:
            moveVector = self.waypoint
        moveAmount = int(match[2])
        self.position += moveVector * moveAmount

    def TurnWaypoint(self, instruction: str) -> Point:
        match = instructionRegex.match(instruction)
        if not match:
            raise ValueError

        action = match[1]
        radians = int(match[2]) / 360 * math.tau
        if action == 'R':
            radians = -radians
        newWaypointX = self.waypoint.x * math.cos(radians) - self.waypoint.y * math.sin(radians)
        newWaypointY = self.waypoint.x * math.sin(radians) + self.waypoint.y * math.cos(radians)
        return Point(round(newWaypointX), round(newWaypointY))

    def ManhattanDistance(self) -> int:
        return abs(self.position.x) + abs(self.position.y)

    def FollowInstructions(self, instructions: List[str]) -> None:
        for instruction in instructions:
            if instruction[0] in 'RL':
                if self.shipType == 1:
                    self.direction.Turn(instruction)
                else:
                    self.waypoint = self.TurnWaypoint(instruction)
            elif instruction[0] in 'NESW':
                self.Move(instruction)
            elif instruction[0] == 'F':
                self.GoForward(instruction)


if __name__ == "__main__":
    testShip = Ship(1)
    testInstructions = TEST.splitlines()
    testShip.FollowInstructions(testInstructions)
    testPart1 = testShip.ManhattanDistance()
    assert testPart1 == 25, f"Part 1 is {testPart1}. It should be 25."
    testShip2 = Ship(2)
    testShip2.FollowInstructions(testInstructions)
    testPart2 = testShip2.ManhattanDistance()
    assert testPart2 == 286, f"Part 2 is {testPart2}. It should be 286"

    ship = Ship(1)
    with open("12.txt", "r") as infile:
        instructions = infile.read().splitlines()
    ship.FollowInstructions(instructions)
    part1 = ship.ManhattanDistance()
    print(f"Part 1: {part1}")
    ship2 = Ship(2)
    ship2.FollowInstructions(instructions)
    part2 = ship2.ManhattanDistance()
    print(f"Part 2: {part2}")
