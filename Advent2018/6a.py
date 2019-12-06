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
row = [-1] * (maxX - minX + 1)
for i in range(maxY - minY + 1):
    closest.append(row.copy())

# Build 2d array of closest coordinate for each square on the grid
for x in range(minX, maxX + 1):
    for y in range(minY, maxY + 1):
        distances = []
        for coordinate in coordinates:
            distances.append(distance(coordinate, x, y))
        if distances.count(min(distances)) == 1:
            closest[y - minY][x - minX] = distances.index(min(distances))

"""
for yIndex in range(maxY - minY + 1):
    for xIndex in range(maxX - minX + 1):
        if closest[yIndex][xIndex] == -1:
            print('.', end='')
        else:
            print(chr(ord('a') + closest[yIndex][xIndex]), end='')
    print()
"""

# Count the number of closest squares for each coordinate
closestCounts = {}
for coordinateNumber in range(len(coordinates)):
    thisCount = 0
    for yIndex in range(maxY - minY + 1):
        thisCount += closest[yIndex].count(coordinateNumber)
    closestCounts[coordinateNumber] = thisCount

# Collect all the coordinates on the edge of the grid because they are infinite
edgeCoordinates = set()
for coord in closest[0]:
    edgeCoordinates.add(coord)
for coord in closest[-1]:
    edgeCoordinates.add(coord)
for row in closest[1:-1]:
    edgeCoordinates.add(row[0])
    edgeCoordinates.add(row[-1])

# Remove the edge coordinates from closestCounts
for edgeCoordinate in edgeCoordinates:
    try:
        closestCounts.pop(edgeCoordinate)
    except KeyError:
        # If it's already gone, don't throw an exception
        pass

print(max(closestCounts.values()))
