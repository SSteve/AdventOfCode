import re
from collections import namedtuple
from typing import Callable, List

import numpy as np

from generic_search import astar, costList, nodeToPath


Point = namedtuple('Point', ['x', 'y', 'tool'])

NEITHER = 0
TORCH = 1
CLIMBING = 2

ROCKY = 0
WET = 1
NARROW = 2


class CaveState(Point):
    def __repr__(self):
        return f"CaveState({self.x}, {self.y}, {self.tool})"

    def __str__(self):
        return f"({self.x}, {self.y}, {self.tool})"

    def __add__(self, other):
        return CaveState(self.x + other[0], self.y + other[1], self.tool)

    def __mul__(self, other):
        return CaveState(self.x * other, self.y * other, self.tool)

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1] and self.tool == other[2]

    def __lt__(self, other):
        return self.y < other[1] or \
            self.y == other[1] and self.x < other[0] or \
            self.y == other[1] and self.x == other[0] and self.tool < other[2]

    def __hash__(self):
        return hash((self.x, self.y))


class Cave:
    def __init__(self, depth, targetX, targetY, overshootX, overshootY):
        self.depth = depth
        self.targetX = targetX
        self.targetY = targetY
        self.erosionLevels = np.full((targetY + overshootY, targetX + overshootX + 1), 0, dtype=int)
        self.regionTypes = np.full((targetY + overshootY, targetX + overshootX + 1), 0, dtype=int)
        self.createToolMap()

    def calculateErosionLevels(self):
        for y in range(self.erosionLevels.shape[0]):
            for x in range(self.erosionLevels.shape[1]):
                if (x, y) == (0, 0) or (x, y) == (self.targetX, self.targetY):
                    geologicIndex = 0
                elif y == 0:
                    geologicIndex = x * 16807
                elif x == 0:
                    geologicIndex = y * 48271
                else:
                    geologicIndex = self.erosionLevels[y, x - 1] * self.erosionLevels[y - 1, x]
                erosionLevel = (geologicIndex + self.depth) % 20183
                self.erosionLevels[y, x] = erosionLevel
                self.regionTypes[y, x] = erosionLevel % 3

    def calculateRiskLevel(self):
        riskLevel = 0
        for y in range(self.targetY + 1):
            for x in range(self.targetX + 1):
                riskLevel += self.regionTypes[y, x]
        return riskLevel

    def printCave(self):
        for y in range(self.regionTypes.shape[0]):
            for x in range(self.regionTypes.shape[1]):
                if (x, y) == (0, 0):
                    print("M", end='')
                elif (x, y) == (self.targetX, self.targetY):
                    print("T", end='')
                else:
                    print(".=|"[self.regionTypes[y, x]], end='')
            print()

    def caveStateType(self, caveState: CaveState) -> int:
        return self.regionTypes[caveState.y, caveState.x]

    def createToolMap(self):
        self.toolMap = {
            (ROCKY, TORCH, ROCKY): TORCH,
            (ROCKY, TORCH, WET): CLIMBING,
            (ROCKY, TORCH, NARROW): TORCH,
            (ROCKY, CLIMBING, ROCKY): CLIMBING,
            (ROCKY, CLIMBING, WET): CLIMBING,
            (ROCKY, CLIMBING, NARROW): TORCH,
            (WET, NEITHER, ROCKY): CLIMBING,
            (WET, NEITHER, WET): NEITHER,
            (WET, NEITHER, NARROW): NEITHER,
            (WET, CLIMBING, ROCKY): CLIMBING,
            (WET, CLIMBING, WET): CLIMBING,
            (WET, CLIMBING, NARROW): NEITHER,
            (NARROW, NEITHER, ROCKY): TORCH,
            (NARROW, NEITHER, WET): NEITHER,
            (NARROW, NEITHER, NARROW): NEITHER,
            (NARROW, TORCH, ROCKY): TORCH,
            (NARROW, TORCH, WET): NEITHER,
            (NARROW, TORCH, NARROW): TORCH,
        }

    def newTool(self, caveState, newX, newY) -> int:
        return self.toolMap[(self.caveStateType(caveState),
                             caveState.tool,
                             self.regionTypes[newY, newX])]

    def canReachRegion(self, caveState, newX, newY) -> bool:
        """
        if newX >= self.regionTypes.shape[1]:
            raise ValueError("Reached the right edge of the cave.")
        if newY >= self.regionTypes.shape[0]:
            raise ValueError("Reached the bottom edge of the cave.")
        return newX >= 0 and newY >= 0
        """
        return newX >= 0 and newY >= 0 and newY < self.regionTypes.shape[0] and newX < self.regionTypes.shape[1]

    def newCaveState(self, caveState, deltaX, deltaY):
        newX = caveState.x + deltaX
        newY = caveState.y + deltaY
        if newX == self.targetX and newY == self.targetY:
            newTool = TORCH
        else:
            newTool = self.newTool(caveState, newX, newY)
        return CaveState(newX, newY, newTool)

    def successors(self, caveState: CaveState) -> List[CaveState]:
        destinations: List[CaveState] = []
        # Left
        if self.canReachRegion(caveState, caveState.x - 1, caveState.y):
            destinations.append(self.newCaveState(caveState, -1, 0))
        # Up
        if self.canReachRegion(caveState, caveState.x, caveState.y - 1):
            destinations.append(self.newCaveState(caveState, 0, -1))
        # Right
        if self.canReachRegion(caveState, caveState.x + 1, caveState.y):
            destinations.append(self.newCaveState(caveState, 1, 0))
        # Down
        if self.canReachRegion(caveState, caveState.x, caveState.y + 1):
            destinations.append(self.newCaveState(caveState, 0, 1))
        return destinations

    def reachedTarget(self, caveState: CaveState) -> bool:
        return self.targetX == caveState.x and self.targetY == caveState.y


def manhattanDistance(x: int, y: int) -> Callable[[CaveState], float]:
    def distance(caveState: CaveState) -> float:
        xdist: int = abs(caveState.x - x)
        ydist: int = abs(caveState.y - y)
        return xdist + ydist
    return distance


def costBetweenStates(state1: CaveState, state2: CaveState) -> float:
    cost = 1
    if state1.tool != state2.tool:
        cost += 7
    return cost


if __name__ == "__main__":
    part1 = False
    with open("22.txt", "r") as infile:
        match = re.match(r"depth: (\d+)", infile.readline())
        if match:
            depth = int(match[1])
        match = re.match(r"target: (\d+),(\d+)", infile.readline())
        if match:
            x = int(match[1])
            y = int(match[2])

    cave = Cave(depth, x, y, 45, 55)
    cave.calculateErosionLevels()
    if part1:
        cave.printCave()
        print(f"Risk level: {cave.calculateRiskLevel()}")
    else:
        startingState = CaveState(0, 0, TORCH)
        # cave.printCave()
        solution = astar(startingState, cave.reachedTarget, cave.successors, manhattanDistance(x, y), costBetweenStates)
        if solution:
            print(f"Fastest route to target: {solution.cost} minutes.")
            # path = nodeToPath(solution)
            # print(path)
            # print(costList(solution))
        else:
            print("No solution found")
