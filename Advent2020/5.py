import math
from typing import Set

characterValues = {'F': 0, 'B': 1, 'L': 0, 'R': 1}


def seatId(code: str) -> int:
    id = 0
    for char in code:
        id = id * 2 + characterValues[char]
    return id

assert seatId('FBFBBFFRLR') == 357
assert seatId('BFFFBBFRRR') == 567
assert seatId('FFFBBBFRRR') == 119
assert seatId('BBFFBBFRLL') == 820

highest = -1
lowest = 1e10
seats: Set[int] = set()

with open("5.txt", "r") as infile:
    for boardingPassCode in infile.read().splitlines():
        id = seatId(boardingPassCode)
        lowest = min(lowest, id)
        highest = max(highest, id)
        # Add the id to the set of seats.
        seats.add(id)

print(f"Part 1: {highest}")

# Find the missing seat in the set of seats.
mySeat = lowest + 1
while mySeat in seats:
    mySeat += 1
print(f"My seat number: {mySeat}")

