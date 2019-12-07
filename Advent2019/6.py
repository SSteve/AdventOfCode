from generic_search import bfs, nodeToPath

class Orbits:
    def __init__(self, orbit_text):
        self.orbits = {}
        for orbit in orbit_text:
            planets = orbit.split(")")
            # The second planet orbits the first. Each planet can orbit only one other.
            self.orbits[planets[1].strip()] = planets[0].strip()
        
    def orbit_count(self):
        result = 0
        for orbit in self.orbits.items():
            result += 1
            parent = orbit[1]
            while parent != 'COM':
                result += 1
                parent = self.orbits[parent]
        return result

    # Create a series of strings to display the data with this graphviz command:
    # dot 6.dot -Tpdf > 6.pdf
    def dot_display(self):
        yield("graph {")
        yield("\trankdir=RL;")
        for orbit in self.orbits.items():
            # orbit[0] is orbited by orbit[1]
            yield(f'\t"{orbit[0]}" -- "{orbit[1]}";')
        yield("}")

    def successors(self, planet):
        # Return the planet this one orbits
        if planet in self.orbits:
            yield self.orbits[planet]
        # Return the planets that orbit this one
        for orbit in self.orbits.items():
            if orbit[1] == planet:
                yield orbit[0]

    def is_santa(self, planet):
        return planet == "SAN"
            
if __name__ == "__main__":
    # Tests
    orbits = Orbits("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L".split("\n"))
    assert orbits.orbit_count() == 42, "Test 1 failed"
    with open("6test1.dot", "w") as outfile:
        for orbit in orbits.dot_display():
            print(orbit, file=outfile)
    orbits = Orbits("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN".split("\n"))
    solution = bfs("YOU", orbits.is_santa, orbits.successors)
    path = nodeToPath(solution)
    assert len(path) - 3 == 4, "Test 2 failed"

    # Part 1
    with open("6.txt") as infile:
        orbits = Orbits(infile)
    print(f"Part one: {orbits.orbit_count()} total paths.")
    with open("6.dot", "w") as outfile:
        for orbit in orbits.dot_display():
            print(orbit, file=outfile)

    # Part 2
    solution = bfs("YOU", orbits.is_santa, orbits.successors)
    path = nodeToPath(solution)
    # Subtract 3 from the path length because we don't count "YOU", "SAN", or the common planet
    # you wind up orbiting
    print(f"{len(path) - 3} orbital transfers required")