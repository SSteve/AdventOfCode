use lazy_static::lazy_static;
use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::fs;

const TEST: &str = r#"Sensor at x=2, y=18: closest beacon is at x=-2, y=15
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
Sensor at x=20, y=1: closest beacon is at x=15, y=3"#;

#[derive(Hash, Eq, PartialEq, Debug, Clone, Copy, Ord, PartialOrd)]
struct Point {
    x: i64,
    y: i64,
}

impl Point {
    fn manhattan_distance_to(&self, other: &Point) -> i64 {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }

    fn border_points(
        &self,
        distance: i64,
        min_coordinate: i64,
        max_coordinate: i64,
    ) -> HashSet<Point> {
        let mut points = HashSet::new();
        if self.x - distance >= min_coordinate {
            points.insert(Point {
                x: self.x - distance,
                y: self.y,
            });
        }
        if self.x + distance <= max_coordinate {
            points.insert(Point {
                x: self.x + distance,
                y: self.y,
            });
        }
        if self.y - distance >= min_coordinate {
            points.insert(Point {
                x: self.x,
                y: self.y - distance,
            });
        }
        if self.y + distance <= max_coordinate {
            points.insert(Point {
                x: self.x,
                y: self.y + distance,
            });
        }
        for delta in 1..distance {
            let x_plus = self.x + delta;
            let x_minus = self.x - delta;
            let y_plus = self.y + (distance - delta);
            let y_minus = self.y - (distance - delta);
            if x_plus <= max_coordinate {
                if y_plus <= max_coordinate {
                    points.insert(Point {
                        x: x_plus,
                        y: y_plus,
                    });
                }
                if y_minus >= min_coordinate {
                    points.insert(Point {
                        x: x_plus,
                        y: y_minus,
                    });
                }
            }
            if x_minus >= min_coordinate {
                if y_plus <= max_coordinate {
                    points.insert(Point {
                        x: x_minus,
                        y: y_plus,
                    });
                }
                if y_minus >= min_coordinate {
                    points.insert(Point {
                        x: x_minus,
                        y: y_minus,
                    });
                }
            }
        }

        points
    }
}

struct Sensor {
    point: Point,
    distance: i64,
    min_coordinate: i64,
    max_coordinate: i64,
    points: HashSet<Point>,
}

impl Iterator for Sensor {
    type Item = Point;

    fn next(&mut self) -> Option<Self::Item> {
        if self.point.x - self.distance >= self.min_coordinate {
            let point = Point {
                x: self.point.x - self.distance,
                y: self.point.y,
            };
            if !self.points.contains(&point) {
                self.points.insert(point);
                return Some(point);
            }
        }
        if self.point.x + self.distance <= self.max_coordinate {
            let point = Point {
                x: self.point.x + self.distance,
                y: self.point.y,
            };
            if !self.points.contains(&point) {
                self.points.insert(point);
                return Some(point);
            }
        }
        if self.point.y - self.distance >= self.min_coordinate {
            let point = Point {
                x: self.point.x,
                y: self.point.y - self.distance,
            };
            if !self.points.contains(&point) {
                self.points.insert(point);
                return Some(point);
            }
        }
        if self.point.y + self.distance <= self.max_coordinate {
            let point = Point {
                x: self.point.x,
                y: self.point.y + self.distance,
            };
            if !self.points.contains(&point) {
                self.points.insert(point);
                return Some(point);
            }
        }
        for delta in 1..self.distance {
            let x_plus = self.point.x + delta;
            let x_minus = self.point.x - delta;
            let y_plus = self.point.y + (self.distance - delta);
            let y_minus = self.point.y - (self.distance - delta);
            if x_plus <= self.max_coordinate {
                if y_plus <= self.max_coordinate {
                    let point = Point {
                        x: x_plus,
                        y: y_plus,
                    };
                    if !self.points.contains(&point) {
                        self.points.insert(point);
                        return Some(point);
                    }
                }
                if y_minus >= self.min_coordinate {
                    let point = Point {
                        x: x_plus,
                        y: y_minus,
                    };
                    if !self.points.contains(&point) {
                        self.points.insert(point);
                        return Some(point);
                    }
                }
            }
            if x_minus >= self.min_coordinate {
                if y_plus <= self.max_coordinate {
                    let point = Point {
                        x: x_minus,
                        y: y_plus,
                    };
                    if !self.points.contains(&point) {
                        self.points.insert(point);
                        return Some(point);
                    }
                }
                if y_minus >= self.min_coordinate {
                    let point = Point {
                        x: x_minus,
                        y: y_minus,
                    };
                    if !self.points.contains(&point) {
                        self.points.insert(point);
                        return Some(point);
                    }
                }
            }
        }
        None
    }
}

struct SensorMap {
    sensors: HashSet<Point>,
    closest_beacons: HashMap<Point, Point>,
}

impl From<Vec<&str>> for SensorMap {
    fn from(lines: Vec<&str>) -> Self {
        lazy_static! {
            static ref RE: Regex = Regex::new(
                r"Sensor at x=([-]?\d+), y=([-]?\d+): closest beacon is at x=([-]?\d+), y=([-]?\d+)"
            )
            .unwrap();
        }
        let mut sensors = HashSet::new();
        let mut closest_beacons = HashMap::new();
        for line in lines.iter() {
            let caps = RE.captures(line).expect("Regex failed.");
            let sensor_x = caps.get(1).unwrap().as_str().parse::<i64>().unwrap();
            let sensor_y = caps.get(2).unwrap().as_str().parse::<i64>().unwrap();
            let beacon_x = caps.get(3).unwrap().as_str().parse::<i64>().unwrap();
            let beacon_y = caps.get(4).unwrap().as_str().parse::<i64>().unwrap();
            sensors.insert(Point {
                x: sensor_x,
                y: sensor_y,
            });
            closest_beacons.insert(
                Point {
                    x: sensor_x,
                    y: sensor_y,
                },
                Point {
                    x: beacon_x,
                    y: beacon_y,
                },
            );
        }
        SensorMap {
            sensors,
            closest_beacons,
        }
    }
}

impl SensorMap {
    fn count_covered_positions(&self, line: i64) -> usize {
        let mut covered_locations = HashSet::new();
        for sensor in self.sensors.iter() {
            let distance_to_beacon = sensor.manhattan_distance_to(&self.closest_beacons[sensor]);
            if (line - sensor.y).abs() <= distance_to_beacon {
                let y_distance = (line - sensor.y).abs();
                let x_range = distance_to_beacon - y_distance;
                covered_locations.extend(sensor.x - x_range..=sensor.x + x_range);
            }
        }
        for beacon in self.closest_beacons.values() {
            if beacon.y == line {
                covered_locations.remove(&beacon.x);
            }
        }

        covered_locations.len()
    }

    fn find_tuning_frequency(&self, min_coordinate: usize, max_coordinate: usize) -> i64 {
        let mut distances = HashMap::<&Point, i64>::new();
        for sensor in self.sensors.iter() {
            distances.insert(
                sensor,
                sensor.manhattan_distance_to(&self.closest_beacons[sensor]) as i64,
            );
        }
        for sensor1 in self.sensors.iter() {
            for border_point in sensor1.border_points(
                distances[sensor1] + 1,
                min_coordinate as i64,
                max_coordinate as i64,
            ) {
                if self
                    .sensors
                    .iter()
                    .filter(|s| *s != sensor1)
                    .all(|s| s.manhattan_distance_to(&border_point) > distances[s])
                {
                    return border_point.x * 4_000_000 + border_point.y;
                }
            }
        }
        0
    }
}

fn main() {
    let sensor_map = SensorMap::from(TEST.lines().collect::<Vec<_>>());

    let part1test = sensor_map.count_covered_positions(10);
    println!("Part 1 test: {}", part1test);
    assert_eq!(part1test, 26);

    let part2test = sensor_map.find_tuning_frequency(0, 20);
    println!("Part 2 test: {}", part2test);
    assert_eq!(part2test, 56000011);

    let binding = fs::read_to_string("../day15.txt").expect("Unable to read input.");
    let day15input = binding.lines().collect::<Vec<_>>();
    let sensor_map = SensorMap::from(day15input);

    let part1 = sensor_map.count_covered_positions(2000000);
    println!("Part 1: {}", part1);
    assert_eq!(part1, 4582667);

    let part2 = sensor_map.find_tuning_frequency(0, 4000000);
    println!("Part 2: {}", part2);
    assert_eq!(part2, 10961118625406);
}
