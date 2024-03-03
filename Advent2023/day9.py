TEST = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def extrapolation(line: str) -> int:
    values = list(map(int, line.split()))
    final_value = 0

    while any(v != 0 for v in values):
        final_value += values[-1]
        values = [values[i] - values[i - 1] for i in range(1, len(values))]

    return final_value


def sum_of_extrapolations(lines: list[str]) -> int:
    extrapolation_sum = sum(extrapolation(line) for line in lines)

    return extrapolation_sum


def left_extrapolation(line: str) -> int:
    values = list(map(int, line.split()))
    final_values: list[int] = []

    while any(v != 0 for v in values):
        final_values.append(values[0])
        values = [values[i] - values[i - 1] for i in range(1, len(values))]

    difference = 0
    while final_values:
        difference = final_values.pop() - difference

    return difference


def sum_of_left_extrapolations(lines: list[str]) -> int:
    extrapolation_sum = sum(left_extrapolation(line) for line in lines)

    return extrapolation_sum


if __name__ == "__main__":
    part1test = sum_of_extrapolations(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 114

    part2test = sum_of_left_extrapolations(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 2

    with open("day9.txt") as infile:
        lines = infile.read().splitlines()

    part1 = sum_of_extrapolations(lines)
    print(f"Part 1: {part1}")
    assert part1 == 1789635132

    part2 = sum_of_left_extrapolations(lines)
    print(f"Part 2: {part2}")
