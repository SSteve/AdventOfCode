// Looking at solutions from last year to get a handle on Rust.
// This is based on https://www.reddit.com/r/adventofcode/comments/r66vow/comment/hngfsqy/?utm_source=share&utm_medium=web2x&context=3
use std::fs;

fn main() {
    let input = fs::read_to_string("../../1.txt").expect("Unable to read input.");
    let mut previous: Option<u32> = None;
    let mut current: Option<u32>;
    let mut count: u32 = 0;

    for line in input.lines() {
        current = Some(line.parse::<u32>().unwrap());

        // Only test this value if the previous wasn't None.
        if let Some(value) = previous {
            if current.unwrap() > value {
                count += 1;
            }
        }
        previous = current;
    }
    println!("Part 1: {}", count);

    previous = None;
    count = 0;
    // Convert all the input values to a vector of u32.
    let lines: Vec<u32> = input
        .lines()
        .map(|line| line.parse::<u32>().unwrap())
        .collect();

    // Examine the input in windows of three at a time. We only care about the last
    // of the three.
    for values in lines.windows(3) {
        if let Some(value) = previous {
            if values[2] > value {
                count += 1;
            }
        }
        previous = Some(values[0]);
    }
    println!("Part 2: {}", count);
}
