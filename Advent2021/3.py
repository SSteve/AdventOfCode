from typing import Tuple


def CountOnes(lines: list[str], position: int) -> int:
    count = 0
    for line in lines:
        if line[position] == "1":
            count += 1
    return count


def ConvertBinary(line: str) -> int:
    power = len(line) - 1
    result = 0
    for position in range(len(line)):
        if line[position] == "1":
            result += 2 ** power
        power -= 1
    return result


def CalcGammaEpsilon(lines: list[str]) -> Tuple[int, int]:
    gamma = 0
    epsilon = 0
    power = len(lines[0]) - 1
    position = 0

    for position in range(len(lines[0])):
        count = CountOnes(lines, position)
        if count > len(lines) / 2:
            gamma += 2 ** power
        else:
            epsilon += 2 ** power
        power -= 1
        position += 1

    return gamma, epsilon


def CalcLifeSupportRating(lines: list[str]) -> int:
    O2Lines = lines[:]
    position = 0
    while (len(O2Lines) != 1):
        count = CountOnes(O2Lines, position)
        if count >= len(O2Lines) / 2:
            keepValue = "1"
        else:
            keepValue = "0"

        newO2Lines: list[str] = []
        for line in O2Lines:
            if line[position] == keepValue:
                newO2Lines.append(line)
        O2Lines = newO2Lines
        position += 1
    O2Rating = ConvertBinary(O2Lines[0])

    CO2Lines = lines[:]
    position = 0
    while (len(CO2Lines) != 1):
        count = CountOnes(CO2Lines, position)
        if count < len(CO2Lines) / 2:
            keepValue = "1"
        else:
            keepValue = "0"

        newCO2Lines: list[str] = []
        for line in CO2Lines:
            if line[position] == keepValue:
                newCO2Lines.append(line)
        CO2Lines = newCO2Lines
        position += 1
    CO2Rating = ConvertBinary(CO2Lines[0])

    return O2Rating * CO2Rating


TEST = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

if __name__ == "__main__":
    gamma, epsilon = CalcGammaEpsilon(TEST.splitlines())
    assert gamma * epsilon == 198

    with open("3.txt", "r") as infile:
        gamma, epsilon = CalcGammaEpsilon(infile.read().splitlines())
    assert gamma == 2484 and epsilon == 1611
    print(f"Part 1: {gamma} * {epsilon} = {gamma * epsilon}")

    lifeSupportRating = CalcLifeSupportRating(TEST.splitlines())
    assert lifeSupportRating == 230

    with open("3.txt", "r") as infile:
        lifeSupportRating = CalcLifeSupportRating(infile.read().splitlines())
    print(f"Part 2: {lifeSupportRating}")
