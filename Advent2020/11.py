from typing import List

TEST = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


def OccupiedSeatsPart1(rowNum: int, colNum: int, seats: List[List[str]]) -> int:
    occupiedSeats = 0
    for row in range(rowNum - 1, rowNum + 2):
        if row >= 0 and row < len(seats):
            seatRow = seats[row]
            for col in range(colNum - 1, colNum + 2):
                if col >= 0 and col < len(seatRow) and seatRow[col] == '#' and\
                        not (col == colNum and row == rowNum):
                    occupiedSeats += 1
    return occupiedSeats


def OccupiedSeatsPart2(rowNum: int, colNum: int, seats: List[List[str]]) -> int:
    occupiedSeats = 0
    vectors = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    for vector in vectors:
        lookCol, lookRow = colNum + vector[0], rowNum + vector[1]
        while lookCol >= 0 and lookCol < len(seats[0]) \
                and lookRow >= 0 and lookRow < len(seats):
            cell = seats[lookRow][lookCol]
            if cell == 'L':
                break
            if cell == '#':
                occupiedSeats += 1
                break
            lookCol += vector[0]
            lookRow += vector[1]
    return occupiedSeats


def PrintSeats(seats: List[List[str]]) -> None:
    for row in seats:
        print(row)
    print()


def Day11(seats: List[List[str]], occupationLimit: int, counterFunc) -> int:
    changedSeats = -1
    while changedSeats != 0:
        newSeats = []
        changedSeats = 0
        for rowNum in range(len(seats)):
            row = seats[rowNum]
            newRow = ''
            for colNum in range(len(row)):
                seat = row[colNum]
                newSeat = seat
                if seat != '.':
                    occupied = counterFunc(rowNum, colNum, seats)
                    if seat == 'L' and occupied == 0:
                        newSeat = '#'
                    if seat == '#' and occupied >= occupationLimit:
                        newSeat = 'L'
                if newSeat != seat:
                    changedSeats += 1
                newRow += newSeat
            newSeats.append(newRow)
        seats = newSeats
        # PrintSeats(seats)

    return sum(row.count('#') for row in seats)


if __name__ == "__main__":
    testSeats = TEST.splitlines()
    assert Day11(testSeats, 4, OccupiedSeatsPart1) == 37
    assert Day11(testSeats, 5, OccupiedSeatsPart2) == 26

    with open("11.txt", "r") as infile:
        seats = infile.read().splitlines()
    print(f"Part 1: {Day11(seats, 4, OccupiedSeatsPart1)}")
    print(f"Part 2: {Day11(seats, 5, OccupiedSeatsPart2)}")