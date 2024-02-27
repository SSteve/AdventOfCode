from dataclasses import dataclass

TEST = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


@dataclass
class AlmanacMap:
    destination_start: int
    source_start: int
    range: int


def find_closest_location(lines: list[str]) -> int:
    closest_location = float("inf")

    return closest_location


if __name__ == "__main__":
    part1test = find_closest_location(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 35

    with open("day5.txt") as infile:
        lines = infile.read().splitlines()

    part1 = find_closest_location(lines)
    print(f"Part 1: {part1}")
