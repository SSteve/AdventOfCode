from enum import Enum

class GC_State(Enum):
	NOT_IN_GARBAGE = 1
	IN_GARBAGE = 2
	IN_GARBAGE_IGNORING_NEXT = 3

	@staticmethod
	def nextState(currentState, char):
		if currentState == GC_State.NOT_IN_GARBAGE:
			if char == "<":
				return GC_State.IN_GARBAGE
		if currentState == GC_State.IN_GARBAGE_IGNORING_NEXT:
			return GC_State.IN_GARBAGE
		if currentState == GC_State.IN_GARBAGE:
			if char == ">":
				return GC_State.NOT_IN_GARBAGE
			if char == "!":
				return GC_State.IN_GARBAGE_IGNORING_NEXT
		return currentState

def processLine(line):
	state = GC_State.NOT_IN_GARBAGE
	previousState = state
	groupLevel = 0
	score = 0
	garbageCount = 0
	nonGarbage = ""
	for char in line:
		if state == GC_State.NOT_IN_GARBAGE:
			if char == "{":
				groupLevel += 1
				score += groupLevel
			elif char == "}":
				groupLevel -= 1
				
		previousState = state
		state = GC_State.nextState(state, char)
		
		if state == GC_State.IN_GARBAGE:
			if previousState != GC_State.NOT_IN_GARBAGE and previousState != GC_State.IN_GARBAGE_IGNORING_NEXT:
				# Don't count opening ">" or character that is ignored
				garbageCount += 1
		if state == GC_State.NOT_IN_GARBAGE:
			if previousState != GC_State.IN_GARBAGE and char not in "{}":
				nonGarbage += char
	print(nonGarbage)
	return score, garbageCount

def day9a(fileName):
	with open(fileName) as infile:
		for line in infile:
			lineScore, garbageCount = processLine(line.strip())
			print(lineScore, garbageCount)
			
if __name__ == "__main__":
	day9a("9.txt")

