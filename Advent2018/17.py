import numpy as np
import re

from collections import namedtuple, deque
from typing import List

compiledScanLine = re.compile(r"(.)=(\d+), (.)=(\d+)\.\.(\d+)")

Coordinate = namedtuple('Coordinate', ['x', 'y'])
Extent = namedtuple('Extent', ['clay', 'dropoff'])


def readGrid(fileName):
    # Get extents
    minX = 1e12
    maxX = -1e12
    minY = 1e12
    maxY = -1e12
    #
    with open(fileName, "r") as infile:
        for line in infile:
            match = compiledScanLine.match(line)
            if not match:
                continue
            if int(match[4]) > int(match[5]):
                raise ValueError(
                    "Wasn't expecting first range value to be greater than second"
                )
            if match[1] == "x":
                minX = min(minX, int(match[2]))
                maxX = max(maxX, int(match[2]))
                minY = min(minY, int(match[4]))
                maxY = max(maxY, int(match[5]))
            else:
                minY = min(minY, int(match[2]))
                maxY = max(maxY, int(match[2]))
                minX = min(minX, int(match[4]))
                maxX = max(maxX, int(match[5]))

    minX -= 1
    maxX += 1
    print(minX, maxX, minY, maxY)
    grid = np.full((maxY - minY + 1, maxX - minX + 1), ".", dtype=str)

    with open(fileName, "r") as infile:
        for line in infile:
            match = compiledScanLine.match(line)
            if not match:
                continue
            firstCoord = int(match[2])
            lowRange = int(match[4])
            highRange = int(
                match[5]
            ) + 1  # Increment because end of range is inclusive in puzzle data
            if match[1] == "x":
                grid[lowRange - minY:highRange - minY, firstCoord - minX] = "#"
            else:
                grid[firstCoord - minY, lowRange - minX:highRange - minX] = "#"

    return grid, minX, minY


def findExtent(grid: np.ndarray, coordinate: Coordinate,
               toLeft: bool) -> Extent:
    """
    Find the first clay or dropoff to the left or right of the given coordinate
    """
    if toLeft:

        def onGrid(x):
            return x - 1 > 0

        def nextX(x):
            return x - 1
    else:

        def onGrid(x):
            return x + 1 < grid.shape[1]

        def nextX(x):
            return x + 1

    extent: Extent = None
    x = coordinate.x
    while not extent and onGrid(x):
        x = nextX(x)
        if grid[coordinate.y, x] == "#":
            extent = Extent(abs(x - coordinate.x), 0)
        elif grid[coordinate.y + 1, x] in ".|":
            extent = Extent(0, abs(x - coordinate.x))

    return extent


def findExtents(grid: np.ndarray, coordinate: Coordinate) -> (Extent, Extent):
    """
    Find the first clay or dropoff location to the left and right of the given coordinate
    """
    leftExtent = findExtent(grid, coordinate, toLeft=True)
    rightExtent = findExtent(grid, coordinate, toLeft=False)
    return (leftExtent, rightExtent)


def printGrid(grid):
    for row in grid:
        for cell in row:
            print(cell, end='')
        print()
    print()


def coordinateIsConnected(grid: np.ndarray,
                          leftCoord: Coordinate,
                          rightCoord: Coordinate) -> bool:
    y = leftCoord.y + 1
    # Move left to the first clay
    leftX = leftCoord.x
    while leftX - 1 >= 0 and grid[y, leftX - 1] == ".":
        leftX -= 1
    if leftX == 0:
        # We hit the side of the puzzle so we can't be in a bucket
        return False
    # Move right to the first clay
    rightX = rightCoord.x
    width = len(grid[0])
    while rightX + 1 < width and grid[y, rightX + 1] == ".":
        rightX += 1
    if rightX + 1 == width:
        # We hit the side of the puzzle so we can't be in a bucket
        return False
    # Move down the the first clay
    while y + 1 < len(grid) and grid[y + 1, rightX] == ".":
        y += 1
    if y + 1 == len(grid):
        # We hit the bottom of the puzzle so we can't be in a bucket
        return False
    # Move left to the first clay
    while rightX - 1 >= 0 and grid[y, rightX - 1] == ".":
        rightX -= 1
    # If leftX and rightX are the same it means we're in a bucket
    return leftX == rightX


def addCoordinateToStack(grid: np.ndarray,
                         startCoordinate: Coordinate,
                         flowStack: List) -> None:
    y = startCoordinate.y
    while y < len(grid) and grid[y, startCoordinate.x] in ".|":
        flowStack.append(Coordinate(startCoordinate.x, y))
        y = y + 1


def exploreGrid(grid: np.ndarray, startCoordinate: Coordinate,
                stopShort=False):
    toExplore: deque = deque([startCoordinate])

    explored = 0

    while len(toExplore) and (not stopShort or explored < 200):
        explored += 1
        exploreCoordinate: Coordinate = toExplore.popleft()
        flowStack = []
        addCoordinateToStack(grid, exploreCoordinate, flowStack)

        while flowStack:
            flowCoord: Coordinate = flowStack.pop()
            if grid[flowCoord.y, flowCoord.x] == "~":
                # This cell has already been filled with water so skip it
                continue
            if flowCoord.y + 1 >= len(grid) or grid[flowCoord.y + 1, flowCoord.x] == "|":
                # If we're at the bottom of the grid or the cell below this is flowing water,
                # This cell can't spread to the left and right
                grid[flowCoord.y, flowCoord.x] = "|"
                continue
            leftExtents, rightExtents = findExtents(grid, flowCoord)
            if leftExtents.clay and rightExtents.clay:
                # This is bounded by clay on both sides, so fill between the clay cells
                grid[flowCoord.y, flowCoord.x - leftExtents.clay + 1:
                     flowCoord.x + rightExtents.clay] = "~"
                continue
            leftDropoffCell = grid[flowCoord.y + 1, flowCoord.x - leftExtents.dropoff] \
                if leftExtents.dropoff else None
            rightDropoffCell = grid[flowCoord.y + 1, flowCoord.x + rightExtents.dropoff] \
                if rightExtents.dropoff else None
            if leftDropoffCell == "." or rightDropoffCell == ".":
                # There's an empty cell at one or both dropoff points so process this cell again after
                # filling below
                flowStack.append(flowCoord)
                if leftDropoffCell == ".":
                    addCoordinateToStack(grid,
                                         Coordinate(flowCoord.x - leftExtents.dropoff, flowCoord.y + 1), flowStack)
                if rightDropoffCell == ".":
                    addCoordinateToStack(grid,
                                         Coordinate(flowCoord.x + rightExtents.dropoff,
                                                    flowCoord.y + 1), flowStack)
                continue
            # The cell isn't bound by clay and we've already filled the dropoffs
            else:
                # Keep track of where flowing water x coordinate starts and stops
                flowXStart = flowCoord.x
                flowXStop = flowCoord.x
                # This drops off on one or both sides. We need to fill with flowing water and add the dropoff
                # cells to the list of coordinates to explore
                if leftExtents.clay:
                    # Fill with flowing water from the clay to here
                    flowXStart = flowCoord.x - leftExtents.clay + 1
                else:
                    # Drops off to the left.
                    flowXStart = flowCoord.x - leftExtents.dropoff
                if rightExtents.clay:
                    # Fill with flowing water from here to clay
                    flowXStop = flowCoord.x + rightExtents.clay
                else:
                    # Drops off to the right.
                    flowXStop = flowCoord.x + rightExtents.dropoff + 1
                grid[flowCoord.y, flowXStart:flowXStop] = "|"
            #printGrid(grid)


if __name__ == "__main__":
    grid, minX, minY = readGrid("17.txt")
    exploreGrid(grid, Coordinate(500 - minX, 0))
    printGrid(grid)
    stillWaterCount = 0
    flowingWaterCount = 0
    for row in grid:
        for cell in row:
            if cell in "~":
                stillWaterCount += 1
            if cell in "|":
                flowingWaterCount += 1
    print(f"{stillWaterCount} still water tiles")
    print(f"{flowingWaterCount} flowing water tiles")
    print(f"{stillWaterCount + flowingWaterCount} total water tiles")
