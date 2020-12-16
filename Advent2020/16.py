import re
from enum import Enum
from typing import List, Set

fieldRegex = re.compile(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)")
ticketStartRegex = re.compile(r"(\d+),")


class Field:
    def __init__(self, name: str, low1: int, high1: int, low2: int, high2: int) -> None:
        self.name = name
        self.range1 = range(low1, high1 + 1)
        self.range2 = range(low2, high2 + 1)

    def ValueIsValid(self, value: int):
        return value in self.range1 or value in self.range2


class ReadState(Enum):
    FIELDS = 1
    MY_TICKET = 2
    NEARBY_TICKETS = 3


TEST = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""


def Part1(lines: List[str]) -> int:
    fields: Set[Field] = set()
    myTicket: List[int]
    nearbyTickets: List[List[int]] = []
    readState = ReadState.FIELDS
    for line in lines:
        if readState == ReadState.FIELDS:
            if match := fieldRegex.match(line):
                fields.add(Field(match[1], int(match[2]), int(match[3]), int(match[4]), int(match[5])))
            else:
                readState = ReadState.MY_TICKET
        elif readState == ReadState.MY_TICKET:
            if ticketStartRegex.match(line):
                # If the line starts with a number and a comma, this is my ticket
                myTicket = [int(n) for n in line.split(',')]
                readState = ReadState.NEARBY_TICKETS
        elif readState == ReadState.NEARBY_TICKETS:
            if ticketStartRegex.match(line):
                nearbyTickets.append([int(n) for n in line.split(',')])

    scanningErrorRate = 0
    for ticket in nearbyTickets:
        for ticketValue in ticket:
            if not any(field.ValueIsValid(ticketValue) for field in fields):
                scanningErrorRate += ticketValue

    return scanningErrorRate


if __name__ == "__main__":
    part1Test = Part1(TEST.splitlines())
    assert part1Test == 71, f"{part1Test=}. Should be 71."

    with open("16.txt", "r") as infile:
        part1 = Part1(infile.read().splitlines())
    print(f"Part 1: {part1}")
