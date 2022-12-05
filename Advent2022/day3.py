TEST = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def letter_score(letter: str) -> int:
    if letter.islower():
        return 1 + ord(letter) - ord('a')
    else:
        return 27 + ord(letter) - ord('A')


def calculate_priority(rucksack: str) -> int:
    compartment1 = set(rucksack[:len(rucksack) // 2])
    compartment2 = set(rucksack[len(rucksack)//2:])
    common = compartment1 & compartment2
    assert (len(common) == 1)
    return letter_score(common.pop())


def sum_priorities(rucksacks: list[str]) -> int:
    score = 0
    for rucksack in rucksacks:
        score += calculate_priority(rucksack)
    return score


def calculate_group_priority(rucksacks: list[str]) -> int:
    assert len(rucksacks) == 3
    common = set(rucksacks[0]) & set(rucksacks[1]) & set(rucksacks[2])
    assert (len(common) == 1)
    return letter_score(common.pop())


def sum_groups(rucksacks: list[str]) -> int:
    score = 0
    for i in range(len(rucksacks)//3):
        score += calculate_group_priority(rucksacks[i*3:(i+1)*3])
    return score


if __name__ == "__main__":
    part1test = sum_priorities(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert (part1test == 157)

    part2test = sum_groups(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert (part2test == 70)

    with open("day3.txt") as infile:
        rucksacks = infile.read().splitlines()

    part1 = sum_priorities(rucksacks)
    print(f"Part 1: {part1}")

    part2 = sum_groups(rucksacks)
    print(f"Part 2: {part2}")
