import re

layerRegex = re.compile(r"(\d+): (\d+)")

def day13(fileName):
	layers = {}
	with open(fileName) as infile:
		for line in infile:
			match = layerRegex.match(line)
			if match:
				if int(match[2]) < 2:
					print(f"layer length {int(match[2])}")
				layers[int(match[1])] = int(match[2])
	severity = 0
	for layer in layers:
		if layer % (layers[layer] * 2 - 2) == 0:
			severity += layer * layers[layer]
	print(f"part 1: {severity}")
	delay = 0
	caught = True
	while caught:
		delay += 1
		for layer in layers:
			if (layer + delay) % (layers[layer] * 2 - 2) == 0:
				break
		else:
			caught = False
	print(f"part 2: {delay}")
				
if __name__ == "__main__":
	day13("13.txt")

