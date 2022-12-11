use std::collections::HashSet;
use std::fs;

fn find_start(signal: &str, window_length: u32) -> Option<u32> {
    for (index, window) in signal
        .as_bytes()
        .windows(window_length as usize)
        .enumerate()
    {
        let char_set: HashSet<_> = HashSet::from_iter(window);
        if char_set.len() == window_length as usize {
            return Some(index as u32 + window_length);
        }
    }

    None
}

fn find_start_of_packet(signal: &str) -> u32 {
    find_start(signal, 4).unwrap()
}

fn find_start_of_message(signal: &str) -> u32 {
    find_start(signal, 14).unwrap()
}

fn main() {
    let tests = vec![
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7u32, 19u32),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5u32, 23u32),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6u32, 23u32),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10u32, 29u32),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11u32, 26u32),
    ];

    for test in tests {
        let part1test = find_start_of_packet(test.0);
        println!("Part 1 test: {}", part1test);
        assert_eq!(part1test, test.1);
        let part2test = find_start_of_message(test.0);
        println!("Part 2 test: {}", part2test);
        assert_eq!(part2test, test.2);
    }

    let day6input = fs::read_to_string("../day6.txt").expect("Unable to read input.");
    let part1 = find_start_of_packet(&day6input);
    println!("Part 1: {}", part1);
    assert_eq!(part1, 1896);
    let part2 = find_start_of_message(&day6input);
    println!("Part 2: {}", part2);
    assert_eq!(part2, 3452);
}
