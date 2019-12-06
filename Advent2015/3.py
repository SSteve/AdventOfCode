from collections import defaultdict

class Santa():
	def __init__(self, houses):
		self.x = 0
		self.y = 0
		self.houses = houses
		self.houses[(self.x, self.y)] += 1
		
	def move(self, char):
		if char == "<":
			self.x -= 1
		elif char == "^":
			self.y -= 1
		elif char == ">":
			self.x += 1
		elif char == "v":
			self.y += 1
		self.houses[(self.x, self.y)] += 1

def day3(fileName, part):
	houses = defaultdict(int)
	santa = Santa(houses)
	santas = [santa]
	if part == 2:
		santa2 = Santa(houses)
		santas.append(santa2)
	currentSanta = 0
	with open(fileName) as infile:
		for line in infile:
			for char in line.strip():
				santas[currentSanta].move(char)
				currentSanta = (currentSanta + 1) % len(santas)
	print(len(santa.houses))
	
if __name__ == "__main__":
	day3("3.txt", 1)
	day3("3.txt", 2)
