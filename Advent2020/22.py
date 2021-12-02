from collections import deque
from hashlib import sha384
from itertools import islice


def PlayRound(deck1: deque[int], deck2: deque[int]):
    card1 = deck1.popleft()
    card2 = deck2.popleft()
    if card1 > card2:
        deck1.append(card1)
        deck1.append(card2)
    else:
        deck2.append(card2)
        deck2.append(card1)


def MakeDecks(lines: list[str]) -> tuple[deque[int], deque[int]]:
    deck1: deque[int] = deque()
    deck2: deque[int] = deque()
    currentDeck = deck1
    for line in lines[1:]:
        if len(line) == 0:
            continue
        if line.find("Player") > -1:
            # When we get to "Player 2:", switch current decks and skip this line.
            currentDeck = deck2
            continue
        currentDeck.append(int(line))
    return (deck1, deck2)


def CalculateDeckScore(deck: deque[int]) -> int:
    # Score is bottom card * 1 + next card * 2 + next card * 3, etc.
    score = 0
    for i in range(len(deck)):
        score += deck[-1 - i] * (i + 1)
    return score


def HashDeck(deck: deque[int]) -> bytes:
    # Calculate a hash of the deck for comparing to previous decks.
    deckAsStrings = [str(val) for val in deck]
    deckString = ''.join(deckAsStrings)
    hashValue = sha384(deckString.encode()).digest()
    return hashValue


def Part1(deck1: deque[int], deck2: deque[int]) -> int:
    while len(deck1) and len(deck2):
        PlayRound(deck1, deck2)
    if len(deck1):
        return CalculateDeckScore(deck1)
    return CalculateDeckScore(deck2)


def RecursiveCombat(deck1: deque[int], deck2: deque[int]) -> int:
    deck1Hashes: set[bytes] = set()
    deck2Hashes: set[bytes] = set()
    while len(deck1) and len(deck2):
        # If we've seen this before, Player 1 is instant winner.
        deck1Hash = HashDeck(deck1)
        deck2Hash = HashDeck(deck2)
        if deck1Hash in deck1Hashes and deck2Hash in deck2Hashes:
            return 1
        else:
            deck1Hashes.add(deck1Hash)
            deck2Hashes.add(deck2Hash)
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if len(deck1) >= card1 and len(deck2) >= card2:
            # Play a game of Recursive Combat.
            # Each deck has a number of cards equal to the value of the card drawn.
            slice1 = islice(deck1, 0, card1)
            slice2 = islice(deck2, 0, card2)
            winner = RecursiveCombat(deque(slice1), deque(slice2))
        else:
            if card1 > card2:
                winner = 1
            else:
                winner = 2
        if winner == 1:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
    if len(deck1):
        return 1
    return 2


def Part2(deck1: deque[int], deck2: deque[int]) -> int:
    winner = RecursiveCombat(deck1, deck2)
    if winner == 1:
        return CalculateDeckScore(deck1)
    return CalculateDeckScore(deck2)


TEST = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

TEST2 = """Player 1:
43
19

Player 2:
2
29
14"""


if __name__ == "__main__":
    testDeck1, testDeck2 = MakeDecks(TEST.splitlines())
    testPart1 = Part1(testDeck1.copy(), testDeck2.copy())
    assert testPart1 == 306
    testPart2 = Part2(testDeck1, testDeck2)
    assert testPart2 == 291

    testDeck1, testDeck2 = MakeDecks(TEST2.splitlines())
    testPart2 = Part2(testDeck1, testDeck2)
    assert testPart2 == 105

    with open("22.txt", "r") as infile:
        deck1, deck2 = MakeDecks(infile.read().splitlines())
    part1 = Part1(deck1.copy(), deck2.copy())
    print(f"Part 1: {part1}")
    part2 = Part2(deck1, deck2)
    print(f"Part 2: {part2}")
    assert part2 == 30498
