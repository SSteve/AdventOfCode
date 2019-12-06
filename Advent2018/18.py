import numpy as np
import hashlib

OPEN_CELL = "."
TREES_CELL = "|"
LUMBER_CELL = "#"


def readGrid(fileName, sideLength):
    grid = np.full((sideLength, sideLength), " ", dtype=str)

    with open(fileName, "r") as infile:
        for rowNumber, line in enumerate(infile):
            for columnNumber, cell in enumerate(line.strip()):
                grid[rowNumber, columnNumber] = cell

    return grid


def printGrid(grid):
    for row in grid:
        for cell in row:
            print(cell, end='')
        print()
    print()


def countNeighbors(grid, x, y):
    cells = ""
    if y > 0:
        # Count the row above
        if x > 0:
            cells += grid[y - 1, x - 1]
        cells += grid[y - 1, x]
        if x + 1 < grid.shape[1]:
            cells += grid[y - 1, x + 1]
    # Count the cell to the left
    if x > 0:
        cells += grid[y, x - 1]
    if x + 1 < grid.shape[1]:
        cells += grid[y, x + 1]
    if y + 1 < grid.shape[0]:
        # Count the row below
        if x > 0:
            cells += grid[y + 1, x - 1]
        cells += grid[y + 1, x]
        if x + 1 < grid.shape[1]:
            cells += grid[y + 1, x + 1]
    openCount = cells.count(OPEN_CELL)
    treesCount = cells.count(TREES_CELL)
    lumberCount = cells.count(LUMBER_CELL)
    return openCount, treesCount, lumberCount


def nextGeneration(currentGeneration, openCount, treesCount, lumberCount):
    nextGenerationCell = None
    if currentGeneration == OPEN_CELL and treesCount >= 3:
        nextGenerationCell = TREES_CELL
    elif currentGeneration == TREES_CELL and lumberCount >= 3:
        nextGenerationCell = LUMBER_CELL
    elif currentGeneration == LUMBER_CELL:
        if not (lumberCount >= 1 and treesCount >= 1):
            nextGenerationCell = OPEN_CELL

    return nextGenerationCell


def minute(grid):
    newGrid = np.full(grid.shape, " ", dtype=str)
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            # openCount, treesCount, lumberCount = countNeighbors(grid, x, y)
            cell = grid[y, x]
            openCount, treesCount, lumberCount = countNeighbors(grid, x, y)
            next = nextGeneration(cell, openCount, treesCount, lumberCount)
            newGrid[y, x] = next if next is not None else cell

    return newGrid


def checkSum(grid):
    fullString = ''.join([y for y in [''.join(x) for x in grid]])
    hashed = hashlib.sha256(fullString.encode()).hexdigest()
    return hashed


def countGrid(grid):
    counts = {OPEN_CELL: 0, TREES_CELL: 0, LUMBER_CELL: 0}
    for row in grid:
        for cell in row:
            counts[cell] += 1
    return counts[OPEN_CELL], counts[TREES_CELL], counts[LUMBER_CELL]


if __name__ == "__main__":
    checkSums = {}
    grids = {}
    checkSumValues = checkSums.values()
    # grid = readGrid("18test1.txt", 10)
    grid = readGrid("18.txt", 50)
    checkSums[0] = checkSum(grid)
    grids[0] = grid
    for i in range(1000000000):
        newGrid = minute(grid)
        newCheckSum = checkSum(newGrid)
        if newCheckSum in checkSumValues:
            for item in checkSums.items():
                if newCheckSum == item[1]:
                    indexMatch = item[0]
            print(f"Found same checksum at {indexMatch} and {i + 1}")
            theIndex = ((1000000000 - indexMatch) % ((i + 1) - indexMatch)) + indexMatch
            print(f"Minute 1,000,000,000 at {theIndex}.")
            openCount, treesCount, lumberCount = countGrid(grids[theIndex])
            print(f"Resource value: {treesCount * lumberCount}")
            break
        else:
            checkSums[i + 1] = newCheckSum
            grids[i + 1] = newGrid
            grid = newGrid
    startIndex = indexMatch - 5 * (i + 1 - indexMatch)
    for printIndex in range(startIndex, i + 1):
        print(f"{printIndex}:")
        printGrid(grids[printIndex])
    # openCount, treesCount, lumberCount = countGrid(grid)
    # print(f"Open: {openCount}, Trees: {treesCount}, Lumber: {lumberCount}")
    # print(f"Resource value: {treesCount * lumberCount}")
