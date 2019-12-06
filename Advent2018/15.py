from dataclasses import dataclass
from typing import List, NamedTuple
import numpy as np

from generic_search import bfsCave, nodeToPath

wall = "#"
emptySpace = "."


class GridLocation(NamedTuple):
    column: int
    row: int

    def __lt__(self, other):
        return self.row < other.row or \
            self.row == other.row and self.column < other.column


def openLocations(cave, location: GridLocation) -> List[GridLocation]:
    """
    Return a list of the open locations around the given location. The locations are
    in reading order.
    """
    available = []
    row = cave[location.row]
    if location.row > 0 and cave[location.row - 1, location.column] == ".":
        available.append(GridLocation(location.column, location.row - 1))
    if location.column > 0 and row[location.column - 1] == ".":
        available.append(GridLocation(location.column - 1, location.row))
    if location.column + 1 < len(row) and row[location.column + 1] == ".":
        available.append(GridLocation(location.column + 1, location.row))
    if location.row + 1 < len(cave) and cave[location.row + 1, location.column] == ".":
        available.append(GridLocation(location.column, location.row + 1))
    return sorted(available)


def reachedLocation(currentLocation, goalLocation):
    return abs(currentLocation.row - goalLocation.row) + abs(currentLocation.column - goalLocation.column) == 1


@dataclass
class Unit:
    x: int
    y: int
    race: str
    hitPoints: int = 200
    attackDamage: int = 3

    def __str__(self):
        return f"{self.race}({self.hitPoints})"

    def __lt__(self, other):
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def location(self):
        return GridLocation(self.x, self.y)

    def sameLocation(self, other):
        """
        Return True if this unit is at the same location as other
        """
        return self.x == other.x and self.y == other.y

    def atLocation(self, x, y):
        """
        Return True if this unit is at this x,y location
        """
        return self.x == x and self.y == y

    def distanceTo(self, other):
        """
        Return the Manhattan distance between this unit and other

        Keyword arguments:
        other -- The other unit.
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def canAttack(self, units):
        """
        Return True if there is an enemy available to attack.

        Keyword arguments:
        units -- A list of all units. Does not need to be sorted.
        """
        for unit in units:
            if unit.hitPoints > 0 and unit.race != self.race and self.distanceTo(unit) == 1:
                return True
        return False

    def enemyExists(self, units):
        """
        Return True if an enemy exists. The enemy does not need to be available for attack.

        Keyword arguments:
        units -- A list of all units. Does not need to be sorted.
        """
        for unit in units:
            if unit.hitPoints > 0 and unit.race != self.race:
                return True
        return False

    def availableEnemies(self, cave, units):
        """
        Return a list of available enemies in the list

        Keyword arguments:
        units -- A list of all units. Does not need to be sorted.
        cave -- The array representing the cave
        """
        availableList = []
        for unit in units:
            if unit.hitPoints > 0 and unit.race != self.race and openLocations(cave, unit.location()):
                availableList.append(unit)
        return availableList

    def move(self, cave, units) -> None:
        targetLocation: GridLocation = None
        shortestPath = None
        enemies = self.availableEnemies(cave, units)
        for enemy in enemies:
            solution = bfsCave(self.location(), enemy.location(), reachedLocation, cave, openLocations)
            if solution:
                path = nodeToPath(solution)
                # We found a path. Now see if it's a better candidate than one already found
                pathEnd = path[-1]
                if shortestPath is None or len(path) < len(shortestPath) or \
                        len(path) == len(shortestPath) and (pathEnd < targetLocation):
                    targetLocation = pathEnd
                    shortestPath = path
        if shortestPath:
            cave[self.y, self.x] = '.'
            # The first step in the path is the current location so go to the second step
            nextLocation: GridLocation = shortestPath[1]
            self.x = nextLocation.column
            self.y = nextLocation.row
            cave[self.y, self.x] = self.race

    def attack(self, cave, units):
        """
        Attack an available enemy.

        units -- A list of all units. Does not need to be sorted.
        """
        target = None
        for unit in units:
            if unit.hitPoints > 0 and unit.race != self.race and self.distanceTo(unit) == 1:
                if target is None or unit.hitPoints < target.hitPoints or \
                        unit.hitPoints == target.hitPoints and unit < target:
                    target = unit
        if target is not None:
            target.hitPoints -= self.attackDamage
            if target.hitPoints <= 0:
                cave[target.y, target.x] = "."


def printCave(cave, units, showScores=False):
    for rowNumber, row in enumerate(cave):
        scores = "   "
        for columnNumber, cell in enumerate(row):
            print(cell, end='')
            if showScores and cell in ["E", "G"]:
                unit = next(unit for unit in units if unit.hitPoints > 0 and unit.atLocation(columnNumber, rowNumber))
                scores += str(unit) + " "
        if len(scores.strip()):
            print(scores, end='')
        print()


def loadPuzzle(puzzleName, elfAttackPower):
    # Get the dimensions of the puzzle.
    with open(puzzleName, "r") as infile:
        puzzleHeight = 0
        puzzleWidth = 0
        for line in infile:
            puzzleHeight += 1
            puzzleWidth = max(puzzleWidth, len(line.rstrip()))

    # Create the cave with the determined puzzle dimensions.
    cave = np.full((puzzleHeight, puzzleWidth), '.', dtype=str)
    units = []

    # Populate the cave and the list of units.
    with open(puzzleName, "r") as infile:
        for rowNumber, line in enumerate(infile):
            for columnNumber, cell in enumerate(line.rstrip()):
                if cell in ['E', 'G']:
                    units.append(Unit(columnNumber, rowNumber, cell, attackDamage=3 if cell == 'G' else elfAttackPower))
                cave[rowNumber, columnNumber] = cell
    return cave, units


if __name__ == "15a":
    cave, units = loadPuzzle("15.txt", 3)
    finished = False
    playRound = 0
    while not finished:
        for unit in units:
            if unit.hitPoints <= 0:
                continue
            if not unit.enemyExists(units):
                finished = True
                break
            if not unit.canAttack(units):
                unit.move(cave, units)
            unit.attack(cave, units)
        if not finished:
            playRound += 1
            print(playRound)
        livingUnits = [unit for unit in units if unit.hitPoints > 0]
        units = sorted(livingUnits)

if __name__ == "__main__":
    goblinsWin = True
    elfAttackPower = 3
    originalElfCount = 0
    survivingElfCount = 0
    while goblinsWin or survivingElfCount < originalElfCount:
        elfAttackPower += 1
        cave, units = loadPuzzle("15.txt", elfAttackPower)
        originalElfCount = len([unit for unit in units if unit.race == "E"])
        finished = False
        playRound = 0
        while not finished:
            for unit in units:
                if unit.hitPoints <= 0:
                    continue
                if not unit.enemyExists(units):
                    finished = True
                    break
                if not unit.canAttack(units):
                    unit.move(cave, units)
                unit.attack(cave, units)
                survivingElfCount = len([unit for unit in units if unit.race == "E" and unit.hitPoints > 0])
                if survivingElfCount < originalElfCount:
                    finished = True
                    break
            if not finished:
                playRound += 1
                print(playRound)
            livingUnits = [unit for unit in units if unit.hitPoints > 0]
            units = sorted(livingUnits)
        goblinsWin = units[0].race == "G"

    printCave(cave, units, showScores=True)
    print(f"Combat ends after {playRound} full rounds")
    hitPoints = sum([unit.hitPoints for unit in units])
    survivingRace = "Goblins" if units[0].race == "G" else "Elves"
    print(f"{survivingRace} win with {hitPoints} total hit points left")
    print(f"Outcome: {playRound} * {hitPoints} = {playRound * hitPoints}")
    print(f"Elf attack power: {elfAttackPower}")
