from collections import Counter
from enum import Enum
from typing import Self

TEST = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


CARD_RANKS = "23456789TJQKA"
CARD_RANKS_WITH_JOKER = "J23456789TQKA"


def calculate_type(cards: str) -> HandType:
    counts = Counter(cards)
    if len(counts) == 1:
        return HandType.FIVE_OF_A_KIND
    if len(counts) == 5:
        return HandType.HIGH_CARD
    if 4 in counts.values():
        return HandType.FOUR_OF_A_KIND
    if 3 in counts.values():
        if 2 in counts.values():
            return HandType.FULL_HOUSE
        return HandType.THREE_OF_A_KIND
    two_count = list(counts.values()).count(2)
    if two_count == 2:
        return HandType.TWO_PAIR
    if two_count == 1:
        return HandType.ONE_PAIR

    raise ValueError(f"Type couldn't be calculated from {cards}. ({counts})")


def calculate_type_with_jokers(cards: str) -> HandType:
    counts = Counter(cards)
    jokers = counts["J"]
    if jokers == 0:
        return calculate_type(cards)
    # Remove jokers from counts.
    del counts["J"]
    if len(counts) <= 1:
        # There's one card plus jokers or five jokers.
        return HandType.FIVE_OF_A_KIND
    if max(counts.values()) + jokers == 4:
        # There's four of something plus joker, so the highest possible is four-of-a-kind.
        return HandType.FOUR_OF_A_KIND
    if 2 in counts.values():
        if len(counts) == 2:
            # There's two of something, two of something else, and one joker.
            # (If there were two of something and two jokers we would have returned four-of-a-kind.)
            return HandType.FULL_HOUSE
        # There's two of something and one of everything else.
        return HandType.THREE_OF_A_KIND
    if jokers == 2:
        # There's one of everything. If there are two jokers, we have three-of-a-kind.
        return HandType.THREE_OF_A_KIND
    if len(counts) == 4:
        # There's one of four different things and one joker.
        return HandType.ONE_PAIR
    # HIGH_CARD is not possible with a joker.

    raise ValueError(f"Type couldn't be calculated from {cards}. ({counts})")


class Hand:
    cards: str
    bid: int
    type: HandType
    with_jokers: bool

    def __init__(self, cards, bid, with_jokers: bool = False) -> None:
        self.cards = cards
        self.bid = int(bid)
        self.type = calculate_type_with_jokers(cards) if with_jokers else calculate_type(cards)
        self.with_jokers = with_jokers

    def __repr__(self) -> str:
        return f"{self.cards} {self.type} bid: {self.bid}"

    def __lt__(self, other: Self) -> bool:
        if self.type.value == other.type.value:
            ranks = CARD_RANKS_WITH_JOKER if self.with_jokers else CARD_RANKS
            for this_rank, other_rank in zip(self.cards, other.cards):
                if ranks.index(this_rank) < ranks.index(other_rank):
                    return True
                if ranks.index(this_rank) > ranks.index(other_rank):
                    return False
            return False
        return self.type.value < other.type.value


def calculate_winnings(hand_strings: list[str], with_jokers=False) -> int:
    hands = sorted(map(lambda vals: Hand(*(vals.split()), with_jokers), hand_strings))

    winnings = 0
    for i, hand in enumerate(hands):
        winnings += hand.bid * (i + 1)
    return winnings


if __name__ == "__main__":
    part1test = calculate_winnings(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 6440

    part2test = calculate_winnings(TEST.splitlines(), True)
    print(f"Part 2 test: {part2test}")
    assert part2test == 5905

    with open("day7.txt") as infile:
        lines = infile.read().splitlines()

    part1 = calculate_winnings(lines)
    print(f"Part 1: {part1}")
    assert part1 == 249390788

    part2 = calculate_winnings(lines, True)
    print(f"Part 2: {part2}")
