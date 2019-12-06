from collections import Counter

twos = 0
threes = 0
with open("3.txt", "r") as infile:
	for scan in infile:
		counts = Counter(scan.strip())
		has_two = False
		has_three = False
		#print(scan.strip())
		for count in counts.values():
			if count == 2:
				has_two = True
			if count == 3:
				has_three = True
		if has_two:
			twos += 1
		if has_three:
			threes += 1
		#print(twos, threes)
	print(twos * threes)
