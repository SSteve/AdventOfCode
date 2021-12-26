from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Optional

from generic_search import astar, nodeToPath

TEST = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y


def ManhattanDistance(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


homeX: dict[str, int] = {'A': 2, 'B': 4, 'C': 6, 'D': 8}

costs: dict[str, int] = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

hallXPositions: list[int] = [0, 1, 3, 5, 7, 9, 10]


@dataclass(frozen=True)
class AmphipodState:
    a1: Point
    a2: Point
    b1: Point
    b2: Point
    c1: Point
    c2: Point
    d1: Point
    d2: Point

    def AllPositions(self) -> set[Point]:
        return {self.a1, self.a2, self.b1, self.b2, self.c1, self.c2, self.d1, self.d2}

    def AsDict(self) -> dict[str, list[Point]]:
        return {'A': [self.a1, self.a2],
                'B': [self.b1, self.b2],
                'C': [self.c1, self.c2],
                'D': [self.d1, self.d2],
                }

    def AtPoint(self, p: Point) -> Optional[str]:
        dict = self.AsDict()
        for c in dict:
            if p in dict[c]:
                return c
        return None

    @staticmethod
    def FromText(lines: list[str]) -> AmphipodState:
        positions: dict[str, list[Point]] = defaultdict(list[Point])
        for x in range(3, 11, 2):
            for y in range(2, 4):
                # Our origin is the first empty hallway space, so the amphipod
                # rooms are at x = 2, 4, 6, & 8 and y = -1 & -2
                positions[lines[y][x]].append(Point(x - 1, -y + 1))
        for c in positions:
            positions[c].sort
        return AmphipodState.FromDict(positions)

    @staticmethod
    def FromDict(positions: dict[str, list[Point]]) -> AmphipodState:
        return AmphipodState(
            positions['A'][0],
            positions['A'][1],
            positions['B'][1],
            positions['B'][0],
            positions['C'][0],
            positions['C'][1],
            positions['D'][0],
            positions['D'][1],
        )

    def IsComplete(self) -> bool:
        dict = self.AsDict()
        for c in dict.keys():
            if Point(homeX[c], -2) not in dict[c] or Point(homeX[c], -1) not in dict[c]:
                return False
        return True

    def Heuristic(self) -> float:
        """
        The heuristic cost is the shortest path of each amphipod to its home.
        """
        cost = 0
        for c, positions in self.AsDict().items():
            for i, position in enumerate(positions):
                # The home y positions are -2 and -1, so they are i - 2 since i will be 0 and 1.
                cost += ManhattanDistance(position,
                                          Point(homeX[c], i - 2)) * costs[c]
        return cost

    def Print(self) -> None:
        print('#############')
        print('#', end='')
        for x in range(0, 11):
            c = self.AtPoint(Point(x, 0))
            print(c if c else '.', end='')
        print('#')
        # Third and fourth rows
        for y in range(-1, -3, -1):
            print('###' if y == -1 else '  #', end='')
            for x in range(2, 10, 2):
                c = self.AtPoint(Point(x, y))
                print(c if c else '.', end='')
                print('#', end='')
            print('##' if y == -1 else '')
        # Bottom row
        print('  #########\n')

    def Cost(self, nextState: AmphipodState) -> float:
        startPoints = self.AllPositions().difference(nextState.AllPositions())
        endPoints = nextState.AllPositions().difference(self.AllPositions())
        if len(startPoints) != 1 or len(endPoints) != 1:
            raise ValueError(
                "There can only be one amphipod in a different location between successive states.")
        startPoint = startPoints.pop()
        endPoint = endPoints.pop()
        startValue = self.AtPoint(startPoint)
        endValue = nextState.AtPoint(endPoint)
        if startValue is None:
            raise ValueError(f"Nothing found at {startPoint}.")
        if endValue is None:
            raise ValueError(f"Nothing found at {endPoint}.")
        if startValue != endValue:
            raise ValueError(
                f"Value at {startPoint} ({startValue}) doesn't match value at {endPoint} ({endValue}).")
        return ManhattanDistance(startPoint, endPoint) * costs[startValue]

    def ReplacePosition(self, c: str, x: int, y: int, i: int) -> AmphipodState:
        newState = self.AsDict()
        newState[c][i] = Point(x, y)
        newState[c].sort()
        return AmphipodState.FromDict(newState)

    def MoveHome(self, c: str, i: int, position: Point) -> Optional[AmphipodState]:
        """
        Given an amphipod in the hall, move it home if possible. This isn't iterable
        because there's only one possible move.
        """
        bottomPosition = self.AtPoint(Point(homeX[c], -2))
        # If the bottom position has a character that isn't at home, return None.
        if bottomPosition and bottomPosition != c:
            return None
        # At this point, if there's something in the bottom position, it's the character
        # at home. If there isn't, this is the target spot. If there is something here,
        # this is the target. If not, we'll check to see if the upper spot is open and
        # if so, make that the target.
        if bottomPosition is None:
            targetY = -2
        else:
            # Now we know the bottom position is a character at home. If the top position
            # is empty, it is the target.
            topPosition = self.AtPoint(Point(homeX[c], -1))
            if topPosition:
                # There's something in the top position that is not a character at home.
                # We can't move here.
                return None
            targetY = -1
        for testX in range(position.x - 1, homeX[c], -1) if position.x > homeX[c] else range(position.x + 1, homeX[c]):
            # Look to see if there's something between here and the home position.
            if self.AtPoint(Point(testX, 0)):
                return None
        return self.ReplacePosition(c, homeX[c], targetY, i)

    def MoveToHall(self, c: str, i: int, position: Point) -> Iterable[Optional[AmphipodState]]:
        """
        Given an amphipod in a side room, return any hall positions it can move to.
        """
        if position == Point(homeX[c], -2):
            # If it's in the bottom slot, this amphipod is already home.
            return None
        if position == Point(homeX[c], -1):
            # If it's in the top slot, it's only home if the bottom is the same character.
            bottomChar = self.AtPoint(Point(homeX[c], -2))
            if bottomChar == c:
                return None
        if position.y == -2 and Point(position.x, -1) in self.AllPositions():
            # This amphipod is in the bottom slot of a room and the upper slot is occupied.
            return None
        # At this point we know the amphipod can get out of the room. Now we return all the
        # hallway positions it can reach.
        for testX in range(position.x - 1, -1, -1):
            # Look at the positions to the left.
            if Point(testX, 0) in self.AllPositions():
                # If we've encountered another amphipod in the hall, stop looking in this direction.
                break
            if testX in hallXPositions:
                yield self.ReplacePosition(c, testX, 0, i)
        for testX in range(position.x + 1, 11):
            # Look at the positions to the right.
            if Point(testX, 0) in self.AllPositions():
                # If we've encountered another amphipod in the hall, stop looking in this direction.
                break
            if testX in hallXPositions:
                yield self.ReplacePosition(c, testX, 0, i)

    def Successors(self) -> Iterable[AmphipodState]:
        # Find amphipods in side rooms that can move to the hall.
        dict = self.AsDict()
        for c in dict:
            for i, position in enumerate(dict[c]):
                if position.y == 0:
                    newState = self.MoveHome(c, i, position)
                    if newState is not None:
                        yield newState
                else:
                    for s in self.MoveToHall(c, i, position):
                        if s:
                            yield s


@dataclass(frozen=True)
class AmphipodState2:
    """
    A separate class for Part 2 (instead of trying to make the part 1 class
    work with four rows).
    """
    a1: Point
    a2: Point
    a3: Point
    a4: Point
    b1: Point
    b2: Point
    b3: Point
    b4: Point
    c1: Point
    c2: Point
    c3: Point
    c4: Point
    d1: Point
    d2: Point
    d3: Point
    d4: Point

    def AllPositions(self) -> set[Point]:
        return {
            self.a1, self.a2, self.b1, self.b2, self.c1, self.c2, self.d1, self.d2,
            self.a3, self.a4, self.b3, self.b4, self.c3, self.c4, self.d3, self.d4
        }

    def AsDict(self) -> dict[str, list[Point]]:
        return {'A': [self.a1, self.a2, self.a3, self.a4],
                'B': [self.b1, self.b2, self.b3, self.b4],
                'C': [self.c1, self.c2, self.c3, self.c4],
                'D': [self.d1, self.d2, self.d3, self.d4],
                }

    def AtPoint(self, p: Point) -> Optional[str]:
        dict = self.AsDict()
        for c in dict:
            if p in dict[c]:
                return c
        return None

    @staticmethod
    def FromText(lines: list[str]) -> AmphipodState2:
        positions: dict[str, list[Point]] = defaultdict(list[Point])
        for x in range(3, 11, 2):
            for y in range(2, 4):
                # Our origin is the first empty hallway space, so the amphipod
                # rooms are at x = 2, 4, 6, & 8 and y = -1 & -4
                # Convert 2 to -1 and 3 to -4
                pointY = -3 * y + 5
                positions[lines[y][x]].append(Point(x - 1, pointY))
        # Add the two hidden lines from the diagram.
        positions['D'].append(Point(2, -2))
        positions['C'].append(Point(4, -2))
        positions['B'].append(Point(6, -2))
        positions['A'].append(Point(8, -2))
        positions['D'].append(Point(2, -3))
        positions['B'].append(Point(4, -3))
        positions['A'].append(Point(6, -3))
        positions['C'].append(Point(8, -3))
        for c in positions:
            positions[c].sort
        return AmphipodState2.FromDict(positions)

    @staticmethod
    def FromDict(positions: dict[str, list[Point]]) -> AmphipodState2:
        return AmphipodState2(
            positions['A'][0],
            positions['A'][1],
            positions['A'][2],
            positions['A'][3],
            positions['B'][0],
            positions['B'][1],
            positions['B'][2],
            positions['B'][3],
            positions['C'][0],
            positions['C'][1],
            positions['C'][2],
            positions['C'][3],
            positions['D'][0],
            positions['D'][1],
            positions['D'][2],
            positions['D'][3],
        )

    def IsComplete(self) -> bool:
        dict = self.AsDict()
        for c in dict.keys():
            for y in range(-4, 0, 1):
                if Point(homeX[c], y) not in dict[c]:
                    return False
        return True

    def Heuristic(self) -> float:
        """
        The heuristic cost is the shortest path of each amphipod to its home.
        """
        cost = 0
        for c, positions in self.AsDict().items():
            for i, position in enumerate(positions):
                # The home y positions are -4 thru -1, so they are i - 4 since i will be 0 thru 3.
                cost += ManhattanDistance(position,
                                          Point(homeX[c], i - 4)) * costs[c]
        return cost

    def Print(self) -> None:
        print('#############')
        print('#', end='')
        for x in range(0, 11):
            c = self.AtPoint(Point(x, 0))
            print(c if c else '.', end='')
        print('#')
        # Third thru sixth rows
        for y in range(-1, -5, -1):
            print('###' if y == -1 else '  #', end='')
            for x in range(2, 10, 2):
                c = self.AtPoint(Point(x, y))
                print(c if c else '.', end='')
                print('#', end='')
            print('##' if y == -1 else '')
        # Bottom row
        print('  #########\n')

    def Cost(self, nextState: AmphipodState2) -> float:
        startPoints = self.AllPositions().difference(nextState.AllPositions())
        endPoints = nextState.AllPositions().difference(self.AllPositions())
        if len(startPoints) != 1 or len(endPoints) != 1:
            raise ValueError(
                "There can only be one amphipod in a different location between successive states.")
        startPoint = startPoints.pop()
        endPoint = endPoints.pop()
        startValue = self.AtPoint(startPoint)
        endValue = nextState.AtPoint(endPoint)
        if startValue is None:
            raise ValueError(f"Nothing found at {startPoint}.")
        if endValue is None:
            raise ValueError(f"Nothing found at {endPoint}.")
        if startValue != endValue:
            raise ValueError(
                f"Value at {startPoint} ({startValue}) doesn't match value at {endPoint} ({endValue}).")
        return ManhattanDistance(startPoint, endPoint) * costs[startValue]

    def ReplacePosition(self, c: str, x: int, y: int, i: int) -> AmphipodState2:
        newState = self.AsDict()
        newState[c][i] = Point(x, y)
        newState[c].sort()
        return AmphipodState2.FromDict(newState)

    def MoveHome(self, c: str, i: int, position: Point) -> Optional[AmphipodState2]:
        """
        Given an amphipod in the hall, move it home if possible. This isn't iterable
        because there's only one possible move.
        """
        targetY = -4
        while targetY < 0:
            valueAtTarget = self.AtPoint(Point(homeX[c], targetY))
            # If the character at the target position is a character that isn't at
            # home, return None because we can't move into the room.
            if valueAtTarget is None:
                # There is nothing at this location so it is the target location.
                break
            if valueAtTarget != c:
                return None
            # This is a character at home so look in the next higher slot.
            targetY += 1

        # At this point, targetY is the highest open spot in the room and all the lower
        # slots are characters at home.
        for testX in range(position.x - 1, homeX[c], -1) if position.x > homeX[c] else range(position.x + 1, homeX[c]):
            # Look to see if there's something between here and the home position.
            if self.AtPoint(Point(testX, 0)):
                return None
        return self.ReplacePosition(c, homeX[c], targetY, i)

    def MoveToHall(self, c: str, i: int, position: Point) -> Iterable[Optional[AmphipodState2]]:
        """
        Given an amphipod in a side room, return any hall positions it can move to.
        """
        if position.y < -1 and self.AtPoint(Point(position.x, position.y + 1)) is not None:
            # There's something above this in the room so it can't move.
            return None
        if position.x == homeX[c]:
            # This is in its home room and there's nothing above it. If everything below it
            # is in it's home room, it can't move.
            if all(self.AtPoint(Point(position.x, y)) == c for y in range(position.y - 1, -5, -1)):
                return None

        # At this point we know the amphipod can get out of the room. Now we return all the
        # hallway positions it can reach.
        for testX in range(position.x - 1, -1, -1):
            # Look at the positions to the left.
            if Point(testX, 0) in self.AllPositions():
                # If we've encountered another amphipod in the hall, stop looking in this direction.
                break
            if testX in hallXPositions:
                yield self.ReplacePosition(c, testX, 0, i)
        for testX in range(position.x + 1, 11):
            # Look at the positions to the right.
            if Point(testX, 0) in self.AllPositions():
                # If we've encountered another amphipod in the hall, stop looking in this direction.
                break
            if testX in hallXPositions:
                yield self.ReplacePosition(c, testX, 0, i)

    def Successors(self) -> Iterable[AmphipodState2]:
        # Find amphipods in side rooms that can move to the hall.
        dict = self.AsDict()
        for c in dict:
            for i, position in enumerate(dict[c]):
                if position.y == 0:
                    # This one is in the hall so see if it can move home.
                    newState = self.MoveHome(c, i, position)
                    if newState is not None:
                        yield newState
                else:
                    # This one is in a side room so see if it can move to the hall.
                    for s in self.MoveToHall(c, i, position):
                        if s:
                            yield s


def FindCost1(lines: list[str], showSolution: bool = False) -> int:
    pods = AmphipodState.FromText(lines)
    solution = astar(pods, AmphipodState.IsComplete,
                     AmphipodState.Successors, AmphipodState.Heuristic, AmphipodState.Cost)
    if solution is None:
        raise ValueError("No solution found.")
    previous = None
    if showSolution:
        for state in nodeToPath(solution):
            if previous:
                print(f"Cost: {previous.Cost(state)}")
            previous = state
            state.Print()
    return int(solution.cost)


def FindCost2(lines: list[str], showSolution: bool = False) -> int:
    pods = AmphipodState2.FromText(lines)
    solution = astar(pods, AmphipodState2.IsComplete,
                     AmphipodState2.Successors, AmphipodState2.Heuristic, AmphipodState2.Cost)
    if solution is None:
        raise ValueError("No solution found.")
    previous = None
    if showSolution:
        for state in nodeToPath(solution):
            if previous:
                print(f"Cost: {previous.Cost(state)}")
            previous = state
            state.Print()
            # This line was to print the output I used for the visualization.
            # print(state.AsDict())
    return int(solution.cost)


if __name__ == "__main__":
    part1 = FindCost1(TEST.splitlines(), False)
    assert part1 == 12521
    part2 = FindCost2(TEST.splitlines(), True)
    assert part2 == 44169

    with open("23.txt", "r") as infile:
        part1 = FindCost1(infile.readlines(), False)
    print(f"Part 1: {part1}")
    with open("23.txt", "r") as infile:
        part2 = FindCost2(infile.readlines(), False)
    print(f"Part 2: {part2}")
