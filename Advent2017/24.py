import re
import pdb

magcomRegex = re.compile(r"(\d+)/(\d+)")


class Magcom:
	def __init__(self, serial, port1, port2):
		self.serial = serial
		self.port1 = port1
		self.port2 = port2
		
	def __repr__(self):
		return f"{self.serial}: ({self.port1}, {self.port2})"
		
	def has(self, val):
		return self.port1 == val or self.port2 == val
		
	def other(self, val):
		return self.port1 if val == self.port2 else self.port2
		
	def available(self, port, unavailable):
		return self.serial not in unavailable and self.has(port)
		
	@property
	def strength(self):
		return self.port1 + self.port2
		
def findall(magcoms, port, bridge, found):
	"""
	Recursively create all complete bridges of magnetic components
	
	Keyword arguments
	magcoms -- Complete dictionary of all components. Key is the magcom serial.
	port -- The port number on the end we're extending.
	bridge -- A list of components already in this bridge.
	found -- A list of complete bridges found. This is a dictionary where the key is
		a tuple of the component serial numbers and the value is the bridge strength
	"""
	available = [mc for mc in magcoms.values() if mc.available(port, bridge)]
	#pdb.set_trace()
	if available:
		for mc in available:
			myBridge = bridge[:]
			myBridge.append(mc.serial)
			nextPort = mc.other(port)
			findall(magcoms, nextPort, myBridge, found)
	else:
		myBridge = tuple(bridge)
		strength = sum(magcoms[serial].strength for serial in bridge)
		found[myBridge] = strength
			

def day24(fileName):
	magcoms = {}
	with open(fileName) as infile:
		for lineNumber, line in enumerate(infile):
			match = magcomRegex.match(line)
			if match:
				magcoms[lineNumber] = Magcom(lineNumber, int(match[1]), int(match[2]))
	bridges = {}
	findall(magcoms, 0, [], bridges)
	return bridges


if __name__ == "__main__":
	bridges = day24("24.txt")
	print(max(bridges.values()))
	longest = (1, 0)
	for bridge, strength in bridges.items():
		if len(bridge) > longest[0]:
			longest = (len(bridge), strength)
		elif len(bridge) == longest[0] and strength > longest[1]:
			longest = (len(bridge), strength)
	print(longest[1])
