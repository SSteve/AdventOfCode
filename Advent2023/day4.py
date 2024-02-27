TEST = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def winning_number_count(card: str) -> int:
    winners, numbers = card.split(": ")[1].split("|")
    win_set = set(int(i) for i in winners.split())
    number_set = set(int(i) for i in numbers.split())
    # The winning numbers are the intersection of the two sets of numbers.
    winning_numbers = number_set & win_set
    return len(winning_numbers)


def calculate_winning_numbers(cards: list[str]) -> int:
    sum = 0

    for card in cards:
        winner_count = winning_number_count(card)
        if winner_count:
            sum += 2 ** (winner_count - 1)

    return sum


def count_scratchcards(cards: list[str]) -> int:
    card_counts = [0] * len(cards)

    for card_number, card in enumerate(cards):
        card_counts[card_number] += 1
        winner_count = winning_number_count(card)
        for i in range(winner_count):
            if card_number + 1 + i < len(cards):
                # The number of subsequent cards is increased by the count of the current card.
                card_counts[card_number + 1 + i] += card_counts[card_number]

    return sum(card_counts)


if __name__ == "__main__":
    part1test = calculate_winning_numbers(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 13

    part2test = count_scratchcards(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 30

    with open("day4.txt") as infile:
        cards = infile.read().splitlines()

    part1 = calculate_winning_numbers(cards)
    print(f"Part 1: {part1}")
    assert part1 == 20855

    part2 = count_scratchcards(cards)
    print(f"Part 2: {part2}")
