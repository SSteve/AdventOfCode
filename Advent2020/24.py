import re

regex = r"(nw|ne|sw|se|e|w)"

class Hex:
    # Good article on hex coordinates at https://www.redblobgames.com/grids/hexagons/
    def __init__(self, q, r):
        self.q = q
        self.r = r

    @property
    def s(self):
        return -self.q - self.r

    def move(self, direction):
        return self + Hex.directions[direction]

    def length(self):
        return int((abs(self.q) + abs(self.r) + abs(self.s)) / 2)

    def distance(self, other):
        return (self - other).length()
        
    def around(self):
        # Return the coordinates of the six tiles aroind this one.
        for direction in Hex.directions:
            yield self.move(direction)

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r)

    def __sub__(self, other):
        return Hex(self.q - other.q, self.r - other.r)
        
    def __str__(self):
        return f"({self.q}, {self.r})"
        
    def __eq__(self, other):
        return self.q == other.q and self.r == other.r
        
    def __hash__(self):
        return hash((self.q, self.r))


Hex.directions = {
        "nw": Hex(0, -1),
        "ne": Hex(1, -1),
        "e": Hex(1, 0),
        "se": Hex(0, 1),
        "sw": Hex(-1, 1),
        "w": Hex(-1, 0),
        }

TEST = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""


def Traverse(line: str) -> Hex:
    tile = Hex(0, 0)
    matches = re.finditer(regex, line)
    for matchNum, match in enumerate(matches, start=1):
        tile = tile.move(match.group())
    return tile


def CountAround(tile: Hex, tiles):
    # Return the number of tiles around the given coordinate
    return sum(coordinate in tiles for coordinate in tile.around()) 
        
        
def Generation(blackTiles):
    whiteTiles = set()
    for tile in blackTiles:
        for adjacentTile in tile.around():
            if adjacentTile not in blackTiles:
                whiteTiles.add(adjacentTile)
    newBlackTiles = set()
    for tile in blackTiles:
        neighbors = CountAround(tile, blackTiles)
        if 0 < neighbors < 3:
            newBlackTiles.add(tile)
    for tile in whiteTiles:
        neighbors = CountAround(tile, blackTiles)
        if neighbors == 2:
            newBlackTiles.add(tile)
    return newBlackTiles
    
    
def Part1(lines):
    blackTiles = set()
    for line in lines:
        finalTile = Traverse(line)
        if finalTile in blackTiles:
            blackTiles.remove(finalTile)
        else:
            blackTiles.add(finalTile)
    return blackTiles
    
    
def Part2(blackTiles):
    for _ in range(100):
        blackTiles = Generation(blackTiles)
    return blackTiles
    
        
test1 = Part1(TEST.splitlines())
assert len(test1) == 10
test2 = Part2(test1)
assert len(test2) == 2208

with open("24.txt", "r") as infile:
    blackTiles = Part1(infile.read().splitlines())
print(f"Part 1: {len(blackTiles)}")
part2 = Part2(blackTiles)
print(f"Part 2: {len(part2)}")
