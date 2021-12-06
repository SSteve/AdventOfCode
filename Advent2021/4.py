from typing import Tuple

TEST = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


def LoadBoards(lines: list[str]) -> list[list[list[str]]]:
    i = 0
    boards: list[list[list[str]]] = []
    while i < len(lines):
        if len(lines[i].strip()) == 0:
            i += 1

        thisBoard: list[list[str]] = []
        for _ in range(5):
            x = lines[i].split()
            thisBoard.append(x)
            i += 1

        boards.append(thisBoard)
    return boards


def IsAWinningBoard(board: list[list[str]], calledNumbers: list[str]) -> bool:
    # Check rows
    if any(all(v in calledNumbers for v in row) for row in board):
        return True

    for i in range(5):
        if all(row[i] in calledNumbers for row in board):
            return True

    return False


def SumOfUnmarkedNumbers(board: list[list[str]], calledNumbers: list[str]) -> int:
    sum = 0
    for line in board:
        for number in line:
            if number not in calledNumbers:
                sum += int(number)
    return sum


def PlayBingo(lines: list[str]) -> Tuple[int, int]:
    scheduledNumbers = lines[0].split(",")
    boards = LoadBoards(lines[2:])
    calledNumbers: list[str] = []
    # The indices of the boards that have one. Once a board has won, we ignore it.
    winningBoards: set[int] = set()
    firstScore = -1

    for calledNumber in scheduledNumbers:
        calledNumbers.append(calledNumber)
        for inx, board in enumerate(boards):
            if inx not in winningBoards and IsAWinningBoard(board, calledNumbers):
                winningBoards.add(inx)
                if firstScore < 0:
                    unmarkedSum = SumOfUnmarkedNumbers(board, calledNumbers)
                    firstScore = unmarkedSum * int(calledNumbers[-1])
                if len(winningBoards) == len(boards):
                    # This was the last winning board.
                    unmarkedSum = SumOfUnmarkedNumbers(
                        board, calledNumbers)
                    secondScore = unmarkedSum * int(calledNumbers[-1])
                    return firstScore, secondScore
    return -1, -1


if __name__ == "__main__":
    firstBingoScore, lastBingoScore = PlayBingo(TEST.splitlines())
    assert firstBingoScore == 4512
    assert lastBingoScore == 1924

    with open("4.txt", "r") as infile:
        firstBingoScore, lastBingoScore = PlayBingo(infile.read().splitlines())
        print(f"Part 1: {firstBingoScore}")
        print(f"Part 2: {lastBingoScore}")
