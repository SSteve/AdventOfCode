from dataclasses import dataclass
from enum import Enum
from typing import Iterable

TEST0 = """...>...
.......
......>
v.....>
......>
.......
..vvv.."""

TEST = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Cuke(Enum):
    EAST = 1
    SOUTH = 2


class SeaCucumbers:
    def __init__(self, lines: list[str]) -> None:
        self.width = len(lines[0].strip())
        self.height = len(lines)
        self.map: dict[Point, Cuke] = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line.strip()):
                if c == '>':
                    self.map[Point(x, y)] = Cuke.EAST
                elif c == 'v':
                    self.map[Point(x, y)] = Cuke.SOUTH

    def EastFacingCukes(self) -> Iterable[Point]:
        for p in self.map:
            if self.map[p] == Cuke.EAST:
                yield p

    def SouthFacingCukes(self) -> Iterable[Point]:
        for p in self.map:
            if self.map[p] == Cuke.SOUTH:
                yield p

    def StepEast(self, p: Point) -> Point:
        return Point((p.x + 1) % self.width, p.y)

    def StepSouth(self, p: Point) -> Point:
        return Point(p.x, (p.y + 1) % self.height)

    def TakeStep(self) -> int:
        """Take a step and return the number of sea cucumbers that moved."""
        cukesToAdd: set[Point] = set()
        cukesToRemove: set[Point] = set()
        for cukePoint in self.EastFacingCukes():
            newLocation = self.StepEast(cukePoint)
            if newLocation not in self.map:
                cukesToRemove.add(cukePoint)
                cukesToAdd.add(newLocation)
        steps = len(cukesToRemove)
        for p in cukesToRemove:
            self.map.pop(p)
        for p in cukesToAdd:
            self.map[p] = Cuke.EAST
        cukesToRemove.clear()
        cukesToAdd.clear()
        for cukePoint in self.SouthFacingCukes():
            newLocation = self.StepSouth(cukePoint)
            if newLocation not in self.map:
                cukesToRemove.add(cukePoint)
                cukesToAdd.add(newLocation)
        steps += len(cukesToRemove)
        for p in cukesToRemove:
            self.map.pop(p)
        for p in cukesToAdd:
            self.map[p] = Cuke.SOUTH
        return steps

    def TextMap(self) -> list[str]:
        mapText: list[list[str]] = []
        for y in range(self.height):
            line: list[str] = []
            for x in range(self.width):
                line.append('.')
            mapText.append(line)
        for cukePoint in self.EastFacingCukes():
            mapText[cukePoint.y][cukePoint.x] = '>'
        for cukePoint in self.SouthFacingCukes():
            mapText[cukePoint.y][cukePoint.x] = 'v'
        return ["".join(line) for line in mapText]


def FirstStationaryStep(lines: list[str]) -> int:
    seaCucumbers = SeaCucumbers(lines)
    step = 1
    while seaCucumbers.TakeStep() > 0:
        step += 1
    return step


if __name__ == "__main__":
    """
    c = SeaCucumbers(TEST.splitlines())
    print("\n".join(c.TextMap()) + "\n")
    c.TakeStep()
    print("\n".join(c.TextMap()) + "\n")
    """
    part1 = FirstStationaryStep(TEST.splitlines())
    assert part1 == 58

    with open("25.txt", "r") as infile:
        part1 = FirstStationaryStep(infile.readlines())
    # 586 is too high. I forgot to strip newlines from the input.
    print(f"Part 1: {part1}")
