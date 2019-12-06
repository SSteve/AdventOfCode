class Hex:
	def __init__(self, q, r):
		self.q = q
		self.r = r
		
	@property
	def s(self):
		return -self.q - self.r
		
	def move(self, direction):
		return self + Hex.directions[direction]
		
	def length(self):
		return int((abs(self.q) + abs(self.r) + abs(self.s)) / 2)
		
	def distance(self, other):
		return (self - other).length()
		
	def __add__(self, other):
		return Hex(self.q + other.q, self.r + other.r)
		
	def __sub__(self, other):
		return Hex(self.q - other.q, self.r - other.r)
		
Hex.directions = {
		"n": Hex(0, -1),
		"ne": Hex(1, -1),
		"se": Hex(1, 0),
		"s": Hex(0, 1),
		"sw": Hex(-1, 1),
		"nw": Hex(-1, 0),
		}
		


		
def day11a(fileName):
	with open(fileName) as infile:
		for line in infile:
			directions = line.strip().split(",")
			tile = Hex(0, 0)
			furthest = 0
			for direction in directions:
				tile = tile.move(direction)
				furthest = max(furthest, tile.length())
			print(tile.distance(Hex(0, 0)), furthest) 
			
if __name__ == "__main__":
	day11a("11.txt")
