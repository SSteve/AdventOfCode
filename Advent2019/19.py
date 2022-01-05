from typing import Tuple

from intcode import IntCode


def Part1(program: str, show: bool = False) -> int:
    total = 0
    for y in range(50):
        for x in range(50):
            computer = IntCode(program, input_queue=[x, y], interactive=False)
            computer.run()
            result = computer.output_values.pop()
            total += result
            if show:
                print('#' if result else '.', end="")
        if show:
            print()
    return total


def Part2(program: str) -> int:
    # Keep track of the starting position and width of each row. The
    # key is the row number and the value is the starting position
    # and width.
    # When we ran part 1, the last complete row we saw was row 35.
    # It started at x = 39 and was 10 characters wide.
    rowStats: dict[int, Tuple[int, int]] = {35: (39, 10)}
    y = 35
    firstX = 39
    result = -1
    width = 10

    while result < 0:
        y += 1
        x = firstX - 1
        firstX = -1
        affectedByTractor = 0
        while True:
            # Find the start and width of this row.
            x += 1
            computer = IntCode(program, input_queue=[x, y], interactive=False)
            computer.run()
            affectedByTractor = computer.output_values.pop()
            if firstX < 0 and affectedByTractor:
                firstX = x
                # Each row is at least as wide as the previous so we can skip
                # the locations we know are affected.
                x += width - 1
            elif firstX > 0 and not affectedByTractor:
                width = x - firstX
                rowStats[y] = (firstX, width)
                break
        if width >= 100:
            topRowStat = rowStats[y-99]
            if topRowStat[0] + topRowStat[1] >= firstX + 100:
                result = firstX * 10000 + y - 99

    return result


if __name__ == '__main__':
    with open("19.txt") as infile:
        program = infile.readline()
    # part1 = Part1(program, False)
    # print(f"Part 1: {part1}")

    part2 = Part2(program)
    # 721428 is too low
    print(f"Part 2: {part2}")
