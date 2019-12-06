def react(compound):
	result = []
	for c in compound:
		if len(result) and c == result[-1].swapcase():
			result.pop()
		else:
			result.append(c)
	
	return ''.join(result)
			
with open("5.txt", "r") as infile:
	for line in infile:
		polymer = line.strip()

polymer = react(polymer)
	
print(len(polymer))
