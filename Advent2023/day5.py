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
        values = (int(num) for num in line.split())
        return AlmanacLine(*values)

    def value_in_range(self, value: int) -> bool:
        return self.source_start <= value < self.source_start + self.range

    def process_value(self, value: int) -> int:
        return value + self.delta

    @property
    def delta(self) -> int:
        return self.destination_start - self.source_start

    @property
    def stop_exclusive(self) -> int:
        return self.source_start + self.range


@dataclass(frozen=True)
class ValueRange:
    start: int
    stop_exclusive: int

    def from_delta(self, delta: int) -> Self:
        return ValueRange(self.start + delta, self.stop_exclusive + delta)

    def with_start(self, new_start: int) -> Self:
        return ValueRange(new_start, self.stop_exclusive)

    def with_stop_exclusive(self, new_stop_exclusive: int) -> Self:
        return ValueRange(self.start, new_stop_exclusive)

    def __lt__(self, other: Self) -> bool:
        if self.start < other.start:
            return True
        if self.start == other.start:
            return self.stop_exclusive < other.stop_exclusive
        return False


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

    # seeds = [int(num) for num in lines[0].split(": ")[1].split()]
    seeds = list(map(int, lines[0].split(": ")[1].split()))
    maps = read_maps(lines[3:])

    for seed in seeds:
        seed_location = location_for_seed(seed, maps)
        closest_location = min(closest_location, seed_location)

    return closest_location, seeds, maps


def get_ranges_for_map(ranges: set[ValueRange], map: AlmanacMap) -> list[ValueRange]:
    output_ranges: set[ValueRange] = set()
    remaining_ranges = ranges

    for line in map:
        ranges = remaining_ranges
        remaining_ranges = set()
        for value_range in ranges:
            if value_range.stop_exclusive <= line.source_start or value_range.start >= line.stop_exclusive:
                # This range is completely outside the range of this line so it passes through unchanged.
                remaining_ranges.add(value_range)
                continue

            if value_range.start >= line.source_start and value_range.stop_exclusive <= line.stop_exclusive:
                # This range is completely inside the range of this line so passes through as a single
                # range offset by this line's delta.
                output_ranges.add(value_range.from_delta(line.delta))
                continue

            # At this point we know the range is split by this line.
            if value_range.start < line.source_start:
                # The part of this range to the left of the line is passed through unchanged.
                remaining_ranges.add(value_range.with_stop_exclusive(line.source_start))
                value_range = value_range.with_start(line.source_start)

            if value_range.stop_exclusive > line.stop_exclusive:
                # The part of this range to the right of the line is passed through unchanged.
                remaining_ranges.add(value_range.with_start(line.stop_exclusive))
                value_range = value_range.with_stop_exclusive(line.stop_exclusive)

            # The remainder of this range is now completely inside the range.
            output_ranges.add(value_range.from_delta(line.delta))

    return output_ranges | remaining_ranges


def closest_location_for_seed_range(seed: int, seed_range: int, maps: list[AlmanacMap]) -> int:
    value_ranges: set[ValueRange] = set()
    value_ranges.add(ValueRange(seed, seed + seed_range))
    for map in maps:
        value_ranges = get_ranges_for_map(value_ranges, map)

    closest = min(v.start for v in value_ranges)
    return closest


def find_closest_location2(seeds: list[int], maps: list[AlmanacMap]) -> int:
    closest_location = float("inf")
    for seed, seedrange in (seeds[i : i + 2] for i in range(0, len(seeds), 2)):
        seed_location = closest_location_for_seed_range(seed, seedrange, maps)
        closest_location = min(closest_location, seed_location)

    return closest_location


if __name__ == "__main__":
    part1test, seeds, maps = find_closest_location(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 35

    part2test = find_closest_location2(seeds, maps)
    print(f"Part 2 test: {part2test}")
    assert part2test == 46

    with open("day5.txt") as infile:
        lines = infile.read().splitlines()

    part1, seeds, maps = find_closest_location(lines)
    print(f"Part 1: {part1}")
    assert part1 == 910845529

    part2 = find_closest_location2(seeds, maps)
    print(f"Part 2: {part2}")
