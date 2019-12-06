def react(compound):
	result = []
	for c in compound:
		if len(result) and c == result[-1].swapcase():
			result.pop()
		else:
			result.append(c)
	
	return ''.join(result)
	
def remove_unit(compound, unit):
	trans = str.maketrans({unit.lower(): None, unit.upper(): None})
	return compound.translate(trans)

with open("5.txt", "r") as infile:
	for line in infile:
		polymer = line.strip()
		
best_unit = None
shortest = 50000
for unit_num in range(ord('a'), ord('z')+1):
	unit = chr(unit_num)
	new_compound = remove_unit(polymer, unit)
	#print(f"{unit}: {new_compound}")
	reacted_compound = react(new_compound)
	reacted_len = len(reacted_compound)
	print(f"{unit}, len: {reacted_len}")
	if reacted_len < shortest:
		best_unit = unit
		shortest = reacted_len
	
print(f"Best: {best_unit}, len = {shortest}")
