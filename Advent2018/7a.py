import re

lineMatch = re.compile("Step (.) must be finished before step (.) can begin.")

order = []
ready = set()
steps = {}

with open("7.txt", "r") as infile:
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
while len(steps):
	#Make a list of the steps that are ready
	for step in steps:
		if len(steps[step]) == 0:
			ready.add(step)
			
	#Determine the next step, add it to the output, and remove it from the available steps
	nextstep = min(ready)
	order.append(nextstep)
	ready.remove(nextstep)
	del steps[nextstep]
	
	#Remove this step from all the prerequisites
	for value in stepvalues:
		value.difference_update(nextstep)
		
print(''.join(order))
