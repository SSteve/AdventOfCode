import numpy as np


def isCorner(x, y, size):
    return x == 0 and y == 0 \
        or x + 1 == size and y == 0 \
        or x == 0 and y + 1 == size \
        or x + 1 == size and y + 1 == size


def rowNeighbors(x, row, cornersOn, y):
    if cornersOn and isCorner(x - 1, y, len(row)):
        yield True
    elif x > 0:
        yield row[x - 1]
    if cornersOn and isCorner(x, y, len(row)):
        yield True
    else:
        yield row[x]
    if cornersOn and isCorner(x + 1, y, len(row)):
        yield True
    elif x + 1 < len(row):
        yield row[x+1]


def neighbors(x, y, lights, cornersOn=False):
    if y > 0:
        for val in rowNeighbors(x, lights[y - 1], cornersOn, y - 1):
            yield val

    if cornersOn and isCorner(x - 1, y, len(lights)):
        yield True
    elif x > 0:
        yield lights[y, x-1]
    if cornersOn and isCorner(x + 1, y, len(lights)):
        yield True
    elif x + 1 < len(lights[y]):
        yield lights[y, x + 1]

    if y + 1 < len(lights):
        for val in rowNeighbors(x, lights[y + 1], cornersOn, y + 1):
            yield val


def printLights(lights):
    for row in lights:
        for char in row:
            print("#" if char else ".", end='')
        print()
    print()

def day18(fileName, size, steps, cornersOn=False, shouldPrint=False):
    lights = np.zeros([size, size], dtype = bool)
    with open(fileName) as infile:
        for rowNumber, line in enumerate(infile):
            for columnNumber, char in enumerate(line.strip()):
                lights[rowNumber, columnNumber] = char == "#"
    for i in range(steps):
        if i % 10 == 0:
            print(i)
        newLights = np.zeros([size, size], dtype = bool)
        for y in range(size):
            for x in range(size):
                if cornersOn and isCorner(x, y, size):
                    newLights[y, x] = True
                else:
                    neighborCount = sum(neighbors(x, y, lights, cornersOn))
                    if lights[y, x]:
                        newLights[y, x] = neighborCount == 2 or neighborCount == 3
                    else:
                        newLights[y, x] = neighborCount == 3
        lights = newLights
        if shouldPrint:
            printLights(lights)

    return sum(sum(row) for row in lights)


# print(day18("18test.txt", 6, 4), "lights are on")
# print(day18("18.txt", 100, 100), "lights are on")
print(day18("18test.txt", 6, 5, True, True), "lights are on")
print(day18("18.txt", 100, 100, True), "lights are on")
