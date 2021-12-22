""" I cribbed part 2 from https://github.com/mebeim/aoc/blob/master/2021/README.md#day-21---dirac-dice"""
from functools import lru_cache
from itertools import product
from typing import Tuple

TEST = """Player 1 starting position: 4
Player 2 starting position: 8"""


def GetStartingPositions(lines: list[str]) -> list[int]:
    """ Get the starting positions for the players, converted to the range 0-9"""
    p1 = int(lines[0].split()[-1]) - 1
    p2 = int(lines[1].split()[-1]) - 1
    return [p1, p2]


def Part1(lines: list[str]) -> int:
    positions = GetStartingPositions(lines)
    scores = [0, 0]
    turn = 0
    lastRoll = -1
    while max(scores) < 1000:
        rollValue = 0
        for _ in range(3):
            lastRoll = (lastRoll + 1) % 100
            # We're mapping 0-99 to 1-100 so add 1 to our value to get the die's value.
            rollValue += lastRoll + 1
        player = turn & 1
        positions[player] = (positions[player] + rollValue) % 10
        score = positions[player] + 1
        scores[player] += score
        turn += 1
    return min(scores) * turn * 3


QUANTUM_ROLLS = tuple(map(sum, product(range(1, 4), range(1, 4), range(1, 4))))


@lru_cache(maxsize=None)
def Part2Round(myPosition: int, myScore: int, otherPosition: int, otherScore: int) -> Tuple[int, int]:
    if myScore >= 21:
        return (1, 0)
    if otherScore >= 21:
        return (0, 1)

    myWins = 0
    otherWins = 0

    for roll in QUANTUM_ROLLS:
        newPosition = (myPosition + roll) % 10
        newScore = myScore + newPosition + 1

        # Let the other player play, swapping the arguments.
        ow, mw = Part2Round(otherPosition, otherScore, newPosition, newScore)

        # Update total wins of each player:
        myWins += mw
        otherWins += ow

    return myWins, otherWins


def Part2(lines: list[str]) -> int:
    positions = GetStartingPositions(lines)
    wins = Part2Round(positions[0], 0, positions[1], 0)
    return max(wins)


if __name__ == "__main__":
    part1 = Part1(TEST.splitlines())
    assert part1 == 739785
    part2 = Part2(TEST.splitlines())
    assert part2 == 444356092776315

    with open("21.txt", "r") as infile:
        lines = infile.readlines()
    part1 = Part1(lines)
    print(f"Part 1: {part1}")
    part2 = Part2(lines)
    print(f"Part 2: {part2}")
