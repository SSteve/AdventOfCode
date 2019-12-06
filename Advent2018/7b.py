import pdb
import re
"""
availableWorkers = 2
minimumStepLength = 1
inputFileName = "7test.txt"
"""
availableWorkers = 5
minimumStepLength = 61
inputFileName = "7.txt"


def stepSeconds(step):
	return ord(step) - ord('A') + minimumStepLength
	
def tick(workers):
	"""
	Subtract one second from each worker task.
	"""
	for worker in workers:
		workers[worker] -= 1
		

lineMatch = re.compile("Step (.) must be finished before step (.) can begin.")

order = []
ready = set()
steps = {}
workers = {}
totalSeconds = 0

with open(inputFileName, "r") as infile:
	for line in infile:
		match = lineMatch.match(line)
		pre = match[1]
		post = match[2]
		if not pre in steps:
			steps[pre] = set()
		if not post in steps:
			steps[post] = set(pre)
		else:
			steps[post].add(pre)
			
stepvalues = steps.values()

while len(steps) or len(workers):
	#Add any ready steps to the set of steps that are ready
	for step in steps:
		if len(steps[step]) == 0:
			ready.add(step)
	
	#Give the ready steps to available workers
	while len(ready) and len(workers) < availableWorkers:
		#Give the next available step to a worker
		nextstep = min(ready)
		workers[nextstep] = stepSeconds(nextstep)
		#Remove the step from consideration
		ready.remove(nextstep)
		del steps[nextstep]
		
	#Elapse one second
	tick(workers)
	totalSeconds += 1
	
	#Build a list of finished steps
	newlyFinished = []
	for worker in workers.items():
		if worker[1] == 0:
			#This step is finished. Add it to the list of newly-finished steps.
			newlyFinished.append(worker[0])
			
	#Process any finished steps
	while len(newlyFinished):
		nextstep = min(newlyFinished)
		newlyFinished.remove(nextstep)
		del workers[nextstep]
		order.append(nextstep)
		#Remove this step from all the prerequisites
		for value in stepvalues:
			value.difference_update(nextstep)
		
print(''.join(order))
print(totalSeconds)
