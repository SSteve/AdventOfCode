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


class Hand:
    cards: str
    bid: int
    type: HandType

    def __init__(self, cards, bid) -> None:
        self.cards = cards
        self.bid = int(bid)
        self.type = calculate_type(cards)

    def __repr__(self) -> str:
        return f"{self.cards} {self.type} bid: {self.bid}"

    def __lt__(self, other: Self) -> bool:
        if self.type.value == other.type.value:
            for this_rank, other_rank in zip(self.cards, other.cards):
                if CARD_RANKS.index(this_rank) < CARD_RANKS.index(other_rank):
                    return True
                if CARD_RANKS.index(this_rank) > CARD_RANKS.index(other_rank):
                    return False
            return False
        return self.type.value < other.type.value


def calculate_winnings(hand_strings: list[str]) -> int:
    hands = sorted(map(lambda vals: Hand(*(vals.split())), hand_strings))

    winnings = 0
    for i, hand in enumerate(hands):
        winnings += hand.bid * (i + 1)
    return winnings


if __name__ == "__main__":
    part1test = calculate_winnings(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 6440

    """     
    part2test = record_beating_count(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 71503
    """

    with open("day7.txt") as infile:
        lines = infile.read().splitlines()

    part1 = calculate_winnings(lines)
    print(f"Part 1: {part1}")

    """ 
    part2 = record_beating_count(lines)
    print(f"Part 2: {part2}")
     """
