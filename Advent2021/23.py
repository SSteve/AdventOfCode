
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Optional

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


AmphipodState = dict[str, list[Point]]

homeX: dict[str, int] = {'A': 2, 'B': 4, 'C': 6, 'D': 8}

costs: dict[str, int] = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

hallXPositions: list[int] = [0, 1, 3, 5, 7, 9, 10]


def IsComplete(state: AmphipodState) -> bool:
    for c in state.keys():
        if state[c][0] != Point(homeX[c], -2) or state[c][1] != Point(homeX[c], -1):
            return False
    return True


def Heuristic(state: AmphipodState) -> float:
    """
    The heuristic cost is the shortest path of each amphipod to its home.
    """
    cost = 0
    for c, positions in state.items():
        for i, position in enumerate(positions):
            # The home y positions are -2 and -1, so they are i - 2 since i will be 0 and 1.
            cost += ManhattanDistance(position,
                                      Point(homeX[c], i - 2)) * costs[c]
    return cost


def AllPositions(state: AmphipodState) -> set[Point]:
    allPositions: set[Point] = set()
    for values in state.values():
        allPositions.update(values)
    return allPositions


def AmphipodStateFromText(lines: list[str]) -> AmphipodState:
    state: AmphipodState = defaultdict(list[Point])
    for x in range(3, 11, 2):
        for y in range(2, 4):
            # Our origin is the first empty hallway space, so the amphipod
            # rooms are at x = 2, 4, 6, & 8 and y = -1 & -2
            state[lines[y][x]].append(Point(x - 1, -y + 1))
    for c in state:
        state[c].sort()
    return state


def AtPoint(state: AmphipodState, p: Point) -> Optional[str]:
    for c in state:
        if p in state[c]:
            return c
    return None


def Cost(start: AmphipodState, end: AmphipodState) -> float:
    startPoints = AllPositions(start).difference(AllPositions(end))
    endPoints = AllPositions(end).difference(AllPositions(start))
    if len(startPoints) != 1 or len(endPoints) != 1:
        raise ValueError(
            "There can only be one amphipod in a different location between successive states.")
    startPoint = startPoints.pop()
    endPoint = endPoints.pop()
    startValue = AtPoint(start, startPoint)
    endValue = AtPoint(end, endPoint)
    if startValue is None:
        raise ValueError(f"Nothing found at {startPoint}.")
    if endValue is None:
        raise ValueError(f"Nothing found at {endPoint}.")
    if startValue != endValue:
        raise ValueError(
            f"Value at {startPoint} ({startValue}) doesn't match value at {endPoint} ({endValue}).")
    return ManhattanDistance(startPoint, endPoint) * costs[startValue]


def ReplacePosition(oldState: AmphipodState, c: str, x: int, i: int) -> AmphipodState:
    newState = oldState.copy()
    positions = newState[c][:]
    positions[i] = Point(x, 0)
    positions.sort()
    newState[c] = positions
    return newState


def MoveToHall(state: AmphipodState, c: str, i: int, position: Point) -> Iterable[Optional[AmphipodState]]:
    """
    Given an amphipod in a side room, return any hall positions it can move to.
    """
    if position == Point(homeX[c], -2):
        # If it's in the bottom slot, this amphipod is already home.
        return None
    if position == Point(homeX[c], -1):
        # If it's in the top slot, it's only home if the bottom is the same character.
        bottomChar = AtPoint(state, Point(homeX[c], -2))
        if bottomChar == c:
            return None
    if position.y == -2 and Point(position.x, -1) in AllPositions(state):
        # This amphipod is in the bottom slot of a room and the upper slot is occupied.
        return None
    # At this point we know the amphipod can get out of the room. Now we return all the
    # hallway positions it can reach.
    for testX in range(position.x - 1, -1, -1):
        # Look at the positions to the left.
        if Point(testX, 0) in AllPositions(state):
            # If we've encountered another amphipod in the hall, stop looking in this direction.
            break
        if testX in hallXPositions:
            yield ReplacePosition(state, c, testX, i)
    for testX in range(position.x + 1, 11):
        # Look at the positions to the right.
        if Point(testX, 0) in AllPositions(state):
            # If we've encountered another amphipod in the hall, stop looking in this direction.
            break
        if testX in hallXPositions:
            yield ReplacePosition(state, c, testX, i)


def MoveHome(state: AmphipodState, c: str, i: int, position: Point) -> Iterable[Optional[AmphipodState]]:
    """
    Given an amphipod in the hall, move it home if possible.
    """
    if AtPoint(state, Point(homeX[c], -2)) != c:
        return None


def Successors(state: AmphipodState) -> Iterable[AmphipodState]:
    # Find amphipods in side rooms that can move to the hall.
    for c in state:
        for i, position in enumerate(state[c]):
            if position.y == 0:
                continue
            else:
                for s in MoveToHall(state, c, i, position):
                    if s:
                        yield s


def PrintAmphipodState(state: AmphipodState) -> None:
    print('#############')
    print('#', end='')
    for x in range(0, 11):
        c = AtPoint(state, Point(x, 0))
        print(c if c else '.', end='')
    print('#')
    # Third and fourth rows
    for y in range(-1, -3, -1):
        print('###' if y == -1 else '  #', end='')
        for x in range(2, 10, 2):
            c = AtPoint(state, Point(x, y))
            print(c if c else '.', end='')
            print('#', end='')
        print('##' if y == -1 else '')
    # Bottom row
    print('  #########\n')


if __name__ == "__main__":
    pods = AmphipodStateFromText(TEST.splitlines())
    PrintAmphipodState(pods)
    previous = pods
    for s in Successors(pods):
        print(f"Cost: {Cost(previous, s)}")
        PrintAmphipodState(s)
    print("\n\n\nNext\n\n\n")
    i = 0
    previous = s
    for t in Successors(s):
        i += 1
        if i == 13:
            u = t
        print(f"Cost: {Cost(previous, t)}")
        PrintAmphipodState(t)

    print("\n\n\nNext\n\n\n")
    previous = u
    for v in Successors(u):
        print(f"Cost: {Cost(previous, v)}")
        PrintAmphipodState(v)
