from dataclasses import dataclass
import hashlib

TEST = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __lt__(self, other: 'Point'):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x
        
    
class RockMap:
    rocks: set[Point]
    cubes: set[Point]
    width: int
    height: int

    def __init__(self, lines: list[str]):
        self.rocks = set()
        self.cubes = set()
        self.width = len(lines[0])
        self.height = len(lines)
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    self.cubes.add(Point(x, y))
                elif c == "O":
                    self.rocks.add(Point(x, y))
                    
    def __repr__(self):
        repr = ''
        for y in range(self.height):
            for x in range(self.width):
                point = Point(x,y)
                if point in self.rocks:
                    repr += 'O'
                elif point in self.cubes:
                    repr +='#'
                else:
                    repr +='.'
            repr += '\n'
        return repr
                    
    def fingerprint(self):
        rock_list = list(sorted(self.rocks))
        rock_string = ''.join(str(rock) for rock in rock_list)
        return hashlib.sha256(bytes(rock_string, 'UTF-8')).hexdigest()

    def cube_at_coordinate(self, x: int, y: int) -> bool:
        point = Point(x, y)
        return point in self.cubes

    def rock_at_coordinate(self, x: int, y: int) -> bool:
        point = Point(x, y)
        return point in self.rocks

    def remove_rock_at_coordinate(self, x: int, y: int) -> None:
        self.rocks.remove(Point(x, y))

    def add_rock_at_coordinate(self, x: int, y: int) -> None:
        self.rocks.add(Point(x, y))
        
    def north_load(self) -> int:
        load = 0
        for rock in self.rocks:
            load += self.height - rock.y
    
        return load

        
    def roll_north(self):
        for x in range(self.width):
            previous_cube = -1
            y = 0
            rock_coordinates: set[int] = set()
            while y <= self.height:
                if self.rock_at_coordinate(x, y):
                    rock_coordinates.add(y)
                elif self.cube_at_coordinate(x, y) or y == self.height:
                    for rock_y in rock_coordinates:
                        self.remove_rock_at_coordinate(x, rock_y)
                    for rock_y in range(previous_cube + 1, previous_cube + 1 + len(rock_coordinates)):
                        self.add_rock_at_coordinate(x, rock_y)
                    rock_coordinates.clear()
                    previous_cube = y
                y += 1

    def roll_south(self):
        for x in range(self.width):
            previous_cube = self.height
            y = self.height - 1
            rock_coordinates: set[int] = set()
            while y >=-1:
                if self.rock_at_coordinate(x, y):
                    rock_coordinates.add(y)
                elif self.cube_at_coordinate(x, y) or y == -1:
                    for rock_y in rock_coordinates:
                        self.remove_rock_at_coordinate(x, rock_y)
                    for rock_y in range(previous_cube - len(rock_coordinates), previous_cube):
                        self.add_rock_at_coordinate(x, rock_y)
                    rock_coordinates.clear()
                    previous_cube = y
                y -= 1
                
    def roll_west(self):
        for y in range(self.height):
            previous_cube = -1
            x = 0
            rock_coordinates: set[int] = set()
            while x <= self.width:
                if self.rock_at_coordinate(x, y):
                    rock_coordinates.add(x)
                elif self.cube_at_coordinate(x, y) or x == self.width:
                    for rock_x in rock_coordinates:
                        self.remove_rock_at_coordinate(rock_x, y)
                    for rock_x in range(previous_cube + 1, previous_cube + 1 + len(rock_coordinates)):
                        self.add_rock_at_coordinate(rock_x, y)
                    rock_coordinates.clear()
                    previous_cube = x
                x += 1

                
    def roll_east(self):
        for y in range(self.height):
            previous_cube = self.width
            x = self.width - 1
            rock_coordinates: set[int] = set()
            while x >= -1:
                if self.rock_at_coordinate(x, y):
                    rock_coordinates.add(x)
                elif self.cube_at_coordinate(x, y) or x == -1:
                    for rock_x in rock_coordinates:
                        self.remove_rock_at_coordinate(rock_x, y)
                    for rock_x in range(previous_cube - len(rock_coordinates), previous_cube):
                        self.add_rock_at_coordinate(rock_x, y)
                    rock_coordinates.clear()
                    previous_cube = x
                x -= 1

    def cycle(self):
        self.roll_north()
        self.roll_west()
        self.roll_south()
        self.roll_east()
                

def roll_north(lines: list[str]) -> int:
    rock_map = RockMap(lines)
    rock_map.roll_north()
    return rock_map.north_load()
    
def run_cycles(lines: list[str], count: int) -> int:
    rock_map = RockMap(lines)
    rock_map.cycle()
    fingerprint = rock_map.fingerprint()
    fingerprints = {}
    
    
    while fingerprint not in fingerprints:
        fingerprints[fingerprint]=rock_map.north_load()
        rock_map.cycle()
        fingerprint = rock_map.fingerprint()
        
    """
    for y, f in enumerate(fingerprints.items()):
        print(y,f)
    print(fingerprint)
    """
    print(len(fingerprints))
    previous_index = list(fingerprints.keys()).index(fingerprint)
    print(previous_index)
    cycle_length = len(fingerprints)- previous_index
    print(f"{cycle_length=}")
    index = ((count - (previous_index+1))%cycle_length)+previous_index
    print(f"{index=}")
    key = list(fingerprints.keys())[index]
    print(key)
    
    return fingerprints[key]

if __name__ == "__main__":    
    part1test = roll_north(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 136

    part2test = run_cycles(TEST.splitlines(), 1_000_000_000)
    print(f"Part 2 test: {part2test}")
    assert part2test == 64

    with open("day14.txt") as infile:
        lines = infile.read().splitlines()

    part1 = roll_north(lines)
    print(f"Part 1: {part1}")
    assert part1 == 103614

    
    part2 = run_cycles(lines, 1_000_000_000)
    print(f"Part 2: {part2}")
 
