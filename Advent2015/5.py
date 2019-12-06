def day5(fileName, part):
	niceCount = 0
	with open(fileName) as infile:
		for line in infile:
			vowels = sum(line.count(vowel) for vowel in "aeiou")
			if vowels < 3:
				continue
			foundDouble = any(line[i] == line[i+1] for i in range(len(line) - 1))
			if not foundDouble:
				continue
			foundBadString = any(badString in line for badString in ["ab", "cd", "pq", "xy"])
			if foundBadString:
				continue
			niceCount += 1
	print(niceCount)
	
def day5b(fileName, part):
	niceCount = 0
	with open(fileName) as infile:
		for line in infile:
			repeatLetter = any(line[i] == line[i+2] for i in range(len(line) - 2))
			if not repeatLetter:
				continue
			repeatPair = any(line[i:i+2] in line[i+2:] for i in range(len(line) - 4))
			if not repeatPair:
				continue
			niceCount += 1
	print(niceCount)
		
	
if __name__ == "__main__":
	day5("5test.txt", 1)
	day5("5.txt", 1)
	day5b("5btest.txt", 0)
	day5b("5.txt", 0)
