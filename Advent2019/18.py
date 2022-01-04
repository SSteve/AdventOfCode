from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, Optional, Tuple

import heapq
import math

"""
This solution cribbed from https://github.com/mebeim/aoc/blob/master/2019/README.md#day-18---many-worlds-interpretation
"""

GRAPH: dict[str, list[Tuple[str, int]]] = {}


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def offset(self, deltaX: int, deltaY: int) -> Point:
        return Point(self.x + deltaX, self.y + deltaY)


def BuildGraph(map: list[str]) -> Tuple[dict[str, list[Tuple[str, int]]], Optional[Point]]:
    graph: dict[str, list[Tuple[str, int]]] = {}
    startPosition: Optional[Point] = None

    for y, line in enumerate(map):
        for x, cell in enumerate(line):
            if cell not in '#.':
                graph[cell] = FindAdjacent(map, Point(x, y))

                if cell == "@":
                    startPosition = Point(x, y)

    return graph, startPosition


def Neighbors(map: list[str], p: Point) -> Iterable[Point]:
    for deltaX, deltaY in ((-1, 0), (1, 0), (0, 1), (0, -1)):
        newX, newY = p.x + deltaX, p.y + deltaY

        if 0 <= newX < len(map[0]) and 0 <= newY < len(map) and \
                map[newY][newX] != '#':
            yield Point(newX, newY)


def FindAdjacent(map: list[str], p: Point) -> list[Tuple[str, int]]:
    queue: deque[Tuple[int, Point]] = deque()
    visited: set[Point] = {p}
    found: list[Tuple[str, int]] = []

    for n in Neighbors(map, p):
        queue.append((1, n))

    while queue:
        dist, node = queue.popleft()

        if node not in visited:
            visited.add(node)

            cell = map[node.y][node.x]

            # Check if this cell is a key or door and wasn't already found.
            if ('a' <= cell <= 'z' or 'A' <= cell <= 'Z') and \
                    cell not in found:
                found.append((cell, dist))
                continue

            # Otherwise add all unvisited neighbors to the queue.
            for neighbor in filter(lambda n: n not in visited, Neighbors(map, node)):
                queue.append((dist + 1, neighbor))

    return found


@lru_cache(2**20)
def Explore(cells: str, numKeysToFind: int, foundKeys: frozenset[str] = frozenset()) -> float:
    if numKeysToFind == 0:
        return 0

    best = math.inf

    for cell in cells:
        for nextKey, distance in ReachableKeys(cell, foundKeys):
            newKeys = foundKeys | {nextKey}
            newSources = cells.replace(cell, nextKey)

            distance += Explore(newSources, numKeysToFind - 1, newKeys)

            if distance < best:
                best = distance

    return best


@lru_cache(2**20)
def DistanceForKeys(keys: frozenset[str]) -> dict[str, float]:
    return defaultdict(lambda: math.inf)


@lru_cache(2**20)
def ReachableKeys(cell: str, foundKeys: frozenset[str]) -> list[Tuple[str, int]]:
    queue: list[Tuple[int, str]] = []
    distance = DistanceForKeys(foundKeys)
    reachable: list[Tuple[str, int]] = []

    for neighbor, weight in GRAPH[cell]:
        queue.append((weight, neighbor))

    heapq.heapify(queue)

    while queue:
        dist, cell = heapq.heappop(queue)

        # Is this a key we don't already have?
        if cell.islower() and cell not in foundKeys:
            reachable.append((cell, dist))
            continue

        if cell.lower() not in foundKeys:
            # This is a door we don't have a key for. Don't explore neighbors.
            continue

        for neighbor, weight in GRAPH[cell]:
            newDistance = dist + weight

            # If the distance to reach it is better than we already have,
            # add it to the queue.
            if newDistance < distance[neighbor]:
                distance[neighbor] = newDistance
                heapq.heappush(queue, (newDistance, neighbor))

    return reachable


def FindMinimumSteps(map: list[str]) -> int:
    Explore.cache_clear()
    DistanceForKeys.cache_clear()
    ReachableKeys.cache_clear()
    global GRAPH
    GRAPH, _ = BuildGraph(map)
    totalKeys = sum(int(node.islower()) for node in GRAPH)
    minSteps = Explore('@', totalKeys)
    return int(minSteps)


def Part2(map: list[str]) -> int:
    def ReplaceChar(s: str, pos: int, newChar: str) -> str:
        return s[:pos] + newChar + s[pos+1:]

    Explore.cache_clear()
    DistanceForKeys.cache_clear()
    ReachableKeys.cache_clear()
    _, startPosition = BuildGraph(map)

    if startPosition is None:
        raise ValueError("Start position can't be None.")

    # Convert cells around entrance to walls.
    for p in Neighbors(map, startPosition):
        map[p.y] = ReplaceChar(map[p.y], p.x, '#')

    map[startPosition.y] = ReplaceChar(
        map[startPosition.y], startPosition.x, '#')

    for c, p in enumerate((Point(-1, -1), Point(1, -1), Point(1, 1), Point(-1, 1))):
        newPosition = startPosition + p
        map[newPosition.y] = ReplaceChar(
            map[newPosition.y], newPosition.x, str(c + 1))

    # Rebuild the graph with the new info.
    global GRAPH
    GRAPH, _ = BuildGraph(map)

    totalKeys = sum(int(node.islower()) for node in GRAPH)
    minSteps = Explore('1234', totalKeys)
    return int(minSteps)


TEST1 = """#########
#b.A.@.a#
#########"""

TEST2 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

TEST3 = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""

TEST4 = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

TEST5 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

TEST6 = """###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############"""

TEST7 = """#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############"""

TEST8 = """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""

if __name__ == "__main__":
    part1 = FindMinimumSteps(TEST1.splitlines())
    assert part1 == 8

    part1 = FindMinimumSteps(TEST2.splitlines())
    assert part1 == 86

    part1 = FindMinimumSteps(TEST3.splitlines())
    assert part1 == 132

    part1 = FindMinimumSteps(TEST4.splitlines())
    assert part1 == 136

    part1 = FindMinimumSteps(TEST5.splitlines())
    assert part1 == 81

    with open("18.txt", "r") as infile:
        part1 = FindMinimumSteps(infile.read().splitlines())
    print(f"Part 1: {part1}")

    part2 = Part2(TEST6.splitlines())
    assert part2 == 24

    part2 = Part2(TEST7.splitlines())
    assert part2 == 32

    part2 = Part2(TEST8.splitlines())
    assert part2 == 72

    with open("18.txt", "r") as infile:
        part2 = Part2(infile.read().splitlines())
    print(f"Part 2: {part2}")
