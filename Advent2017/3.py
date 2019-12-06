import pdb

xDelta = [1, 0, -1, 0]
yDelta = [0, -1, 0, 1]

def move(x, y, direction):
	return x + xDelta[direction], y + yDelta[direction]
	
def outOfBounds(x, y, direction, bounds):
	oob = False
	if direction == 0 and x > bounds[0]:
		bounds[0] += 1
		oob = True
	elif direction == 1 and y < bounds[1]:
		bounds[1] -= 1
		oob = True
	elif direction == 2 and x < bounds[2]:
		bounds[2] -= 1
		oob = True
	elif direction == 3 and y > bounds[3]:
		bounds[3] += 1
		oob = True
	return oob
		
def sumForSquare(x, y, values):
	#pdb.set_trace()
	squareValue = 0
	for xtest in range(x - 1, x + 2):
		for ytest in range(y - 1, y + 2):
			if (xtest, ytest) in values:
				squareValue += values[(xtest, ytest)]
	return squareValue

def a3(value):
	x = 0
	y = 0
	bounds = [0, 0, 0, 0] # minx, miny, maxx, maxy
	values = {(0, 0): 1}
	direction = 0 # Moving right
	while values[x, y] <= value:
		x, y = move(x, y, direction)
		values[(x, y)] = sumForSquare(x, y, values)
		if outOfBounds(x, y, direction, bounds):
			direction = (direction + 1) % 4
	return values[(x, y)]

if __name__ == "__main__":
	print(a3(312051))
	#print(20, a3(20))
	#print(2, a3(2))
