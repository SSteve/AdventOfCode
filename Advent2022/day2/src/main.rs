use std::fs;

const TEST: &str = r#"A Y
B X
C Z"#;

fn score_round(round: &str) -> u32 {
    let mut chars = round.chars();
    let opponent = chars.next().unwrap();
    let _ = chars.next();
    let mine = chars.next().unwrap();
    let score: u32;

    match opponent {
        'A' => match mine {
            'X' => score = 3 + 1,
            'Y' => score = 6 + 2,
            'Z' => score = 3,
            _ => panic!("Invalid opponent value."),
        },
        'B' => match mine {
            'X' => score = 1,
            'Y' => score = 3 + 2,
            'Z' => score = 6 + 3,
            _ => panic!("Invalid opponent value."),
        },
        'C' => match mine {
            'X' => score = 6 + 1,
            'Y' => score = 2,
            'Z' => score = 3 + 3,
            _ => panic!("Invalid opponent value."),
        },
        _ => panic!("Invalid opponent value."),
    };
    score
}

fn strategize_round(round: &str) -> u32 {
    let mut chars = round.chars();
    let opponent = chars.next().unwrap();
    let _ = chars.next();
    let mine = chars.next().unwrap();
    let mut score: u32;

    match mine {
        'X' => {
            score = 0;
            match opponent {
                'A' => score += 3,
                'B' => score += 1,
                'C' => score += 2,
                _ => panic!("Invalid opponent value."),
            }
        }
        'Y' => {
            score = 3;
            match opponent {
                'A' => score += 1,
                'B' => score += 2,
                'C' => score += 3,
                _ => panic!("Invalid opponent value."),
            }
        }
        'Z' => {
            score = 6;
            match opponent {
                'A' => score += 2,
                'B' => score += 3,
                'C' => score += 1,
                _ => panic!("Invalid opponent value."),
            }
        }
        _ => panic!("Invalid opponent value."),
    };
    score
}

fn tally_score(strategy_guide: &str) -> u32 {
    let mut score: u32 = 0;
    for line in strategy_guide.lines() {
        score += score_round(line);
    }
    score
}

fn tally_strategy(strategy_guide: &str) -> u32 {
    let mut score: u32 = 0;
    for line in strategy_guide.lines() {
        score += strategize_round(line);
    }
    score
}

fn main() {
    let part1test = tally_score(TEST);
    println!("Part 1 test: {}", part1test);
    assert_eq!(part1test, 15);
    let part2test = tally_strategy(TEST);
    println!("Part 2 test: {}", part2test);
    assert_eq!(part2test, 12);

    let day2input = fs::read_to_string("../day2.txt").expect("Unable to read input.");
    let part1 = tally_score(&day2input);
    println!("Part 1: {}", part1);
    let part2 = tally_strategy(&day2input);
    println!("Part 2: {}", part2)
}
