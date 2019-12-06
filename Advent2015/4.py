from hashlib import md5

def day4(secretKey, zeroes):
	zeroString = zeroes * "0"
	seed = 1
	found = False
	while not found:
		val = f"{secretKey}{seed}"
		hash = md5(str.encode(val)).hexdigest()
		if hash[:zeroes] == zeroString:
			print(f"{seed}: {hash}")
			found = True
		seed += 1
		
day4("abcdef", 5)
day4("pqrstuv", 5)
day4("yzbqklnj", 5)
day4("yzbqklnj", 3)
day4("yzbqklnj", 6)
