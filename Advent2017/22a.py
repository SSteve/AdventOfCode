from enum import IntEnum
from collections import defaultdict


class Direction(IntEnum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def turnLeft(self):
        return Direction((self - 1) % len(Direction))

    def turnRight(self):
        return Direction((self + 1) % len(Direction))

    def reverse(self):
        return Direction((self + 2) % len(Direction))


class InfectionState(IntEnum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3

    def nextState(self):
        return InfectionState((self + 1) % len(InfectionState))


class Sporifica:
    xOffsets = {
        Direction.LEFT: -1,
        Direction.UP: 0,
        Direction.RIGHT: 1,
        Direction.DOWN: 0
    }
    yOffsets = {
        Direction.LEFT: 0,
        Direction.UP: -1,
        Direction.RIGHT: 0,
        Direction.DOWN: 1
    }

    def __init__(self, x, y, infected):
        self.x = x
        self.y = y
        self.infected = infected
        self.direction = Direction.UP
        self.infectionCount = 0

    def burst(self):
        currentNode = self.infected[(self.x, self.y)]
        if currentNode == InfectionState.CLEAN:
            self.direction = self.direction.turnLeft()
        elif currentNode == InfectionState.INFECTED:
            self.direction = self.direction.turnRight()
        elif currentNode == InfectionState.FLAGGED:
            self.direction = self.direction.reverse()

        currentNode = currentNode.nextState()
        if currentNode == InfectionState.INFECTED:
            self.infectionCount += 1
        self.infected[(self.x, self.y)] = currentNode

        self.x += Sporifica.xOffsets[self.direction]
        self.y += Sporifica.yOffsets[self.direction]

    def bursts(self, burstCount):
        for i in range(burstCount):
            self.burst()
            # if i % 100000 == 0:
            #    print(i // 100000)


def day22(fileName):
    infected = defaultdict(lambda: InfectionState.CLEAN)
    with open(fileName) as infile:
        for lineNumber, line in enumerate(infile):
            for columnNumber, char in enumerate(line):
                if char == "#":
                    infected[(columnNumber, lineNumber)] = InfectionState.INFECTED
    print(f"Grid: {columnNumber} by {lineNumber}")
    sporifica = Sporifica(columnNumber // 2, lineNumber // 2, infected.copy())
    sporifica.bursts(100)
    print(f"After 100: {sporifica.infectionCount}")
    sporifica.bursts(10000000 - 100)
    print(f"After 10,000,000: {sporifica.infectionCount}")


if __name__ == "__main__":
    day22("22test.txt")
    day22("22.txt")
