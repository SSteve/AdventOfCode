def day1(fileName):
	floor = 0
	firstBasement = None
	with open(fileName) as infile:
		chars = infile.readline()
		for position, char in enumerate(chars):
			if char == '(':
				floor += 1
			elif char == ')':
				floor -= 1
			
			if floor < 0 and firstBasement is None:
				firstBasement = position + 1
	print(f"Floor: {floor}")
	print(f"First basement: {firstBasement}")
	
if __name__ == "__main__":
	day1("1.txt")
