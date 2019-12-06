def powerLevelForCell(x, y, gridSerialNumber):
		rackID = x + 11
		powerLevel = rackID * (y + 1)
		powerLevel += gridSerialNumber
		powerLevel *= rackID
		powerLevel //= 100
		toSubtract = powerLevel // 10 * 10
		powerLevel -= toSubtract
		powerLevel -= 5
		return powerLevel
	
"""	
print(powerLevelForCell(2, 4, 8))
print(powerLevelForCell(121, 78, 57))
print(powerLevelForCell(216, 195, 39))
print(powerLevelForCell(100, 152, 71))

"""
gridSerialNumber = 42
grid = []
for y in range(300):
	row = []
	for x in range(300):
		row.append(powerLevelForCell(x, y, gridSerialNumber))
	grid.append(row)

largest = -1e12
for y in range(300):
	print(y)
	for x in range(300):
		squareValue = 0
		for squareSize in range(min(50, 300 - max(x, y))):
			squareValue += grid[y+squareSize][x+squareSize]
			column = x + squareSize
			for row in range(squareSize):
				squareValue += grid[y+row][column]
			row = y + squareSize
			for column in range(squareSize):
				squareValue += grid[row][x+column]
			if squareValue > largest:
				largest = squareValue
				largestCoordinate = (x+1, y+1, squareSize+1)
				
print(largestCoordinate)
