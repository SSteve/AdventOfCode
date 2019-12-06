def showList(numbers, pos):
	for i in range(len(numbers)):
		if i == pos:
			print(f"[{numbers[i]}]", end=" ")
		else:
			print(numbers[i], end=" ")
	print()


def knotHash(value):
	skipSize = 0
	pos = 0
	numbers = list(range(256))
	for _ in range(64):
		for i in range(len(value) + 5):
			if i < len(value):
				length = ord(value[i])
			else:
				length = [17, 31, 73, 47, 23][i % len(value)]
			performReverse(numbers, pos, length)
			pos = (pos + length + skipSize) % 256
			skipSize += 1
	denseHash = []
	for i in range(16):
		x = numbers[i * 16]
		for j in range(i * 16 + 1, i * 16 + 16):
			x ^= numbers[j]
		denseHash.append(x)
	hashStr = ""
	for hashval in denseHash:
		hashStr += f"{hashval:02x}"
	return hashStr


def day10a(fileName, listSize, shouldPrint=False):
	with open(fileName) as infile:
		line = infile.readline()
	lengths = [int(x) for x in line.strip().split(",")]
	skipSize = 0
	pos = 0
	numbers = list(range(listSize))
	for length in lengths:
		performReverse(numbers, pos, length)
		pos = (pos + length + skipSize) % listSize
		skipSize += 1
		if shouldPrint:
			showList(numbers, pos)

	return numbers


def day10b(fileName, listSize, shouldPrint=False):
	with open(fileName) as infile:
		for line in infile:
			line = line.strip()
			hashStr = knotHash(line)
			if shouldPrint:
				print(f"{line}: {hashStr}")
	return hashStr


if __name__ == "__main__":
	numbers = day10a("10.txt", 256, shouldPrint=False)
	print(numbers[0] * numbers[1])
	hash = day10b("10test1.txt", 256, shouldPrint=True)
	print(hash)

