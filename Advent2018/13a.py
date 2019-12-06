import numpy as np

from enum import Enum

northCart = '^'
southCart = 'v'
westCart = '<'
eastCart = '>'
verticalCarts = [northCart, southCart]
horizontalCarts = [westCart, eastCart]
allCarts = verticalCarts + horizontalCarts

northEastCurve = '/'
northWestCurve = '\\'  # Double-backslash required for escaping
intersection = '+'
verticalTrack = '|'
horizontalTrack = '-'


class Orientation(Enum):
    """
    The direction a cart is currently facing
    """
    WEST = 1
    NORTH = 2
    EAST = 3
    SOUTH = 4

    def turn(self, direction):
        if direction == Direction.LEFT:
            return self.prev()
        if direction == Direction.STRAIGHT:
            return self
        if direction == Direction.RIGHT:
            return self.next()

    def next(self):
        if self == Orientation.WEST:
            return Orientation.NORTH
        if self == Orientation.NORTH:
            return Orientation.EAST
        if self == Orientation.EAST:
            return Orientation.SOUTH
        if self == Orientation.SOUTH:
            return Orientation.WEST

    def prev(self):
        if self == Orientation.WEST:
            return Orientation.SOUTH
        if self == Orientation.NORTH:
            return Orientation.WEST
        if self == Orientation.EAST:
            return Orientation.NORTH
        if self == Orientation.SOUTH:
            return Orientation.EAST

    @staticmethod
    def orientationFromCharacter(character):
        if character == northCart:
            return Orientation.NORTH
        elif character == southCart:
            return Orientation.SOUTH
        elif character == westCart:
            return Orientation.WEST
        elif character == eastCart:
            return Orientation.EAST

    def character(self):
        if self == Orientation.WEST:
            return westCart
        if self == Orientation.NORTH:
            return northCart
        if self == Orientation.EAST:
            return eastCart
        if self == Orientation.SOUTH:
            return southCart

    def offset(self):
        if self == Orientation.WEST:
            return (-1, 0)
        if self == Orientation.NORTH:
            return (0, -1)
        if self == Orientation.EAST:
            return (1, 0)
        if self == Orientation.SOUTH:
            return (0, 1)


class Direction(Enum):
    """
    The next direction a cart will turn
    """
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1

    def next(self):
        if self == Direction.LEFT:
            return Direction.STRAIGHT
        if self == Direction.STRAIGHT:
            return Direction.RIGHT
        if self == Direction.RIGHT:
            return Direction.LEFT


class Cart:
    def __init__(self, x: int, y: int, character, nextDirection=Direction.LEFT):
        self.x = x
        self.y = y
        self.orientation = Orientation.orientationFromCharacter(character)
        self.nextDirection = nextDirection

    def __repr__(self):
        return f"Cart({self.x}, {self.y}, " \
            f"{self.orientation.character()}, {self.nextDirection.name})"

    def __lt__(self, other):
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def asCharacter(self):
        return self.orientation.character()

    def atLocation(self, x, y):
        return self.x == x and self.y == y

    def move(self, tracks):
        # Calculate new position
        xOffset, yOffset = self.orientation.offset()
        self.x += xOffset
        self.y += yOffset
        # Calculate new orientation
        trackCell = tracks[self.y, self.x]
        if trackCell == intersection:
            self.orientation = self.orientation.turn(self.nextDirection)
            self.nextDirection = self.nextDirection.next()
        elif self.orientation == Orientation.WEST:
            if trackCell != horizontalTrack:
                if trackCell == northEastCurve:
                    self.orientation = Orientation.SOUTH
                elif trackCell == northWestCurve:
                    self.orientation = Orientation.NORTH
                else:
                    raise ValueError(
                        f"Vertical track encountered at ({self.x}, {self.y}) when moving west")
        elif self.orientation == Orientation.NORTH:
            if trackCell != verticalTrack:
                if trackCell == northEastCurve:
                    self.orientation = Orientation.EAST
                elif trackCell == northWestCurve:
                    self.orientation = Orientation.WEST
                else:
                    raise ValueError(
                        f"Horizontal track encountered at ({self.x}, {self.y}) when moving north")
        elif self.orientation == Orientation.EAST:
            if trackCell != horizontalTrack:
                if trackCell == northEastCurve:
                    self.orientation = Orientation.NORTH
                elif trackCell == northWestCurve:
                    self.orientation = Orientation.SOUTH
                else:
                    raise ValueError(
                        f"Vertical track encountered at ({self.x}, {self.y}) when moving east")
        elif self.orientation == Orientation.SOUTH:
            if trackCell != verticalTrack:
                if trackCell == northEastCurve:
                    self.orientation = Orientation.WEST
                elif trackCell == northWestCurve:
                    self.orientation = Orientation.EAST
                else:
                    raise ValueError(
                        f"Horizontal track encountered at ({self.x}, {self.y}) when moving south")


def printTracks(tracks, carts, quiet=False):
    """
    Print the current state.

    Return True if there was a collision
    """
    collisionCell = None
    for rowNumber, row in enumerate(tracks):
        for column, cell in enumerate(row):
            cartInCell = None
            for cart in carts:
                if cart.atLocation(column, rowNumber):
                    if cartInCell:
                        cartInCell = 'X'
                        if collisionCell is None:
                            collisionCell = (column, rowNumber)
                        break
                    else:
                        cartInCell = cart.asCharacter()
            if not quiet:
                if cartInCell:
                    print(cartInCell, end='')
                else:
                    print(cell, end='')
        if not quiet:
            print()
    if collisionCell is not None:
        print(f"Collision at {collisionCell}")
    if not quiet:
        print("\n\n\n\n")
    else:
        print(carts)
    return collisionCell is not None


def findCollision(carts):
    """
    sortedCarts = sorted(carts)
    for i in range(len(sortedCarts):
        if sortedCarts[i] == sortedCarts[i+1]:
            return (sortedCarts[i].x, sortedCarts[i].y)
    """
    for i, cart in enumerate(carts):
        for j in range(i + 1, len(carts)):
            if cart == carts[j]:
                print(f"Collision at {cart.x}, {cart.y}")
                return (cart.x, cart.y)
    return None


def loadPuzzle(puzzleInputName):
    # First get the bounds of the tracks
    with open(puzzleInputName, "r") as infile:
        tracksHeight = 0
        tracksWidth = 0
        for line in infile:
            tracksHeight += 1
            tracksWidth = max(tracksWidth, len(line.rstrip()))
    tracks = np.full((tracksHeight, tracksWidth), ' ', dtype=str)

    carts = []
    # Now populate the tracks and create the carts
    with open(puzzleInputName, "r") as infile:
        for lineNumber, line in enumerate(infile):
            for column, cell in enumerate(line.rstrip()):
                if cell in allCarts:
                    # This character is a cart
                    carts.append(Cart(column, lineNumber, cell))
                    # Add the underlying track type to tracks
                    if cell in horizontalCarts:
                        tracks[lineNumber, column] = '-'
                    else:
                        tracks[lineNumber, column] = '|'
                else:
                    tracks[lineNumber, column] = cell
    print(f"Track dimensions: {tracksWidth} x {tracksHeight}. {len(carts)} carts.")
    return carts, tracks


def aWithPrinting(puzzleName):
    carts, tracks = loadPuzzle(puzzleName)
    printTracks(tracks, carts)
    choice = " "
    while choice != "q":
        for cart in carts:
            cart.move(tracks)
        printTracks(tracks, carts)
        choice = input("(n)ext or (q)uit: ")


def aWithoutPrinting(puzzleName):
    carts, tracks = loadPuzzle(puzzleName)
    collisionCoordinates = None
    generation = 0
    while collisionCoordinates is None:
        generation += 1
        print(f"Generation {generation}")
        for cart in carts:
            cart.move(tracks)
            collisionCoordinates = findCollision(carts)
            if collisionCoordinates is not None:
                break


def b13(puzzleName, quiet):
    carts, tracks = loadPuzzle(puzzleName)
    if not quiet:
        printTracks(tracks, carts)
    choice = " "
    generation = 0
    while len(carts) > 1 and (quiet or choice != "q"):
        cartIndex = 0
        generation += 1
        # print(f"Generation {generation}")
        while cartIndex < len(carts):
            cart = carts[cartIndex]
            cart.move(tracks)
            collisionCoordinates = findCollision(carts)
            if collisionCoordinates is not None:
                # Remove colliding carts
                carts.pop(cartIndex)
                cartToRemove = Cart(collisionCoordinates[0], collisionCoordinates[1], " ")
                removeIndex = carts.index(cartToRemove)
                carts.pop(removeIndex)
                if removeIndex < cartIndex:
                    # We removed a cart earlier in the list than this one so we need to decrement cartIndex
                    cartIndex -= 1
            else:
                cartIndex += 1
        if not quiet:
            printTracks(tracks, carts)
        # print(f"{len(carts)} carts left.")
        if len(carts) == 1:
            print(f"Last cart: {carts[0]}")
        if not quiet:
            choice = input("(n)ext or (q)uit: ")


if __name__ == "__main__":
    b13("13.txt", True)
