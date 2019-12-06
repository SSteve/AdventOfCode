from enum import Enum


class Direction(Enum):
	LEFT = 1
	UP = 2
	RIGHT = 3
	DOWN = 4


class Packet:
	xOffsets = {
		Direction.LEFT: -1,
		Direction.UP: 0,
		Direction.RIGHT: 1,
		Direction.DOWN: 0
	}
	yOffsets = {
		Direction.LEFT: 0,
		Direction.UP: -1,
		Direction.RIGHT: 0,
		Direction.DOWN: 1
	}

	def __init__(self, map):
		self.map = map
		self.path = ""

	def start(self):
		self.direction = Direction.DOWN
		self.stepCount = 0
		self.y = 0
		self.x = self.map[0].index("|")
		while self.move():
			pass
		return self.path, self.stepCount

	def nextChar(self, direction):
		"""
        Return the next character in the given direction. Return
        None if we'd fall off the map
        """
		testX = self.x + Packet.xOffsets[direction]
		testY = self.y + Packet.yOffsets[direction]
		try:
			mapChar = self.map[testY][testX]
		except IndexError:
			mapChar = None
		return mapChar

	def nextDirection(self):
		testDirections = [Direction.LEFT, Direction.RIGHT] if self.direction in [Direction.UP, Direction.DOWN] \
      else [Direction.UP, Direction.DOWN]
		for direction in testDirections:
			if self.nextChar(direction) not in [None, " "]:
				newDirection = direction
				break
		else:
			raise ValueError
		return newDirection

	def move(self):
		reachedEnd = False
		try:
			mapChar = self.map[self.y][self.x]
			self.stepCount += 1
		except IndexError:
			mapChar = None
			reachedEnd = True
		if mapChar is None:
			pass
		elif mapChar in "|-":
			# Keep going in the same direction
			pass
		elif mapChar == "+":
			# Figure out which direction to go next
			nextChar = self.nextChar(self.direction)
			if nextChar in [None, " "]:
				# Can't keep going in the same direction
				try:
					self.direction = self.nextDirection()
				except ValueError:
					# There is no valid next direction
					reachedEnd = True
		elif mapChar == " ":
			self.stepCount -= 1
			reachedEnd = True
		else:
			self.path += mapChar

		if not reachedEnd:
			self.x += Packet.xOffsets[self.direction]
			self.y += Packet.yOffsets[self.direction]
		return not reachedEnd


def day19(fileName):
	map = []
	with open(fileName) as infile:
		for line in infile:
			map.append(line.rstrip())
	packet = Packet(map)
	return packet.start()


if __name__ == "__main__":
	path, stepCount = day19("19.txt")
	print(path)
	print(f"{stepCount} steps")
	# 16493 is wrong

