import random

with open("4testsorted.txt", "r") as infile:
	lines = [line.strip() for line in infile]
	
random.shuffle(lines)

with open("4text.txt", "w") as outfile:
	for line in lines:
		print(line, file=outfile)
