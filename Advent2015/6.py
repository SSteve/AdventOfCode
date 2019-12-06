import numpy as np
import re

lineRegex = re.compile(r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)")

def day6(fileName):
	lights = np.zeros((1000, 1000), dtype=bool)
	with open(fileName) as infile:
		for line in infile:
			match = lineRegex.match(line)
			if match:
				for x in range(int(match[2]), int(match[4]) + 1):
					for y in range(int(match[3]), int(match[5]) + 1):
						if match[1] == "turn on":
							lights[y, x] = True
						elif match[1] == "turn off":
							lights[y, x] = False
						elif match[1] == "toggle":
							lights[y, x] = not lights[y, x]
						else:
							raise ValueError(f"Unknown directive: {match[1]}")
	print(f"There are {lights.sum()} lights!")
				
def day6b(fileName):
	lights = np.zeros((1000, 1000), dtype=int)
	with open(fileName) as infile:
		for line in infile:
			match = lineRegex.match(line)
			if match:
				x1 = int(match[2])
				x2 = int(match[4])
				y1 = int(match[3])
				y2 = int(match[5])
				if match[1] == "turn on":
					lights[y1:y2 + 1, x1:x2 + 1] += 1
				elif match[1] == "turn off":
					for x in range(x1, x2 + 1):
						for y in range(y1, y2 + 1):
							lights[y, x] = max(lights[y, x] - 1, 0)
				elif match[1] == "toggle":
					lights[y1:y2 + 1, x1:x2 + 1] += 2
				else:
					raise ValueError(f"Unknown directive: {match[1]}")
	print(f"Brightness: {lights.sum()}")
				
#day6("6test.txt")
#day6("6.txt")
day6b("6btest.txt")
day6b("6.txt") #15343601
