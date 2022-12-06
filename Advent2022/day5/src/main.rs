use lazy_static::lazy_static;
use regex::Regex;
use std::fs;

const TEST: &str = r#"    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"#;

fn process_command(stacks: &mut [Vec<String>], command: &str) {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"move (\d+) from (\d+) to (\d+)").unwrap();
    }
    let caps = RE.captures(command).expect("Regex failed.");
    let move_count = caps.get(1).unwrap().as_str().parse::<u32>().unwrap();
    let from_stack = caps.get(2).unwrap().as_str().parse::<usize>().unwrap() - 1;
    let to_stack = caps.get(3).unwrap().as_str().parse::<usize>().unwrap() - 1;
    for _ in 0..move_count {
        let value = stacks[from_stack].pop().unwrap();
        stacks[to_stack].push(value);
    }
}

fn process_command_2(stacks: &mut [Vec<String>], command: &str) {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"move (\d+) from (\d+) to (\d+)").unwrap();
    }
    let caps = RE.captures(command).expect("Regex failed.");
    let move_count = caps.get(1).unwrap().as_str().parse::<u32>().unwrap();
    let from_stack = caps.get(2).unwrap().as_str().parse::<usize>().unwrap() - 1;
    let to_stack = caps.get(3).unwrap().as_str().parse::<usize>().unwrap() - 1;
    let mut temp_stack = Vec::<String>::new();
    for _ in 0..move_count {
        let value = stacks[from_stack].pop().unwrap();
        temp_stack.push(value);
    }
    for _ in 0..move_count {
        let value = temp_stack.pop().unwrap();
        stacks[to_stack].push(value);
    }
}

fn build_stacks(stack_input: &Vec<&str>) -> Vec<Vec<String>> {
    // Get the indexes of each stack.
    let stack_indices: Vec<usize> = Regex::new(r"\d")
        .expect("Regex failed.")
        .find_iter(stack_input[stack_input.len() - 1])
        .map(|m| m.start())
        .collect();

    let re = Regex::new(r"([[:alpha:]]{1})").unwrap();
    let mut stacks = Vec::<Vec<String>>::new();
    for _ in 0..stack_indices.len() {
        stacks.push(Vec::<String>::new());
    }
    // Process each line of input from bottom to top.
    for stack_line in stack_input.iter().rev().skip(1) {
        // Create a vector of the characters in the line of input.
        let stack_chars: Vec<char> = stack_line.chars().collect();
        // Find the index of each letter in the input line.
        for index in re.find_iter(stack_line) {
            // Find the index of the vector that contains the stack
            // corresponding to the index of the letter.
            let vector_index = stack_indices
                .iter()
                .position(|i| *i == index.start())
                .unwrap();
            // Push the letter onto the stack.
            stacks[vector_index].push(stack_chars[index.start()].to_string());
        }
    }

    stacks
}

fn move_stacks(stack_input: &str, f: &dyn Fn(&mut [Vec<String>], &str)) -> String {
    let mut starting_stacks: Vec<&str> = Vec::new();
    let mut building_stacks = true;
    let mut stacks: Vec<Vec<String>> = Vec::new();
    for line in stack_input.lines() {
        if building_stacks {
            if line.is_empty() {
                building_stacks = false;
                stacks = build_stacks(&starting_stacks);
            } else {
                starting_stacks.push(line);
            }
        } else {
            f(&mut stacks, line);
        }
    }
    let mut stack_tops: String = "".to_string();
    for mut stack in stacks {
        stack_tops = format!("{}{}", stack_tops, stack.pop().unwrap());
    }
    stack_tops
}

fn main() {
    let part1test = move_stacks(TEST, &process_command);
    println!("Part 1 test: {}", part1test);
    assert_eq!(part1test, "CMZ");
    let part2test = move_stacks(TEST, &process_command_2);
    println!("Part 2 test: {}", part2test);
    assert_eq!(part2test, "MCD");

    let day5input = fs::read_to_string("../day5.txt").expect("Unable to read input.");
    let part1 = move_stacks(&day5input, &process_command);
    println!("Part 1: {}", part1);
    assert_eq!(part1, "ZRLJGSCTR");
    let part2 = move_stacks(&day5input, &process_command_2);
    println!("Part 2: {}", part2);
}
