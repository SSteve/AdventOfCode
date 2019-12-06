def a1(fileName):
	firstDigit = None
	captcha = 0
	previousDigit = None
	with open(fileName) as infile:
		for line in infile:
			for char in line:
				if char not in "1234567890":
					continue
				if firstDigit is None:
					firstDigit = int(char)
					previousDigit = firstDigit
				else:
					newDigit = int(char)
					if newDigit == previousDigit:
						captcha += newDigit
					previousDigit = newDigit
	if previousDigit == firstDigit:
		captcha += firstDigit
	return captcha

def a2(fileName):
	captcha2 = 0
	with open(fileName) as infile:
		digits = infile.readline().strip()
	dLen = len(digits)
	halfLen = dLen // 2
	for inx, digit in enumerate(digits):
		if digit == digits[(inx + halfLen) % dLen]:
			captcha2 += int(digit)
	return captcha2
	
if __name__ == "__main__":
	fileName = "1.txt"
	print(a1(fileName))
	print(a2(fileName))
