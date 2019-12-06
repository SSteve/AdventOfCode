import re
import pdb

stateRegex = re.compile(r"In state (.):")
valueRegex = re.compile(r".*If the current value is (.)")
markRegex = re.compile(r".*Write the value (.)")
moveRegex = re.compile(r".*Move one slot to the (left|right)")
nextStateRegex = re.compile(r".*Continue with state (.)")


class State:
	def __init__(self, name, value, mark, move, nextState):
		self.name = name
		self.value = value
		self.mark = mark
		self.move = move
		self.nextState = nextState
		
	def __repr__(self):
		return f"State({self.name}, {self.value}, {self.mark}, {self.move}, {self.nextState})"
		
class Turing:
	def __init__(self, states, start):
		self.states = states
		self.currentState = start
		self.marks = set()
		self.position = 0
		
	def move(self):
		state = self.states[(self.currentState, self.position in self.marks)]
		if state.mark:
			self.marks.add(self.position)
		else:
			self.marks.discard(self.position)
		self.position += state.move
		self.currentState = state.nextState

def day25(fileName):
	states = {}
	with open(fileName) as infile:
		for lineNumber, line in enumerate(infile):
			if lineNumber == 0:
				match = re.match(r"Begin in state (.)", line)
				firstState = match[1]
			elif lineNumber == 1:
				match = re.match(r"Perform a diagnostic checksum after (\d+) steps", line)
				stepCount = int(match[1])
			else:
				#pdb.set_trace()
				match = stateRegex.match(line)
				if match:
					currentState = match[1]
					continue
				match = valueRegex.match(line)
				if match:
					currentValue = match[1] == "1"
					continue
				match = markRegex.match(line)
				if match:
					currentMark = match[1] == "1" 
					continue
				match = moveRegex.match(line)
				if match:
					currentMove = -1 if match[1] == "left" else 1
					continue
				match = nextStateRegex.match(line)
				if match:
					state = State(currentState, currentValue, currentMark, currentMove, match[1])
					states[(currentState, currentValue)] = state
				
	turing = Turing(states, firstState)
	print(states)
	for i in range(stepCount):
		turing.move()
		if i % 100000 == 0:
			print(i)
	print(len(turing.marks))
	
if __name__ == "__main__":
	day25("25.txt")
	
