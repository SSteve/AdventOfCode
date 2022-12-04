// Just starting to learn Rust so this is undoubtedly rudimentary.

use std::collections::HashSet;
use std::fs;

const TEST: &str = r#"vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"#;

fn letter_score(letter: &char) -> u32 {
    if letter.is_uppercase() {
        27 + *letter as u32 - 'A' as u32
    } else {
        1 + *letter as u32 - 'a' as u32
    }
}

fn calculate_priority(rucksack: &str) -> u32 {
    let compartment1: HashSet<char> = rucksack.chars().take(rucksack.len() / 2).collect();
    let compartment2: HashSet<char> = rucksack.chars().skip(rucksack.len() / 2).collect();
    let intersection = compartment1.intersection(&compartment2);
    let letter = intersection
        .last()
        .expect("Couldn't get last item in intersection.");
    letter_score(letter)
}

fn sum_priorities(rucksacks: &str) -> u32 {
    let mut score: u32 = 0;
    for line in rucksacks.lines() {
        score += calculate_priority(line);
    }
    score
}

fn calculate_priority_group(rucksacks: Vec<&str>) -> u32 {
    assert_eq!(rucksacks.len(), 3);
    let set1: HashSet<char> = rucksacks[0].chars().collect();
    let set2: HashSet<char> = rucksacks[1].chars().collect();
    let intersection1: HashSet<char> = set1.intersection(&set2).copied().collect();
    let set3: HashSet<char> = rucksacks[2].chars().collect();
    let intersection2 = intersection1.intersection(&set3);
    let letter = intersection2
        .last()
        .expect("Couldn't get last item in intersection2.");
    letter_score(letter)
}

fn sum_groups(rucksacks: &str) -> u32 {
    let mut score: u32 = 0;
    let lines: Vec<&str> = rucksacks.lines().collect();
    for i in 0..lines.len() / 3 {
        let group = vec![lines[i * 3], lines[i * 3 + 1], lines[i * 3 + 2]];
        score += calculate_priority_group(group);
    }
    score
}

fn main() {
    let part1test = sum_priorities(TEST);
    println!("Part 1 test: {}", part1test);
    assert_eq!(part1test, 157);
    let part2test = sum_groups(TEST);
    println!("Part 2 test: {}", part2test);
    assert_eq!(part2test, 70);

    let day3input = fs::read_to_string("../day3.txt").expect("Unable to read input.");
    let part1 = sum_priorities(&day3input);
    println!("Part 1: {}", part1);
    let part2 = sum_groups(&day3input);
    println!("Part 2: {}", part2)
}
