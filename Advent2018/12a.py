import re
import pdb

def potSum(state, leftPot):
	potSum = 0
	for i in range(len(state)):
		if state[i] == '#':
			potSum += i + leftPot
	return potSum

noteLine = re.compile("(.....) => (.)")

notes=[]
with open("12.txt", "r") as infile:
	for line in infile:
		match = noteLine.match(line)
		if match and match[2] == '#':
			notes.append(match[1])
			continue
		match = re.match("initial state: (.*)", line)
		if match:
			state = match[1]
			
leftPot = 0
generations = []

for generation in range(200):
	while state[:5] != '.....':
		state = '.' + state
		leftPot -= 1
	while state[-5:] != '.....':
		state = state + '.'
	print(generation, state, leftPot)
	"""
	if state in generations:
		pdb.set_trace()
	else:
		generations.append(state)
	"""
	newState = ""
	leftPot += 2
	for stateIndex in range(2, len(state) - 2):
		thisCell = state[stateIndex-2:stateIndex+3]
		#print(thisCell)
		foundMatch = False
		for note in notes:
			if note == thisCell:
				foundMatch = True
				break
		if foundMatch:
			newState += '#'
		else:
			newState += '.'

	state = newState
	
print(generation+1, state, leftPot)

print(potSum(state, leftPot))
