from collections import namedtuple
from typing import Tuple

TEST = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

Point = namedtuple('Point', ['x', 'y'])


def CreateDots(lines: list[str]) -> set[Point]:
    dots = set()
    for line in lines:
        x, y = (int(c) for c in line.split(","))
        dots.add(Point(x, y))
    return dots


def PerformFold(instruction: str, dots: set[Point]) -> set[Point]:
    newDots: set[Point] = set()
    axis, value = instruction.split()[2].split('=')
    value = int(value)
    if axis == "x":
        for dot in dots:
            if dot.x == value:
                raise ValueError(
                    f"X can't be on a fold line. Dot: {dot}, line at {value}.")
            if dot.x < value:
                newDots.add(dot)
            else:
                newX = value * 2 - dot.x
                newDots.add(Point(newX, dot.y))
    else:
        for dot in dots:
            if dot.y == value:
                raise ValueError(
                    f"Y can't be on a fold line. Dot: {dot}, line at {value}.")
            if dot.y < value:
                newDots.add(dot)
            else:
                newY = value * 2 - dot.y
                newDots.add(Point(dot.x, newY))

    return newDots


def PerformFolds(coordinates: str, instructions: str) -> Tuple[set[Point], int]:
    dots = CreateDots(coordinates.split())
    dotsAfterOneFold = -1
    for instruction in instructions.split("\n"):
        dots = PerformFold(instruction, dots)
        if dotsAfterOneFold < 0:
            dotsAfterOneFold = len(dots)
    return dots, dotsAfterOneFold


def FinalPaper(dots: set[Point]) -> str:
    maxX = max(d.x for d in dots)
    maxY = max(d.y for d in dots)
    paper: list[list[str]] = []
    for _ in range(maxY + 1):
        paper.append([" "] * (maxX + 1))

    for dot in dots:
        paper[dot.y][dot.x] = "X"

    lines: list[str] = []
    for y in range(len(paper)):
        lines.append("".join(paper[y]))
    return "\n".join(lines)


if __name__ == "__main__":
    coordinates, instructions = TEST.split("\n\n")
    dots, part1 = PerformFolds(coordinates, instructions)
    assert part1 == 17
    print(FinalPaper(dots))

    with open("13.txt", "r") as infile:
        coordinates, instructions = infile.read().split("\n\n")
    dots, part1 = PerformFolds(coordinates, instructions)
    print(f"Part 1: {part1}")
    print(FinalPaper(dots))
