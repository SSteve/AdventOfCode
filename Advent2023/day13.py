TEST = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

TEST2 = """.##.#..#.##.###
####.#..#######
.##.##.#.######
#..#.#..#..#.##
.##.##.##.###..
..#.#.#.#.#.#..
....#.#..#.####"""


def vertical_reflection_value(pattern: list[str], y: int) -> int | None:
    # Determine if there is a reflection at y. If so, return the reflection value (100 times the
    # number of rows above the line of reflection).
    # y is the dividing line where we split the pattern. The lower part is rows 0 to y-1. The
    # upper part is y to len(pattern) - 1. Excess lines in the larger partition are ignored.

    # For the number of lines, use the smaller number of lines below or above the dividing line.
    number_of_lines = min(y, len(pattern) - y)
    for x in range(len(pattern[0])):
        lower_index = y - 1
        upper_index = y
        for _ in range(number_of_lines):
            if pattern[lower_index][x] != pattern[upper_index][x]:
                return None
            lower_index -= 1
            upper_index += 1

    # If we get here, all tests passed.
    return 100 * y


def horizontal_reflection_value(pattern: list[str], x: int) -> int | None:
    # Determine if there is a reflection at x. If so, return the reflection value (the
    # number of columns to the left of the line of reflection).
    # x is the dividing line where we split each line. The left part is characters 0 to x-1. The
    # right part is x to len(pattern[0]) - 1. Excess columns in the larger partition are ignored.

    # For the number of columns, use the smaller number of columns to the left or right of the dividing line.
    number_of_columns = min(x, len(pattern[0]) - x)
    for y in range(len(pattern)):
        left_index = x - 1
        right_index = x
        for _ in range(number_of_columns):
            if pattern[y][left_index] != pattern[y][right_index]:
                return None
            left_index -= 1
            right_index += 1

    # If we get here, all tests passed.
    return x


def calculate_pattern_value(pattern: list[str]) -> int:
    # Check horizontal lines first.
    for y in range(1, len(pattern)):
        if value := vertical_reflection_value(pattern, y):
            return value
    for x in range(1, len(pattern[0])):
        if value := horizontal_reflection_value(pattern, x):
            return value
    raise ValueError(f"Couldn't find a reflection.\n{"\n".join(pattern)}")


def calculate_reflections(lines: list[str]) -> int:
    patterns: list[list[str]] = []
    pattern: list[str] = []
    for line in lines:
        if line:
            pattern.append(line)
        else:
            patterns.append(pattern)
            pattern = []
    patterns.append(pattern)

    return sum(calculate_pattern_value(pattern) for pattern in patterns)


if __name__ == "__main__":
    x = calculate_pattern_value(TEST2.splitlines())
    assert x == 14

    part1test = calculate_reflections(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 405

    """ 
    part2test = calculate_reflections(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 1030
 """

    with open("day13.txt") as infile:
        lines = infile.read().splitlines()

    part1 = calculate_reflections(lines)
    print(f"Part 1: {part1}")
    # assert part1 == 9403026

    """ 
    part2 = calculate_reflections(lines)
    print(f"Part 2: {part2}")
 """
