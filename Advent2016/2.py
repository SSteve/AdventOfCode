from typing import Tuple

offsets: dict[str, Tuple[int, int]] = {
    'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}


def FollowInstructions1(instructions: list[str]) -> str:
    keys: dict[Tuple[int, int], str] = {(-1, 1): '1', (0, 1): '2', (1, 1): '3', (-1, 0): '4', (0, 0): '5',
                                        (1, 0): '6', (-1, -1): '7', (0, -1): '8', (1, -1): '9'}
    result = ''
    positionX, positionY = 0, 0
    for instruction in instructions:
        for ch in instruction:
            positionX = min(1, max(-1, positionX + offsets[ch][0]))
            positionY = min(1, max(-1, positionY + offsets[ch][1]))
        result += keys[(positionX, positionY)]
    return result


def FollowInstructions2(instructions: list[str]) -> str:
    """
        1
      2 3 4
    5 6 7 8 9
      A B C
        D
    """
    keys: dict[Tuple[int, int], str] = {(0, 2): '1', (-1, 1): '2', (0, 1): '3', (1, 1): '4',
                                        (-2, 0): '5', (-1, 0): '6', (0, 0): '7', (1, 0): '8', (2, 0): '9',
                                        (-1, -1): 'A', (0, -1): 'B', (1, -1): 'C', (0, -2): 'D'}
    result = ''
    positionX, positionY = -2, 0
    for instruction in instructions:
        for ch in instruction:
            newX = positionX + offsets[ch][0]
            newY = positionY + offsets[ch][1]
            if (newX, newY) in keys:
                positionX, positionY = newX, newY
        result += keys[(positionX, positionY)]
    return result


TEST = """ULL
RRDDD
LURDL
UUUUD"""

if __name__ == '__main__':
    part1 = FollowInstructions1(TEST.splitlines())
    assert part1 == '1985'

    part2 = FollowInstructions2(TEST.splitlines())
    assert part2 == '5DB3'

    with open('2.txt', 'r') as infile:
        instructions = infile.read().splitlines()
    part1 = FollowInstructions1(instructions)
    print(f"Part 1: {part1}")

    part2 = FollowInstructions2(instructions)
    print(f"Part 2: {part2}")
