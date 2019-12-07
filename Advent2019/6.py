class Orbits:
	def __init__(self, orbit_text):
		self.orbits = {}
		for orbit in orbit_text:
			planets = orbit.split(")")
			self.orbits[planets[1]] = planets[0]
		print(self.orbits)
		
	def orbit_count(self):
		result = 0
		for orbit in self.orbits.items():
			result += 1
			parent = orbit[1]
			while parent != 'COM':
				result += 1
				parent = self.orbits[parent]
		return result
			
if __name__ == "__main__":
	# Tests
	orbits = Orbits("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L".split("\n"))
	assert orbits.orbit_count() == 42, "Test 1 failed"
	
	# Part 1
	with open("6.txt") as infile:
		orbits = Orbits(infile)
