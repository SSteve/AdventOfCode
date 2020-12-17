import re
from enum import Enum
from typing import DefaultDict, Dict, List, Tuple

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

TEST2 = """departure date: 33-862 or 883-964
departure time: 35-716 or 722-971
arrival location: 32-59 or 74-955
arrival station: 41-330 or 353-963

your ticket:
40,400,100,100

nearby tickets:
50,400,100,30
863,864,800,880
718,721,717,900
900,60,73,331,61
333,200,340,344"""


def ReadData(lines: List[str]) -> Tuple[List[Field], List[int], List[List[int]]]:
    fields: List[Field] = []
    myTicket: List[int] = []
    nearbyTickets: List[List[int]] = []
    readState = ReadState.FIELDS
    for line in lines:
        if readState == ReadState.FIELDS:
            if match := fieldRegex.match(line):
                fields.append(Field(match[1], int(match[2]), int(match[3]), int(match[4]), int(match[5])))
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
    return (fields, myTicket, nearbyTickets)


def Part1(fields: List[Field], nearbyTickets: List[List[int]]) -> int:
    scanningErrorRate = 0
    for ticket in nearbyTickets:
        for ticketValue in ticket:
            if not any(field.ValueIsValid(ticketValue) for field in fields):
                scanningErrorRate += ticketValue

    return scanningErrorRate


def DiscardInvalid(fields: List[Field], nearbyTickets: List[List[int]]) -> List[List[int]]:
    valid: List[List[int]] = []
    for ticket in nearbyTickets:
        if all(any(field.ValueIsValid(ticketValue) for field in fields) for ticketValue in ticket):
            valid.append(ticket)
    return valid


def Part2(fields: List[Field], myTicket: List[int], nearbyTickets: List[List[int]]) -> int:
    validTickets = DiscardInvalid(fields, nearbyTickets)

    # There's a lot of overlap between valid values so some values at a given index
    # may be valid for multiple fields. Find all the potential value indexes for
    # each field.
    potentials = DefaultDict(set)
    for valueIndex in range(len(validTickets[0])):
        for fieldIndex in range(len(fields)):
            if all(fields[fieldIndex].ValueIsValid(ticket[valueIndex]) for ticket in validTickets):
                # This value index is valid for all fields, so add it to the list of
                # potential value indexes for this field.
                potentials[fieldIndex].add(valueIndex)

    # Now we need to go through the potentials and find the fields that have only
    # one potential value index. When we find one, we add that mapping to fieldMap
    # and remove that value index from all the other potentials for each field index.
    fieldMap: Dict[int, int] = {}
    while len(fieldMap) < len(fields):
        foundIndex = -1
        for fieldIndex in potentials:
            if len(potentials[fieldIndex]) == 1:
                # This valueIndex must be this field.
                foundIndex = fieldIndex
                break
        assert foundIndex > -1, "Didn't find a potential with len == 1."
        valueIndex = potentials[foundIndex].pop()
        fieldMap[valueIndex] = foundIndex
        # This value is mapped so remove it as a potential for mapping
        # to any other field.
        for fieldIndex in potentials:
            potentials[fieldIndex].discard(valueIndex)

    # look for the six fields on your ticket that start with the word departure.
    # What do you get if you multiply those six values together?
    part2 = 1
    for valueIndex in range(len(myTicket)):
        fieldName = fields[fieldMap[valueIndex]].name
        if fieldName.find("departure") == 0:
            part2 *= myTicket[valueIndex]
    return part2


if __name__ == "__main__":
    part1Data = ReadData(TEST.splitlines())
    part1Test = Part1(part1Data[0], part1Data[2])
    assert part1Test == 71, f"{part1Test=}. Should be 71."

    part2Data = ReadData(TEST2.splitlines())
    part2Test = Part2(*part2Data)
    assert part2Test == 100 * 100, f"{part2Test=}. Should be {100 * 100}."

    with open("16.txt", "r") as infile:
        data = ReadData(infile.read().splitlines())

    part1 = Part1(data[0], data[2])
    print(f"Part 1: {part1}")
    assert part1 == 23044, f"{part1=}. Should be 23044."

    part2 = Part2(*data)
    print(f"Part 2: {part2}")
    assert part2 == 3765150732757, f"{part2=}. Should be 3765150732757."
