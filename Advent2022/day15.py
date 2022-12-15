import re
from dataclasses import dataclass

TEST = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def manhattan_distance_to(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class SensorMap:
    def __init__(self, lines: list[str]) -> None:
        self.sensors: set[Point] = set()
        self.closest_beacons: dict[Point, Point] = {}
        regex = re.compile(
            r"Sensor at x=([-]?\d+), y=([-]?\d+): closest beacon is at x=([-]?\d+), y=([-]?\d+)")
        for line in lines:
            line_match = regex.match(line)
            if line_match is None:
                raise ValueError(f"Invalid line: {line}")
            sensor_point = Point(int(line_match[1]), int(line_match[2]))
            self.sensors.add(sensor_point)
            beacon_point = Point(int(line_match[3]), int(line_match[4]))
            self.closest_beacons[sensor_point] = beacon_point

    def count_covered_positions(self, line: int):
        covered_locations: set[int] = set()
        for sensor in self.sensors:
            distance_to_beacon = sensor.manhattan_distance_to(
                self.closest_beacons[sensor])
            if abs(line - sensor.y) <= distance_to_beacon:
                y_distance = abs(line - sensor.y)
                x_range = distance_to_beacon - y_distance
                for x in range(sensor.x - x_range, sensor.x + x_range + 1):
                    covered_locations.add(x)
        for beacon in self.closest_beacons.values():
            if beacon.y == line:
                covered_locations.discard(beacon.x)
        return len(covered_locations)

    def find_tuning_frequency(self, min_coordinate: int, max_coordinate: int) -> int:
        distances: dict[Point, int] = {}
        for sensor in self.sensors:
            distances[sensor] = sensor.manhattan_distance_to(
                self.closest_beacons[sensor])
        for x in range(min_coordinate, max_coordinate + 1):
            for y in range(min_coordinate, max_coordinate + 1):
                this_point = Point(x, y)
                if all(this_point.manhattan_distance_to(s) > distances[s] for s in self.sensors):
                    return this_point.x * 4000000 + this_point.y
        raise ValueError("No uncovered location found.")


if __name__ == "__main__":
    sensor_map = SensorMap(TEST.splitlines())

    part1test = sensor_map.count_covered_positions(10)
    print(f"Part 1 test: {part1test}")
    assert (part1test == 26)

    part2test = sensor_map.find_tuning_frequency(0, 20)
    print(f"Part 2 test: {part2test}")

    with open("day15.txt") as infile:
        sensor_map = SensorMap(infile.read().splitlines())

    part1 = sensor_map.count_covered_positions(2000000)
    print(f"Part 1: {part1}")
    assert (part1 == 4582667)

    part2 = sensor_map.find_tuning_frequency(0, 4000000)
    print(f"Part 2: {part2}")
