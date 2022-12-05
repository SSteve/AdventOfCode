use lazy_static::lazy_static;
use regex::Regex;
use std::fs;

const TEST: &str = r#"2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"#;

fn pair_is_contained(pair_string: &str) -> bool {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"(\d+)-(\d+),(\d+)-(\d+)").unwrap();
    }
    let caps = RE.captures(pair_string).unwrap();
    let pair1start = caps.get(1).unwrap().as_str().parse::<u32>().unwrap();
    let pair1end = caps.get(2).unwrap().as_str().parse::<u32>().unwrap();
    let pair2start = caps.get(3).unwrap().as_str().parse::<u32>().unwrap();
    let pair2end = caps.get(4).unwrap().as_str().parse::<u32>().unwrap();
    pair2start >= pair1start && pair2end <= pair1end
        || pair1start >= pair2start && pair1end <= pair2end
}

fn pair_overlaps(pair_string: &str) -> bool {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"(\d+)-(\d+),(\d+)-(\d+)").unwrap();
    }
    let caps = RE.captures(pair_string).unwrap();
    let pair1start = caps.get(1).unwrap().as_str().parse::<u32>().unwrap();
    let pair1end = caps.get(2).unwrap().as_str().parse::<u32>().unwrap();
    let pair2start = caps.get(3).unwrap().as_str().parse::<u32>().unwrap();
    let pair2end = caps.get(4).unwrap().as_str().parse::<u32>().unwrap();
    pair2start <= pair1end && pair2end >= pair1start
}

fn count_contained_pairs(pair_strings: &str) -> u32 {
    let mut count: u32 = 0;
    for line in pair_strings.lines() {
        if pair_is_contained(line) {
            count += 1;
        }
    }
    count
}

fn count_overlapping_pairs(pair_strings: &str) -> u32 {
    let mut count: u32 = 0;
    for line in pair_strings.lines() {
        if pair_overlaps(line) {
            count += 1;
        }
    }
    count
}

fn main() {
    let part1test = count_contained_pairs(TEST);
    println!("Part 1 test: {}", part1test);
    assert_eq!(part1test, 2);
    let part2test = count_overlapping_pairs(TEST);
    println!("Part 2 test: {}", part2test);
    assert_eq!(part2test, 4);

    let day4input = fs::read_to_string("../day4.txt").expect("Unable to read input.");
    let part1 = count_contained_pairs(&day4input);
    println!("Part 1: {}", part1);
    assert_eq!(part1, 538);
    let part2 = count_overlapping_pairs(&day4input);
    println!("Part 2: {}", part2);
    assert_eq!(part2, 792);
}
