freqs = set({0})
total_shift = 0
duplicate_found = False
while not duplicate_found:
	with open("2test1.txt", "r") as infile:
		for shift in infile:
			total_shift += (int(shift))
			if total_shift in freqs:
				duplicate_found = True
				break
			freqs.add(total_shift)
		
print(total_shift)
