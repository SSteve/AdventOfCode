with open("2.txt", "r") as infile:
	scans = [scan.strip() for scan in infile]
	
#print(scans)
for scan1 in range(len(scans)):
	for scan2 in range(scan1 + 1, len(scans)):
		differences = 0
		for letters in (zip(scans[scan1], scans[scan2])):
			if letters[0] != letters[1]:
				differences += 1
		
		if differences == 1:
			break
	if differences == 1:
		break
		
for letters in (zip(scans[scan1], scans[scan2])):
	if letters[0] == letters[1]:
		print(letters[0], end='')
