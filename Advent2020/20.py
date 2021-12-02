import re


tileRegex = re.compile(r"Tile (\d\d\d\d):")


def ReverseBits(n: int, bits: int) -> int:
    result = 0
    for i in range(bits):
        result <<= 1
        result |= n & 1
        n >>= 1
    return result


class GridLocation:
    def __init__(self, flip: int):
        self.flip = flip
        self.top = None
        self.right = None
        self.bottom = None
        self.left = None

    def __repr__(self):
        return f"flip: {self.flip} neighbors: {self[0]}, {self[1]}, {self[2]}, {self[3]}"

    def count(self) -> int:
        count = 0
        if self.top:
            count += 1
        if self.right:
            count += 1
        if self.bottom:
            count += 1
        if self.left:
            count += 1
        return count

    def __getitem__(self, key: int):
        if 0 > key > 4:
            raise IndexError
        return [self.top, self.right, self.bottom, self.left][key]

    def __setitem__(self, key: int, value: int):
        if 0 > key > 4:
            raise IndexError
        if key == 0:
            self.top = value
        elif key == 1:
            self.right = value
        elif key == 2:
            self.bottom = value
        elif key == 3:
            self.left = value


class Tile:
    def __init__(self, lines: list[str]) -> None:
        self.values: list[int] = []
        for line in lines:
            lineValue = 0
            for char in line:
                lineValue *= 2
                if char == "#":
                    lineValue += 1
            self.values.append(lineValue)
        self.top = self.values[0]
        self.bottom = self.values[9]
        self.left = 0
        self.right = 0
        for value in self.values:
            self.left *= 2
            self.right *= 2
            if value >= 2 ** 9:
                self.left += 1
            if value & 1:
                self.right += 1

        self.topReverse = ReverseBits(self.top, 10)
        self.bottomReverse = ReverseBits(self.bottom, 10)
        self.leftReverse = ReverseBits(self.left, 10)
        self.rightReverse = ReverseBits(self.right, 10)

    def connectsToTile(self, other) -> tuple[int, int, int, int]:
        for flip in range(4):
            for side in range(4):
                for otherFlip in range(4):
                    for otherSide in range(4):
                        if self.side(flip, side) == other.side(otherFlip, otherSide):
                            return (flip, side, otherFlip, otherSide)
        return None

    def connectsOnSide(self, flip: int, side: int, other) -> tuple[int, int]:
        mySide = self.side(flip, side)
        for otherFlip in range(4):
            for otherSide in range(4):
                otherSideValue = other.side(otherFlip, otherSide)
                if mySide == otherSideValue:
                    return (otherFlip, otherSide)
        return None

    def side(self, flip: int, side: int):
        # flip: 0=none, 1=vertical, 2=horizontal, 3=vertical&horizontal.
        # side: 0=top, 1=right, 2=bottom, 3=left.
        if flip == 0:
            if side == 0:
                return self.top
            elif side == 1:
                return self.right
            elif side == 2:
                return self.bottom
            elif side == 3:
                return self.left
        elif flip == 1:
            # Vertical flip:
            #   top & bottom are swapped.
            #   left & right are reversed.
            if side == 0:
                return self.bottom
            elif side == 1:
                return self.rightReverse
            elif side == 2:
                return self.top
            elif side == 3:
                return self.leftReverse
        elif flip == 2:
            # Horizontal flip:
            #   top & bottom are reversed.
            #   left & right are swapped.
            if side == 0:
                return self.topReverse
            elif side == 1:
                return self.left
            elif side == 2:
                return self.bottomReverse
            elif side == 3:
                return self.right
        elif flip == 3:
            # Vertical & Horizontal flip:
            #   Each side is swapped and reversed.
            if side == 0:
                return self.bottomReverse
            elif side == 1:
                return self.leftReverse
            elif side == 2:
                return self.topReverse
            elif side == 3:
                return self.rightReverse


class OrientedTile:
    def __init__(self, tile: Tile, flip: int):
        self.tile = tile
        self.flip = flip

    def connectsOnSide(self, side: int, other) -> tuple[int, int]:
        for otherFlip in range(4):
            for otherSide in range(4):
                if self.tile.connectsOnSide(self.flip, side, other) == other.side(otherFlip, otherSide):
                    return (otherFlip, otherSide)
        return None


def BuildGrid(tiles: dict[int, Tile]) -> dict[int, GridLocation]:
    grid = {}

    for tileId in tiles:
        tile = tiles[tileId]
        if tileId in grid:
            # If this tile is already in the grid, we can't change its orientation.
            orientations = [grid[tileId].flip]
        else:
            # If the tile isn't in the grid, we can try all orientations.
            orientations = [0, 1, 2, 3]
        for orientation in orientations:
            if tileId in grid and grid[tileId].flip != orientation:
                # This ends the loop when we're trying all orientations
                # and have found one that works.
                break
            for side in range(4):
                if tileId in grid and grid[tileId][side] is not None:
                    # If we already have a connection for this side, skip to the next.
                    continue
                for otherId in tiles:
                    if otherId == tileId:
                        # Don't try to connect a tile with itself.
                        continue
                    if result := tile.connectsOnSide(orientation, side, tiles[otherId]):
                        # result[0]: orientation of other tile.
                        # result[1]: side of other tile that connects to this tile.
                        # print(f"tile {tileId} side {side} connects to {otherId} in orientation {result[0]} on side {result[1]}")
                        if tileId not in grid:
                            grid[tileId] = GridLocation(orientation)
                        grid[tileId][side] = otherId
                        if otherId not in grid:
                            grid[otherId] = GridLocation(result[0])
                            grid[otherId][result[1]] = tileId
                        elif grid[otherId] == result[0]:
                            # The other tile is in the grid and in the desired orientation.
                            grid[otherId][result[1]] = tileId
                        else:
                            # The other tile is in the grid but not in the desired orientation.
                            # This is ok for part 1, but it breaks part 2.
                            # print("Orientation is wrong.")
                            pass
                        break

    return grid


def FindUpperLeftTile(grid: dict[int, GridLocation]) -> int:
    # Return the id of the tile in the upper-left of the grid.
    for tile in grid:
        if grid[tile].count() == 2:
            print(f"{tile}: {grid[tile]}")
        if grid[tile].count() == 2 and grid[tile].right is not None and \
                grid[tile].bottom is not None:
            return tile
    return None


def BuildSea(tiles: dict[int, Tile], grid: dict[int, GridLocation]) -> list[list[str]]:
    pass


def BuildTiles(lines: list[str]) -> dict[int, Tile]:
    # Build a list of Tiles from the given input strings
    tiles = {}
    while True:
        idLine = next(lines, "")
        if idLine == "":
            break

        # The first line is the id.
        tileId = int(tileRegex.match(idLine)[1])

        tileLines = []
        for _ in range(10):
            tileLines.append(next(lines))

        tile = Tile(tileLines)
        tiles[tileId] = tile

        # Read blank line between tiles.
        next(lines, "")

    return tiles


if __name__ == "__main__":
    with open("20test.txt", "r") as infile:
        testTiles = BuildTiles(map(str.rstrip, infile))
        grid = BuildGrid(testTiles)
        testResult = 1
        cornerCount = 0
        for tile in testTiles:
            gridLocation = grid[tile]
            if gridLocation.count() == 2:
                cornerCount += 1
                testResult *= tile
        print(f"{cornerCount} corners, answer: {testResult}")
        print(f"Upper left: {FindUpperLeftTile(grid)}")

    with open("20.txt", "r") as infile:
        tiles = BuildTiles(map(str.rstrip, infile))
        grid = BuildGrid(tiles)
        result = 1
        cornerCount = 0
        for tile in tiles:
            gridLocation = grid[tile]
            if gridLocation.count() == 2:
                cornerCount += 1
                result *= tile
        print(f"{cornerCount} corners, answer: {result}")
        print(f"Upper left: {FindUpperLeftTile(grid)}")
