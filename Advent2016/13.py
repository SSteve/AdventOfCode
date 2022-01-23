from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, Optional

from generic_search import bfs, nodeToPath, Node


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@lru_cache(maxsize=None)
def IsOpen(p: Point) -> bool:
    if p.x < 0 or p.y < 0:
        return False
    value = p.x*p.x + 3*p.x + 2*p.x*p.y + p.y + p.y*p.y + 1358
    bitCount = 0
    while value != 0:
        bitCount += value & 1
        value //= 2
    isEven = (bitCount & 1) == 0
    return isEven


def Successors(p: Point) -> Iterable[Point]:
    for deltaX, deltaY in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        neighbor = Point(p.x + deltaX, p.y + deltaY)
        if IsOpen(neighbor):
            yield neighbor


def IsFinished(p: Point) -> bool:
    global destinationX
    global destinationY
    return p.x == destinationX and p.y == destinationY


def GetSolution(x: int, y: int) -> Optional[Node[Point]]:
    global destinationX
    global destinationY
    if IsOpen(Point(x, y)):
        destinationX = x
        destinationY = y
        solution = bfs(Point(1, 1), IsFinished, Successors)
        if solution:
            path = nodeToPath(solution)
            if len(path) - 1 <= 50:
                return solution
    return None


if __name__ == '__main__':
    global destinationX
    global destinationY
    destinationX = 31
    destinationY = 39
    solution = bfs(Point(1, 1), IsFinished, Successors)
    if not solution:
        print("No solution found.")
    else:
        part1 = len(nodeToPath(solution)) - 1
        print(f"Part 1: {part1}")

    reachedPoint: set[Point] = set()
    for x in range(-1, 51):
        for y in range(-1, 51):
            if x + y > 50:
                continue
            solution = GetSolution(x+1, y+1)
            if solution:
                path = nodeToPath(solution)
                for node in path:
                    reachedPoint.add(node)

    part2 = len(reachedPoint)
    print(f"Part 2: {part2}")
