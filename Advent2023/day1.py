import re

TEST = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

TEST2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

def sum_calibrations(lines: list[str]) -> int:
    sum = 0
    for line in lines:
        for c in line:
            # Look through the string and find the first numeral.
            if c.isdigit():
                sum += int(c) * 10
                break

        # Look the the string backward and find the first numeral.
        for c in reversed(line):
            if c.isdigit():
                sum += int(c)
                break

    return sum

def get_value(value: str) -> int:
    

def sum_calibrations2(lines: list[str]) -> int:
    values: dict[str, int] = {}
    values["one"] = 1

    numberRegex = re.compile(r"one|two|three|four|five|six|seven|eight|nine|[1-9]")
    sum = 0

    for line in lines:
        match = numberRegex.findall(line)
        print(f"first: {match[0]}, second: {match[-1]}")

    return sum

if __name__ == "__main__":
    part1test = sum_calibrations(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert (part1test == 142)

    part2test = sum_calibrations2(TEST2.splitlines())
    print(f"Part 2 test: {part2test}")
    assert (part2test == 281)


    with open("day1.txt") as infile:
        lines = infile.read().splitlines()

    part1 = sum_calibrations(lines)
    print(f"Part 1: {part1}")

    part2 = sum_calibrations2(lines)
    print(f"Part 2: {part2}")
