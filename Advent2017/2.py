def a2(fileName, delimiter):
	checksum = 0
	with open(fileName) as infile:
		for line in infile:
			values = sorted([int(val) for val in line.split(delimiter)])
			checksum += values[-1] - values[0]
	return checksum
	
def a2b(fileName, delimiter):
	checksum = 0
	with open(fileName) as infile:
		for line in infile:
			values = [int(val) for val in line.split(delimiter)]
			lineChecksum = None
			for i in range(len(values)):
				if lineChecksum is not None:
					break
				for j in range(i + 1, len(values)):
					if lineChecksum is not None:
						break
					if values[i] / values[j] == values[i] // values[j]:
						lineChecksum = values[i] // values[j]
					elif values[j] / values[i] == values[j] // values[i]:
						lineChecksum = values[j] // values[i]
			checksum += lineChecksum

	return checksum
	
if __name__ == "__main__":
	print(a2("2.txt", "\t"))
	print(a2b("2.txt", "\t"))
