from enum import IntEnum


class Direction(IntEnum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def turnLeft(self):
        return Direction((self - 1) % len(Direction))

    def turnRight(self):
        return Direction((self + 1) % len(Direction))


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
        if (self.x, self.y) in self.infected:
            self.direction = self.direction.turnRight()
            self.infected.discard((self.x, self.y))
        else:
            self.direction = self.direction.turnLeft()
            self.infected.add((self.x, self.y))
            self.infectionCount += 1
        self.x += Sporifica.xOffsets[self.direction]
        self.y += Sporifica.yOffsets[self.direction]

    def bursts(self, burstCount):
        for _ in range(burstCount):
            self.burst()


def day22(fileName):
    infected = set()
    with open(fileName) as infile:
        for lineNumber, line in enumerate(infile):
            for columnNumber, char in enumerate(line):
                if char == "#":
                    infected.add((columnNumber, lineNumber))
    print(columnNumber, lineNumber)
    sporifica = Sporifica(columnNumber // 2, lineNumber // 2, infected.copy())
    sporifica.bursts(10000)
    print(sporifica.infectionCount)


if __name__ == "__main__":
    day22("22.txt")
