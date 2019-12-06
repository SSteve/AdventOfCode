total_shift = 0
with open("1.txt", "r") as infile:
	for shift in infile:
		total_shift += (int(shift))
		
print(total_shift)
