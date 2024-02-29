from dataclasses import dataclass
from typing import Self

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
class AlmanacLine:
    destination_start: int
    source_start: int
    range: int

    @staticmethod
    def from_line(line: str) -> Self:
        d, s, r = (int(num) for num in line.split())
        return AlmanacLine(d, s, r)

    def value_in_range(self, value: int) -> bool:
        return self.source_start <= value < self.source_start + self.range

    def process_value(self, value: int) -> int:
        return value - self.source_start + self.destination_start


type AlmanacMap = list[AlmanacLine]


def read_maps(lines: list[str]) -> list[AlmanacMap]:
    maps: list[AlmanacMap] = []
    map: AlmanacMap = []

    for line in lines:
        if len(line.strip()) == 0:
            maps.append(map)
            map = []
            continue
        if "map" in line:
            continue
        map.append(AlmanacLine.from_line(line))
    maps.append(map)

    return maps


def process_map(input: int, map: AlmanacMap) -> int:
    for line in map:
        if line.value_in_range(input):
            return line.process_value(input)
    return input


def location_for_seed(seed: int, maps: list[AlmanacMap]) -> int:
    value = seed

    for map in maps:
        value = process_map(value, map)
    return value


def find_closest_location(lines: list[str]) -> tuple[int, list[int], list[AlmanacMap]]:
    closest_location = float("inf")

    seeds = [int(num) for num in lines[0].split(": ")[1].split()]
    maps = read_maps(lines[3:])

    for seed in seeds:
        seed_location = location_for_seed(seed, maps)
        closest_location = min(closest_location, seed_location)

    return closest_location, seeds, maps


if __name__ == "__main__":
    part1test, seeds, maps = find_closest_location(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 35

    with open("day5.txt") as infile:
        lines = infile.read().splitlines()

    part1, seeds, maps = find_closest_location(lines)
    print(f"Part 1: {part1}")
    assert part1 == 910845529
