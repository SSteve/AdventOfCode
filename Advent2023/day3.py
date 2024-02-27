from dataclasses import dataclass
from math import prod
from typing import Self

TEST = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


@dataclass
class Point:
    x: int
    y: int

    def is_neighbor(self, other: Self) -> bool:
        return other.x - 1 <= self.x <= other.x + 1 and other.y - 1 <= self.y <= other.y + 1


@dataclass
class SymbolLocation:
    location: Point
    symbol: str


@dataclass
class NumberLocation:
    number: int
    locations: list[int]


def find_symbols(y: int, line: str) -> list[SymbolLocation]:
    symbols = []

    for x, character in enumerate(line):
        if character != "." and character.isdigit() is False:
            symbols.append(SymbolLocation(Point(x, y), character))

    return symbols


def point_is_adjacent_to_symbol(point: Point, symbol_locations: list[list[SymbolLocation]]) -> int:
    for y in range(max(point.y - 1, 0), min(len(symbol_locations), point.y + 2)):
        for symbol_location in symbol_locations[y]:
            if point.is_neighbor(symbol_location.location):
                return True
    return False


def sum_of_part_numbers(lines: list[str]) -> tuple[int, list[list[SymbolLocation]], list[list[NumberLocation]]]:
    sum = 0

    # First find the coordinates of all the symbols.
    symbol_locations = [find_symbols(line_number, line) for line_number, line in enumerate(lines)]

    number_locations: list[list[NumberLocation]] = []
    number_locations_in_line: list[NumberLocation]
    numeral_locations: list[int]

    # Now look for the numbers.
    for y, line in enumerate(lines):
        in_number = False
        number_adjacent_to_symbol = False
        number = 0
        number_locations_in_line = []
        numeral_locations = []
        for x, c in enumerate(line):
            if c.isdigit():
                in_number = True
                number = number * 10 + int(c)
                numeral_locations.append(x)
                number_adjacent_to_symbol = number_adjacent_to_symbol or point_is_adjacent_to_symbol(Point(x, y), symbol_locations)
            elif in_number:
                # Character isn't a numeral so we've exited this number.
                if number_adjacent_to_symbol:
                    sum += number
                    number_locations_in_line.append(NumberLocation(number, numeral_locations))
                in_number = False
                number_adjacent_to_symbol = False
                number = 0
                numeral_locations = []
        if in_number and number_adjacent_to_symbol:
            # We were in a number when we reached the end of the line so the number is finished.
            sum += number
            number_locations_in_line.append(NumberLocation(number, numeral_locations))
        number_locations.append(number_locations_in_line)

    return sum, symbol_locations, number_locations


def find_adjacent_numbers(point: Point, locations: list[list[NumberLocation]]) -> list[int]:
    adjacent_numbers: list[int] = []

    for line in locations:
        for number_location in line:
            # Test that the right edge of this number and left edge of this number are within one location
            # of the point we're testing.
            if number_location.locations[-1] >= point.x - 1 and number_location.locations[0] <= point.x + 1:
                # If so, this number is adjacent.
                adjacent_numbers.append(number_location.number)
    return adjacent_numbers


def gear_ratio(symbol_locations: list[list[SymbolLocation]], number_locations: list[list[NumberLocation]]) -> int:
    ratio = 0
    for y, symbol_line in enumerate(symbol_locations):
        for symbol_location in symbol_line:
            if symbol_location.symbol != "*":
                continue
            # Find adjacent numbers in the lines above, at, and below the line this symbol is on.
            adjacent_numbers = find_adjacent_numbers(
                symbol_location.location, number_locations[max(y - 1, 0) : min(y + 2, len(number_locations))]
            )
            # If there are exactly two numbers, add their product to the total.
            if len(adjacent_numbers) == 2:
                ratio += prod(adjacent_numbers)

    return ratio


if __name__ == "__main__":
    part1test, symbol_locations, number_locations = sum_of_part_numbers(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 4361

    part2test = gear_ratio(symbol_locations, number_locations)
    print(f"Part 2 test: {part2test}")
    assert part2test == 467835

    with open("day3.txt") as infile:
        lines = infile.read().splitlines()

    part1, symbol_locations, number_locations = sum_of_part_numbers(lines)
    print(f"Part 1: {part1}")
    assert part1 == 551094

    part2 = gear_ratio(symbol_locations, number_locations)
    print(f"Part 2: {part2}")
