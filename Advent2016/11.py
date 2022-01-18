from __future__ import annotations
from itertools import combinations
from datetime import datetime
from typing import Collection, Iterable

from generic_search import bfs, nodeToPath

TEST2 = """The first floor contains nothing relevant.
The second floor contains nothing relevant.
The third floor contains nothing relevant.
The fourth floor contains a hydrogen-compatible microchip, a hydrogen generator, a "+ \
    "lithium generator, and a lithium-compatible microchip."""

TEST1 = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""


class Floor:
    def __init__(self, microchips: Collection[str], generators: Collection[str]) -> None:
        self.microchips: frozenset[str] = frozenset(microchips)
        self.generators: frozenset[str] = frozenset(generators)

    @classmethod
    def FromString(cls, line: str) -> Floor:
        words = line.replace('.', '').replace(',', '').split()
        microchips: set[str] = set()
        generators: set[str] = set()
        for i, word in enumerate(words):
            if word == 'microchip':
                microchips.add(words[i-1].split('-')[0])
            elif word == 'generator':
                generators.add(words[i-1])
        return cls(microchips, generators)

    def __hash__(self) -> int:
        return hash((self.microchips, self.generators))

    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        other: Floor = __o  # type: ignore
        return self.microchips == other.microchips and self.generators == other.generators

    def __repr__(self) -> str:
        return f"   microchips: {', '.join(self.microchips)}\n   generators: {', '.join(self.generators)}"

    def CanAddMicrochips(self, microchips: Collection[str]) -> bool:
        return Floor.StateIsLegal(self.microchips.union(microchips), self.generators)

    def AddMicrochips(self, microchips: Collection[str]) -> Floor:
        return Floor(self.microchips.union(microchips), self.generators)

    def CanRemoveMicrochips(self, microchips: Collection[str]) -> bool:
        return Floor.StateIsLegal(self.microchips.difference(microchips), self.generators)

    def RemoveMicrochips(self, microchips: Collection[str]) -> Floor:
        return Floor(self.microchips.difference(microchips), self.generators)

    def CanAddGenerators(self, generators: Collection[str]) -> bool:
        return Floor.StateIsLegal(self.microchips, self.generators.union(generators))

    def AddGenerators(self, generators: Collection[str]) -> Floor:
        return Floor(self.microchips, self.generators.union(generators))

    def CanRemoveGenerators(self, generators: Collection[str]) -> bool:
        return Floor.StateIsLegal(self.microchips, self.generators.difference(generators))

    def RemoveGenerators(self, generators: Collection[str]) -> Floor:
        return Floor(self.microchips, self.generators.difference(generators))

    @staticmethod
    def StateIsLegal(microchips: frozenset[str], generators: frozenset[str]) -> bool:
        # If there are any microchips not paired with their generator when there
        # are other generators, the state is not legal.
        return len(generators) == 0 or not(microchips - generators)


class Facility:
    def __init__(self, floors: list[Floor], currentFloor: int) -> None:
        self.floors = tuple(floors)
        self.currentFloor = currentFloor

    @classmethod
    def FromStrings(cls, lines: list[str]) -> Facility:
        floors = [Floor.FromString(line) for line in lines]
        return cls(floors, 0)

    def __hash__(self) -> int:
        return hash((self.floors, self.currentFloor))

    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        other: Facility = __o  # type: ignore
        if self.currentFloor != other.currentFloor:
            return False
        for i, floor in enumerate(self.floors):
            if floor != other.floors[i]:
                return False
        return True

    def __repr__(self) -> str:
        result = ""
        for i, floor in enumerate(self.floors):
            result += f"Floor {i + 1}:"
            if i == self.currentFloor:
                result += " <- current"
            result += '\n'
            result += f"{floor}\n"
        return result[:-1]

    def ReadyForAssembly(self) -> bool:
        return all(len(floor.microchips) == 0 and len(floor.generators) == 0 for floor in self.floors[:-1])

    def MoveMicrochips(self, microchips: Collection[str], fromFloor: int, toFloor: int) -> Facility:
        newFloors = list(self.floors)
        newFloors[toFloor] = newFloors[toFloor].AddMicrochips(microchips)
        newFloors[fromFloor] = newFloors[fromFloor].RemoveMicrochips(
            microchips)
        return Facility(newFloors, toFloor)

    def MoveGenerators(self, generators: Collection[str], fromFloor: int, toFloor: int) -> Facility:
        newFloors = list(self.floors)
        newFloors[toFloor] = newFloors[toFloor].AddGenerators(generators)
        newFloors[fromFloor] = newFloors[fromFloor].RemoveGenerators(
            generators)
        return Facility(newFloors, toFloor)

    def MovePair(self, element: str, fromFloor: int, toFloor: int) -> Facility:
        newFloors = list(self.floors)
        newFloors[toFloor] = newFloors[toFloor].AddGenerators([element])
        newFloors[fromFloor] = newFloors[fromFloor].RemoveGenerators(
            [element])
        newFloors[toFloor] = newFloors[toFloor].AddMicrochips([element])
        newFloors[fromFloor] = newFloors[fromFloor].RemoveMicrochips(
            [element])
        return Facility(newFloors, toFloor)

    def Successors(self) -> Iterable[Facility]:
        floor = self.floors[self.currentFloor]
        i = self.currentFloor
        for count in range(1, 3):
            for microchips in combinations(floor.microchips, count):
                if not floor.CanRemoveMicrochips(microchips):
                    # This microchip combination can't be moved from this floor.
                    continue
                if i > 0:
                    if self.floors[i - 1].CanAddMicrochips(microchips):
                        yield self.MoveMicrochips(microchips, i, i-1)
                if i + 1 < len(self.floors):
                    if self.floors[i + 1].CanAddMicrochips(microchips):
                        yield self.MoveMicrochips(microchips, i, i+1)
            for generators in combinations(floor.generators, count):
                if not floor.CanRemoveGenerators(generators):
                    # This Generator combination can't be moved from this floor.
                    continue
                if i > 0:
                    if self.floors[i - 1].CanAddGenerators(generators):
                        yield self.MoveGenerators(generators, i, i-1)
                if i + 1 < len(self.floors):
                    if self.floors[i + 1].CanAddGenerators(generators):
                        yield self.MoveGenerators(generators, i, i+1)
        # Move matching pairs.
        for microchip in floor.microchips:
            if microchip in floor.generators:
                if i > 0:
                    if self.floors[i-1].CanAddGenerators(frozenset([microchip])):
                        yield self.MovePair(microchip, i, i-1)
                if i+1 < len(self.floors):
                    if self.floors[i+1].CanAddGenerators(frozenset([microchip])):
                        yield self.MovePair(microchip, i, i+1)


if __name__ == '__main__':
    facility = Facility.FromStrings(TEST1.splitlines())
    """
    print(facility)
    for successor in facility.Successors():
        print(successor, '\n\n')
    """
    solution = bfs(facility, Facility.ReadyForAssembly, Facility.Successors)
    assert solution and len(nodeToPath(solution)) - 1 == 11

    with open('11.txt', 'r') as infile:
        facility = Facility.FromStrings(infile.read().splitlines())

    newFirstFloor = facility.floors[0].AddMicrochips(
        ['elerium', 'dilithium']).AddGenerators(['elerium', 'dilithium'])
    newFloors = [newFirstFloor, *facility.floors[1:]]
    newFacility = Facility(newFloors, 0)

    solution = bfs(facility, Facility.ReadyForAssembly, Facility.Successors)
    if solution is None:
        print("No solution found for part 1.")
    else:
        part1 = len(nodeToPath(solution)) - 1
        print(f"Part 1: {part1}")

    solution = bfs(newFacility, Facility.ReadyForAssembly, Facility.Successors)
    if solution is None:
        print("No solution found for part 2.")
    else:
        part2 = len(nodeToPath(solution)) - 1
        print(f"Part 2: {part2}")
