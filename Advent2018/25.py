import re
import pdb

pointRegex = re.compile(r"\s*(-?\d+),(-?\d+),(-?\d+),(-?\d+)")


class Point:
	def __init__(self, *args):
		self.x = int(args[0][0])
		self.y = int(args[0][1])
		self.z = int(args[0][2])
		self.t = int(args[0][3])
		
	def distanceTo(self, other):
		return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) + abs(self.t - other.t)
		
	def __repr__(self):
		return f"Point({self.x}, {self.y}, {self.z}, {self.t})"
		
	def __str__(self):
		return f"({self.x}, {self.y}, {self.z}, {self.t})"
		
		
def a25(fileName):
	constellations = []
	with open(fileName) as handle:
		for line in handle:
			match = pointRegex.match(line)
			if match:
				point = Point(match.group(1, 2, 3, 4))
				print(point)
				if len(constellations) == 0:
					constellations.append({point})
				else:
					newConstellation = set()
					joinedIndexes = []
					for (conIndex, constellation) in enumerate(constellations):
						for star in constellation:
							if point.distanceTo(star) <= 3:
								newConstellation |= constellation | {point}
								joinedIndexes.append(conIndex)
								break
					if len(joinedIndexes) == 0:
						# New point isn't in any constellation, create a new one
						constellations.append({point})
					elif len(joinedIndexes) == 1:
						# New point is in a single constellation so replace the existing with the new
						constellations[joinedIndexes[0]] = newConstellation
					else:
						# New point joins multiple constellations
						for popIndex in sorted(joinedIndexes, reverse=True):
							constellations.pop(popIndex)
						constellations.append(newConstellation)
			else:
				print(f"no match: {line}")
	#pdb.set_trace()
	#print(constellations)
	print(f"{len(constellations)} constellations")
	
if __name__ == "__main__":
	a25("25.txt")
