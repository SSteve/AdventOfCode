from __future__ import annotations
from collections import deque
from typing import Tuple

import re

TEST1 = """deal with increment 7
deal into new stack
deal into new stack"""

TEST2 = """cut 6
deal with increment 7
deal into new stack"""

TEST3 = """deal with increment 7
deal with increment 9
cut -2"""

TEST4 = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""


class SpaceCards:
    def __init__(self, size: int) -> None:
        self.size = size
        self.deck: deque[int] = deque(i for i in range(size))
        self.reversed = False
        self.top = 0

    def Cut(self, length: int) -> None:
        if self.reversed:
            length = -length
        self.top = (self.top + length) % self.size

    def DealNewDeck(self) -> None:
        length = 1 if self.reversed else -1
        self.top = (self.top + length) % self.size
        self.reversed = not self.reversed

    def DealN(self, length: int) -> None:
        newDeck: deque[int] = deque([0] * self.size)
        # The index into the new deck.
        inx = 0
        # The amount to increment self.top.
        delta = -1 if self.reversed else 1
        for _ in range(self.size):
            newDeck[inx] = self.deck[self.top]
            inx = (inx + length) % self.size
            self.top = (self.top + delta) % self.size
        self.deck = newDeck
        self.reversed = False
        self.top = 0

    def CardN(self, cardNumber: int) -> int:
        if self.reversed:
            cardNumber = -cardNumber
        inx = (self.top + cardNumber) % self.size
        return self.deck[inx]

    def IndexOfCard(self, cardValue: int) -> int:
        inx = 0
        delta = -1 if self.reversed else 1
        for _ in range(self.size):
            if self.deck[(self.top + inx * delta) % self.size] == cardValue:
                return inx
            inx += 1

        return -1

    def ProcessInstructions(self, lines: list[str], show=False):
        for line in lines:
            if match := re.match(r"deal with increment (\d+)", line):
                self.DealN(int(match[1]))
            elif line == "deal into new stack":
                self.DealNewDeck()
            elif match := re.match(r"cut (-?\d+)", line):
                self.Cut(int(match[1]))
            else:
                raise ValueError(f"Unknown instruction: {line}")
            if show:
                print(self)

    def __repr__(self) -> str:
        result = ""
        inx = self.top
        delta = -1 if self.reversed else 1
        for i in range(self.size):
            result += f"{self.deck[inx]} "
            inx = (inx + delta) % self.size
        return result.strip()


def Transform(start: int, step: int, size: int, moves: list[str]) -> Tuple[int, int]:
    for move in moves:
        if move == "deal into new stack":
            start = (start - step) % size
            step = -step % size
        elif match := re.match(r"deal with increment (\d+)", move):
            step = (step * pow(int(match[1]), -1, size)) % size
        elif match := re.match(r"cut (-?\d+)", move):
            n = int(match[1])
            if n < 0:
                n += size

            start = (start + step * n) % size

    return start, step


def Repeat(start: int, step: int, size: int, repetitions: int) -> Tuple[int, int]:
    final_step = pow(step, repetitions, size)
    final_start = (start * (1 - final_step) *
                   pow(1 - step, -1, size)) % size

    return final_start, final_step


if __name__ == '__main__':
    cards = SpaceCards(10)
    cards.ProcessInstructions(TEST1.splitlines())
    assert cards.deck == deque(map(int, "0369258147"))
    assert cards.IndexOfCard(1) == 7

    cards = SpaceCards(10)
    cards.ProcessInstructions(TEST2.splitlines())
    assert repr(cards) == "3 0 7 4 1 8 5 2 9 6"
    assert cards.IndexOfCard(2) == 7

    cards = SpaceCards(10)
    cards.ProcessInstructions(TEST3.splitlines())
    assert repr(cards) == "6 3 0 7 4 1 8 5 2 9"
    assert cards.IndexOfCard(5) == 7

    cards = SpaceCards(10)
    cards.ProcessInstructions(TEST4.splitlines())
    assert repr(cards) == "9 2 5 8 1 4 7 0 3 6"
    assert cards.IndexOfCard(0) == 7

    cards = SpaceCards(10007)
    with open("22.txt", "r") as infile:
        instructions = infile.read().splitlines()
    cards.ProcessInstructions(instructions)
    print(f"Part 1: {cards.IndexOfCard(2019)}")

    # Part 2 is beyond me mathematically. I got my answer from
    # who, in turn, got it from https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/

    size = 10007
    start, step = Transform(0, 1, size, instructions)
    inx = ((2019 - start) * pow(step, -1, size)) % size
    assert inx == 3377

    start, step, size = 0, 1, 119315717514047
    repetitions = 101741582076661
    start, step = Transform(start, step, size, instructions)
    start, step = Repeat(start, step, size, repetitions)
    value = (start + step * 2020) % size
    print('Part 2:', value)
