import re
import sys


def distance(coordinate, x, y):
    return abs(coordinate[0] - x) + abs(coordinate[1] - y)


compiled = re.compile(r"(\d+), (\d+)")

coordinates = []
minX = sys.maxsize
maxX = -sys.maxsize
minY = sys.maxsize
maxY = -sys.maxsize

with open("6.txt", "r") as infile:
    for line in infile:
        result = compiled.match(line)
        if result:
            x = int(result[1])
            y = int(result[2])
            coordinates.append((x, y))
            minX = min(minX, x)
            maxX = max(maxX, x)
            minY = min(minY, y)
            maxY = max(maxY, y)

# Expand field by 1 on each side
minX -= 1
maxX += 1
minY -= 1
maxY += 1

# Build the grid
closest = []
row = [0] * (maxX - minX + 1)
for i in range(maxY - minY + 1):
    closest.append(row.copy())

# Build 2d array of closest coordinate for each square on the grid
closeSquares = 0
for x in range(minX, maxX + 1):
    for y in range(minY, maxY + 1):
        distances = []
        for coordinate in coordinates:
            distances.append(distance(coordinate, x, y))
        closest[y - minY][x - minX] = sum(distances)
        if closest[y - minY][x - minX] < 10_000:
        	closeSquares += 1

"""
for yIndex in range(maxY - minY + 1):
    for xIndex in range(maxX - minX + 1):
        if closest[yIndex][xIndex] < 32:
            print('#', end='')
        else:
            print('.', end='')
    print()
"""


print(closeSquares)
