import math

def partition(values: str, width: int, lowSplit: str, highSplit: str) -> int:
    low = 0
    high = width - 1
    for char in values:
        if char == lowSplit:
            high -= (high - low + 1) // 2
        else:
            low += (high - low + 1) // 2
    return low

def seatId(code: str) -> int:
    return partition(code[:7], 128, 'F', 'R') * 8 + partition(code[7:], 8, 'L', 'R')
    
    
assert seatId('FBFBBFFRLR') == 357
assert seatId('BFFFBBFRRR') == 567
assert seatId('FFFBBBFRRR') == 119
assert seatId('BBFFBBFRLL') == 820

highest = 0
lowest = 1e10
seats = set()
with open("5.txt", "r") as infile:
    for boardingPassCode in infile.read().splitlines():
        id = seatId(boardingPassCode)
        lowest = min(lowest, id)
        highest = max(highest, id)
        seats.add(id)

print(f"Part 1: {highest}")

mySeat = lowest + 1
while mySeat in seats:
    mySeat += 1
print(f"My seat number: {mySeat}")

