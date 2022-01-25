from dataclasses import dataclass

TEST = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""


@dataclass
class Disc:
    period: int
    position: int


def ReadDiscs(lines: list[str]) -> list[Disc]:
    discs: list[Disc] = []
    for line in lines:
        words = line.split()
        period = int(words[3])
        position = int(words[-1][:-1])
        discs.append(Disc(period, position))
    return discs


def ProcessDiscs(discs: list[Disc]) -> int:
    delta = 1
    time = 0
    for i, disc in enumerate(discs):
        # discTime is the time at which the capsule will hit this disc.
        discTime = i + 1
        while (disc.position + discTime + time) % disc.period != 0:
            time += delta
        delta *= disc.period
    return time


"""
I wrote this after looking at the solution megathread to get hints.
"""

if __name__ == '__main__':
    discs = ReadDiscs(TEST.splitlines())
    part1 = ProcessDiscs(discs)
    assert part1 == 5

    with open('15.txt', 'r') as infile:
        discs = ReadDiscs(infile.read().splitlines())
    part1 = ProcessDiscs(discs)
    print(f"Part 1: {part1}")

    discs.append(Disc(11, 0))
    part2 = ProcessDiscs(discs)
    print(f"Part 2: {part2}")
