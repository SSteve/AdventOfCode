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


homeX: dict[str, int] = {'A': 2, 'B': 4, 'C': 6, 'D': 8}

costs: dict[str, int] = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

hallXPositions: list[int] = [0, 1, 3, 5, 7, 9, 10]


def IsComplete(state: AmphipodState) -> bool:
    dict = state.AsDict()
    for c in dict.keys():
        if Point(homeX[c], -2) not in dict[c] or Point(homeX[c], -1) not in dict[c]:
            return False
    return True


def Heuristic0(state: AmphipodState) -> float:
    return 0


def Heuristic(state: AmphipodState) -> float:
    """
    The heuristic cost is the shortest path of each amphipod to its home.
    """
    cost = 0
    for c, positions in state.AsDict().items():
        for i, position in enumerate(positions):
            # The home y positions are -2 and -1, so they are i - 2 since i will be 0 and 1.
            cost += ManhattanDistance(position,
                                      Point(homeX[c], i - 2)) * costs[c]
    return cost


def Cost(start: AmphipodState, end: AmphipodState) -> float:
    startPoints = start.AllPositions().difference(end.AllPositions())
    endPoints = end.AllPositions().difference(start.AllPositions())
    if len(startPoints) != 1 or len(endPoints) != 1:
        raise ValueError(
            "There can only be one amphipod in a different location between successive states.")
    startPoint = startPoints.pop()
    endPoint = endPoints.pop()
    startValue = start.AtPoint(startPoint)
    endValue = end.AtPoint(endPoint)
    if startValue is None:
        raise ValueError(f"Nothing found at {startPoint}.")
    if endValue is None:
        raise ValueError(f"Nothing found at {endPoint}.")
    if startValue != endValue:
        raise ValueError(
            f"Value at {startPoint} ({startValue}) doesn't match value at {endPoint} ({endValue}).")
    return ManhattanDistance(startPoint, endPoint) * costs[startValue]


def ReplacePosition(state: AmphipodState, c: str, x: int, y: int, i: int) -> AmphipodState:
    newState = state.AsDict()
    newState[c][i] = Point(x, y)
    newState[c].sort()
    return AmphipodState.FromDict(newState)


def MoveHome(state: AmphipodState, c: str, i: int, position: Point) -> Optional[AmphipodState]:
    """
    Given an amphipod in the hall, move it home if possible. This isn't iterable
    because there's only one possible move.
    """
    bottomPosition = state.AtPoint(Point(homeX[c], -2))
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
        topPosition = state.AtPoint(Point(homeX[c], -1))
        if topPosition:
            # There's something in the top position that is not a character at home.
            # We can't move here.
            return None
        targetY = -1
    for testX in range(position.x - 1, homeX[c], -1) if position.x > homeX[c] else range(position.x + 1, homeX[c]):
        # Look to see if there's something between here and the home position.
        if state.AtPoint(Point(testX, 0)):
            return None
    return ReplacePosition(state, c, homeX[c], targetY, i)


def MoveToHall(state: AmphipodState, c: str, i: int, position: Point) -> Iterable[Optional[AmphipodState]]:
    """
    Given an amphipod in a side room, return any hall positions it can move to.
    """
    if position == Point(homeX[c], -2):
        # If it's in the bottom slot, this amphipod is already home.
        return None
    if position == Point(homeX[c], -1):
        # If it's in the top slot, it's only home if the bottom is the same character.
        bottomChar = state.AtPoint(Point(homeX[c], -2))
        if bottomChar == c:
            return None
    if position.y == -2 and Point(position.x, -1) in state.AllPositions():
        # This amphipod is in the bottom slot of a room and the upper slot is occupied.
        return None
    # At this point we know the amphipod can get out of the room. Now we return all the
    # hallway positions it can reach.
    for testX in range(position.x - 1, -1, -1):
        # Look at the positions to the left.
        if Point(testX, 0) in state.AllPositions():
            # If we've encountered another amphipod in the hall, stop looking in this direction.
            break
        if testX in hallXPositions:
            yield ReplacePosition(state, c, testX, 0, i)
    for testX in range(position.x + 1, 11):
        # Look at the positions to the right.
        if Point(testX, 0) in state.AllPositions():
            # If we've encountered another amphipod in the hall, stop looking in this direction.
            break
        if testX in hallXPositions:
            yield ReplacePosition(state, c, testX, 0, i)


def Successors(state: AmphipodState) -> Iterable[AmphipodState]:
    # Find amphipods in side rooms that can move to the hall.
    dict = state.AsDict()
    for c in dict:
        for i, position in enumerate(dict[c]):
            if position.y == 0:
                newState = MoveHome(state, c, i, position)
                if newState is not None:
                    yield newState
            else:
                for s in MoveToHall(state, c, i, position):
                    if s:
                        yield s


def PrintAmphipodState(state: AmphipodState) -> None:
    print('#############')
    print('#', end='')
    for x in range(0, 11):
        c = state.AtPoint(Point(x, 0))
        print(c if c else '.', end='')
    print('#')
    # Third and fourth rows
    for y in range(-1, -3, -1):
        print('###' if y == -1 else '  #', end='')
        for x in range(2, 10, 2):
            c = state.AtPoint(Point(x, y))
            print(c if c else '.', end='')
            print('#', end='')
        print('##' if y == -1 else '')
    # Bottom row
    print('  #########\n')


def FindCost(lines: list[str], showSolution: bool = False) -> int:
    pods = AmphipodState.FromText(lines)
    solution = astar(pods, IsComplete, Successors, Heuristic, Cost)
    if solution is None:
        raise ValueError("No solution found.")
    previous = None
    if showSolution:
        for state in nodeToPath(solution):
            if previous:
                print(f"Cost: {Cost(previous, state)}")
            previous = state
            PrintAmphipodState(state)
    return int(solution.cost)


if __name__ == "__main__":
    part1 = FindCost(TEST.splitlines(), False)
    assert part1 == 12521

    with open("23.txt", "r") as infile:
        part1 = FindCost(infile.readlines(), False)
    # 18328 too high.
    # 18282 is correct. My initial Heuristic calculation was incorrect.
    # It needed the lists of points to be sorted.
    print(f"Part 1: {part1}")
