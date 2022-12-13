extern crate pathfinding;

use pathfinding::prelude::bfs;
use std::collections::HashMap;
use std::fs;

const TEST: &str = r#"Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"#;

#[derive(Hash, Eq, PartialEq, Debug, Clone, Copy, Ord, PartialOrd)]
struct Point {
    x: i32,
    y: i32,
}
struct HeightMap {
    start: Point,
    end: Point,
    locations: HashMap<Point, u8>,
}

impl From<Vec<&str>> for HeightMap {
    fn from(lines: Vec<&str>) -> Self {
        let mut start = Point { x: 0, y: 0 };
        let mut end = Point { x: 0, y: 0 };
        let mut locations = HashMap::new();
        for (y, line) in lines.iter().enumerate() {
            for (x, char) in line.as_bytes().iter().enumerate() {
                match char {
                    b'S' => {
                        start = Point {
                            x: x as i32,
                            y: y as i32,
                        };
                        locations.insert(
                            Point {
                                x: x as i32,
                                y: y as i32,
                            },
                            0,
                        );
                    }
                    b'E' => {
                        end = Point {
                            x: x as i32,
                            y: y as i32,
                        };
                        locations.insert(
                            Point {
                                x: x as i32,
                                y: y as i32,
                            },
                            25,
                        );
                    }
                    b'a'..=b'z' => {
                        locations.insert(
                            Point {
                                x: x as i32,
                                y: y as i32,
                            },
                            char - b'a',
                        );
                    }
                    _ => panic!("Invalid input"),
                }
            }
        }
        HeightMap {
            start,
            end,
            locations,
        }
    }
}

impl HeightMap {
    // Values to add to a point to get its four neighbors.
    const DIR: [Point; 4] = [
        Point { x: -1, y: 0 },
        Point { x: 1, y: 0 },
        Point { x: 0, y: -1 },
        Point { x: 0, y: 1 },
    ];
    fn successors(&self, pos: &Point) -> Vec<Point> {
        let reachable_height = self.locations[pos] + 1;
        Self::DIR
            .iter()
            .map(|p| Point {
                x: p.x + pos.x,
                y: p.y + pos.y,
            })
            .filter(|p| self.locations.contains_key(p) && self.locations[p] <= reachable_height)
            .collect()
    }

    fn reverse_successors(&self, pos: &Point) -> Vec<Point> {
        let reachable_height = self.locations[pos] - 1;
        Self::DIR
            .iter()
            .map(|p| Point {
                x: p.x + pos.x,
                y: p.y + pos.y,
            })
            .filter(|p| self.locations.contains_key(p) && self.locations[p] >= reachable_height)
            .collect()
    }

    fn find_shortest_path_length(&self, start_point: Point) -> usize {
        let result = bfs(&start_point, |p| self.successors(p), |p| *p == self.end).unwrap();
        result.len() - 1
    }

    fn find_shortest_path_from_a(&self) -> usize {
        let result = bfs(
            &self.end,
            |p| self.reverse_successors(p),
            |p| self.locations[p] == 0,
        )
        .unwrap();
        result.len() - 1
    }
}

fn main() {
    let height_map = HeightMap::from(TEST.lines().collect::<Vec<_>>());

    let part1test = height_map.find_shortest_path_length(height_map.start);
    println!("Part 1 test: {}", part1test);
    assert_eq!(part1test, 31);

    let part2test = height_map.find_shortest_path_from_a();
    println!("Part 2 test: {}", part2test);
    assert_eq!(part2test, 29);

    let binding = fs::read_to_string("../day12.txt").expect("Unable to read input.");
    let day12input = binding.lines().collect::<Vec<_>>();
    let height_map = HeightMap::from(day12input);
    let part1 = height_map.find_shortest_path_length(height_map.start);
    println!("Part 1: {}", part1);
    assert_eq!(part1, 456);

    let part2 = height_map.find_shortest_path_from_a();
    println!("Part 2: {}", part2);
    assert_eq!(part2, 454);
}
