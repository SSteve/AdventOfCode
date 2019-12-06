import re

boxRegex = re.compile(r"(\d+)x(\d+)x(\d+)")

def day2(fileName):
	totalPaper = 0
	totalRibbon = 0
	with open(fileName) as infile:
		for line in infile:
			match = boxRegex.match(line)
			if match:
				sides = sorted(int(side) for side in match.group(1, 2, 3))
				totalPaper += 3 * sides[0] * sides[1] + 2 * sides[1] * sides[2] + 2 * sides[2] * sides[0]
				totalRibbon += 2 * sides[0] + 2 * sides[1] + sides[0] * sides[1] * sides[2]
	print(totalPaper)
	print(totalRibbon)
	
if __name__ == "__main__":
	day2("2.txt")
