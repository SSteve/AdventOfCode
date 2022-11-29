// Looking at solutions from last year to get a handle on Rust.
// This is based on https://www.reddit.com/r/adventofcode/comments/r6zd93/comment/hnisk0i/?utm_source=share&utm_medium=web2x&context=3

use std::fs;

const TEST: &str = r#"forward 5
down 5
forward 8
up 3
down 8
forward 2"#;

/// Representation of a Position.
///
/// Position consists of a depth and a position.
struct Position {
    depth: u32,
    position: u32,
    aim: i32,
}

/// Representation of a Submarine.
///
/// Submarines are represented by a Position.
struct Submarine {
    position: Position,
}

impl Submarine {
    /// Perform a move for part 1.
    fn move1(&mut self, direction: Direction) {
        match direction {
            Direction::Up(scalar) => self.position.depth -= scalar,
            Direction::Down(scalar) => self.position.depth += scalar,
            Direction::Forward(scalar) => self.position.position += scalar,
        }
    }

    fn move2(&mut self, direction: Direction) {
        match direction {
            Direction::Up(scalar) => self.position.aim -= scalar as i32,
            Direction::Down(scalar) => self.position.aim += scalar as i32,
            Direction::Forward(scalar) => {
                self.position.position += scalar;
                self.position.depth += self.position.aim as u32 * scalar;
            }
        }
    }
}

enum Direction {
    Up(u32),
    Down(u32),
    Forward(u32),
}

impl Direction {
    fn from(s: &str) -> Direction {
        let s: Vec<&str> = s.split_ascii_whitespace().collect();
        let scalar = s[1].parse::<u32>().unwrap();
        match s[0] {
            "down" => Direction::Down(scalar),
            "forward" => Direction::Forward(scalar),
            "up" => Direction::Up(scalar),
            _ => panic!("Illegal value for direction."),
        }
    }
}

fn follow_commands1(commands: &str) -> u32 {
    let mut submarine = Submarine {
        position: Position {
            depth: 0,
            position: 0,
            aim: 0,
        },
    };
    commands
        .lines()
        .for_each(|l| submarine.move1(Direction::from(l)));

    submarine.position.depth * submarine.position.position
}

fn follow_commands2(commands: &str) -> u32 {
    let mut submarine = Submarine {
        position: Position {
            depth: 0,
            position: 0,
            aim: 0,
        },
    };
    commands
        .lines()
        .for_each(|l| submarine.move2(Direction::from(l)));

    submarine.position.depth * submarine.position.position
}

fn main() {
    let part1test = follow_commands1(TEST);
    println!("Part 1 test: {}", part1test);

    let day2input = fs::read_to_string("../../2.txt").expect("Unable to read input.");
    let part1 = follow_commands1(&day2input);
    println!("Part 1: {}", part1);

    let part2test = follow_commands2(TEST);
    println!("Part 2 test: {}", part2test);

    let day2input = fs::read_to_string("../../2.txt").expect("Unable to read input.");
    let part2 = follow_commands2(&day2input);
    println!("Part 2: {}", part2);
}
