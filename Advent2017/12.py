from collections import defaultdict
import re

pipesRegex = re.compile(r"(\d+) <-> (.*)")

def progGroup(prog, progs):
	group = set([prog])
	frontier = [prog]
	while frontier:
		for theProg in progs[frontier.pop()]:
			if theProg not in group:
				group.add(theProg)
				frontier.append(theProg)
	
	return group

def day12a(fileName):
	progs = defaultdict(set)
	with open(fileName) as infile:
		for line in infile:
			match = pipesRegex.match(line)
			if match:
				thisProg = int(match[1])
				connected = [int(x) for x in match[2].split(", ")]
				for otherProg in connected:
					progs[thisProg].add(otherProg)
					progs[otherProg].add(thisProg)
	group = progGroup(0, progs)
	print(f"part 1: {len(group)}")
	allProgs = set(progs.keys())
	groupCount = 0
	while allProgs:
		groupCount += 1
		group = progGroup(allProgs.pop(), progs)
		allProgs -= group
	print(f"part 2: {groupCount}")

				
if __name__ == "__main__":
	day12a("12.txt")
