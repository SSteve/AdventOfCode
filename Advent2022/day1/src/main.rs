use std::fs;

const TEST: &str = r#"1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"#;

fn find_most_calories(calories: &str) -> u32 {
    let mut highest: u32 = 0;
    let mut current: u32 = 0;

    for line in calories.lines() {
        if line.is_empty() {
            if current > highest {
                highest = current;
            }
            current = 0;
        } else {
            let value = line.parse::<u32>().unwrap();
            current += value;
        }
    }
    highest
}

fn find_three_most_calories(calories: &str) -> u32 {
    let mut elves: Vec<u32> = Vec::new();
    let mut current: u32 = 0;
    for line in calories.lines() {
        if line.is_empty() {
            elves.push(current);
            current = 0;
        } else {
            let value = line.parse::<u32>().unwrap();
            current += value;
        }
    }
    if current != 0 {
        elves.push(current);
    }
    elves.sort_by(|a, b| b.cmp(a));
    elves[0] + elves[1] + elves[2]
}

fn main() {
    let part1test = find_most_calories(TEST);
    println!("Part 1 test: {}", part1test);
    assert_eq!(part1test, 24000);
    let part2test = find_three_most_calories(TEST);
    println!("Part 2 test: {}", part2test);
    assert_eq!(part2test, 45000);

    let day1input = fs::read_to_string("../day1.txt").expect("Unable to read input.");
    let part1 = find_most_calories(&day1input);
    println!("Part 1: {}", part1);
    let part2 = find_three_most_calories(&day1input);
    println!("Part 2: {}", part2)
}
