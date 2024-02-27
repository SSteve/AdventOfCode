import re
from dataclasses import dataclass
from typing import Iterable

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

    @staticmethod
    def border_points(sensor: Point, distance: int, min_coordinate: int, max_coordinate: int) -> Iterable[Point]:
        if sensor.x - distance >= min_coordinate:
            yield Point(sensor.x - distance, sensor.y)
        if sensor.x + distance <= max_coordinate:
            yield Point(sensor.x + distance, sensor.y)
        if sensor.y - distance >= min_coordinate:
            yield Point(sensor.x, sensor.y - distance)
        if sensor.y + distance <= max_coordinate:
            yield Point(sensor.x, sensor.y + distance)
        for delta in range(1, distance):
            x_plus = sensor.x + delta
            x_minus = sensor.x - delta
            y_plus = sensor.y + (distance - delta)
            y_minus = sensor.y - (distance - delta)
            if x_plus <= max_coordinate:
                if y_plus <= max_coordinate:
                    yield Point(x_plus, y_plus)
                if y_minus >= min_coordinate:
                    yield Point(x_plus, y_minus)
            if x_minus >= min_coordinate:
                if y_plus <= max_coordinate:
                    yield Point(x_minus, y_plus)
                if y_minus >= min_coordinate:
                    yield Point(x_minus, y_minus)

    def find_tuning_frequency(self, min_coordinate: int, max_coordinate: int) -> int:
        distances: dict[Point, int] = {}
        tested_sensors: set[Point] = set()
        for sensor in self.sensors:
            distances[sensor] = sensor.manhattan_distance_to(
                self.closest_beacons[sensor])
        while len(self.sensors) > 0:
            sensor = self.sensors.pop()
            for border_point in self.border_points(sensor, distances[sensor] + 1, min_coordinate, max_coordinate):
                if all(test_sensor1.manhattan_distance_to(border_point) > distances[test_sensor1]
                       for test_sensor1 in self.sensors) and \
                        all(test_sensor2.manhattan_distance_to(border_point) > distances[test_sensor2]
                            for test_sensor2 in tested_sensors):
                    return border_point.x * 4000000 + border_point.y
                    # print(Point(border_point.x, + border_point.y))
            tested_sensors.add(sensor)
        raise ValueError("No uncovered location found.")


if __name__ == "__main__":
    sensor_map = SensorMap(TEST.splitlines())

    part1test = sensor_map.count_covered_positions(10)
    print(f"Part 1 test: {part1test}")
    assert (part1test == 26)

    part2test = sensor_map.find_tuning_frequency(0, 20)
    print(f"Part 2 test: {part2test}")
    assert (part2test == 56000011)

    with open("day15.txt") as infile:
        sensor_map = SensorMap(infile.read().splitlines())

    part1 = sensor_map.count_covered_positions(2000000)
    print(f"Part 1: {part1}")
    assert (part1 == 4582667)

    part2 = sensor_map.find_tuning_frequency(0, 4000000)
    print(f"Part 2: {part2}")
    assert (part2 == 10961118625406)
