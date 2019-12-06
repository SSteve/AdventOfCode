from collections import defaultdict
import re

instructionRegex = re.compile(r"(\w+) (dec|inc) (-?\d+) if (\w+) (.+) (-?\d+)")


def day8a(fileName):
	registers = defaultdict(int)
	largestEver = -1e20
	with open(fileName) as infile:
		for line in infile:
			match = instructionRegex.match(line)
			if match:
				destReg = match[1]
				delta = int(match[3])
				if match[2] == "dec":
					delta = -delta
				testReg = match[4]
				compareValue = int(match[6])
				compareOp = match[5]
				if eval(f"{registers[testReg]} {compareOp} {compareValue}"):
					registers[destReg] += delta
					largestEver = max(largestEver, registers[destReg])
				
	return max(registers.values()), largestEver
				
if __name__ == "__main__":
	largestEnd, largestEver = day8a("8.txt")
	print(largestEnd, largestEver)
