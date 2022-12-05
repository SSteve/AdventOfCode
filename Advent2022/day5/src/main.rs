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
    let caps = RE.captures(command).unwrap();
    let move_count = caps.get(1).unwrap().as_str().parse::<u32>().unwrap();
    let from_stack = caps.get(2).unwrap().as_str().parse::<usize>().unwrap() - 1;
    let to_stack = caps.get(3).unwrap().as_str().parse::<usize>().unwrap() - 1;
    for _ in 0..move_count {
        let value = stacks[from_stack].pop().unwrap();
        stacks[to_stack].push(value);
    }
}

fn build_stacks(starting_stacks: &Vec<&str>) -> Vec<Vec<String>> {
    let stacks = vec![
        vec!["Z".to_string(), "N".to_string()],
        vec!["M".to_string(), "C".to_string(), "D".to_string()],
        vec!["P".to_string()],
    ];

    stacks
}

fn move_stacks(stack_input: &str) -> String {
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
            process_command(&mut stacks, line);
        }
    }
    let mut stack_tops: String = "".to_string();
    for mut stack in stacks {
        stack_tops = format!("{}{}", stack_tops, stack.pop().unwrap());
    }
    stack_tops
}

fn main() {
    let part1test = move_stacks(TEST);
    println!("Part 1 test: {}", part1test);
    assert_eq!(part1test, "CMZ");
    //let part2test = count_overlapping_pairs(TEST);
    //println!("Part 2 test: {}", part2test);
    //assert_eq!(part2test, 4);

    /*
    let day5input = fs::read_to_string("../day5.txt").expect("Unable to read input.");
    let part1 = move_stacks(&day5input);
    println!("Part 1: {}", part1);
    assert_eq!(part1, 538);
    let part2 = count_overlapping_pairs(&day5input);
    println!("Part 2: {}", part2);
    assert_eq!(part2, 792);
    */
}
