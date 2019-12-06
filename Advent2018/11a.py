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
gridSerialNumber = 8141
grid = []
for y in range(300):
	row = []
	for x in range(300):
		row.append(powerLevelForCell(x, y, gridSerialNumber))
	grid.append(row)

largest = -1e12
for y in range(297):
	for x in range(297):
		cellValue = grid[y][x] + grid[y+1][x] + grid[y+2][x] \
				+ grid[y][x+1] + grid[y+1][x+1] + grid[y+2][x+1] \
				+ grid[y][x+2] + grid[y+1][x+2] + grid[y+2][x+2]
		if cellValue > largest:
			largest = cellValue
			largestCoordinate = (x+1, y+1)
				
print(largestCoordinate)
