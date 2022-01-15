from collections import namedtuple
from typing import Iterable

TEST = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
abcd[bddb]xyyp"""

TEST2 = """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb"""

AbaPattern = namedtuple('AbaPattern', ['a', 'b'])


def SplitSequences(ip: str) -> list[str]:
    # Split the strings into those inside and outside brackets. Strings
    # with even-numbered indicies are outide brackets.
    return ip.replace('[', ' ').replace(']', ' ').split()


def AbbaPatternFound(s: str) -> bool:
    for i in range(1, len(s) - 2):
        if s[i] == s[i+1] and s[i-1] == s[i+2] and s[i] != s[i-1]:
            return True
    return False


def SupportsTls(ip: str) -> bool:
    assert ip[0] != '['
    sequences = SplitSequences(ip)
    # Make sure the pattern isn't inside a bracketed sequence.
    for i in range(1, len(sequences), 2):
        if AbbaPatternFound(sequences[i]):
            return False
    # Look for the pattern outside brackets.
    for i in range(0, len(sequences), 2):
        if AbbaPatternFound(sequences[i]):
            return True
    # Pattern wasn't found outside brackets.
    return False


def FindAbaPatterns(sequence: str) -> set[AbaPattern]:
    result: set[AbaPattern] = set()
    for i in range(1, len(sequence) - 1):
        if sequence[i-1] == sequence[i+1] and sequence[i-1] != sequence[i]:
            result.add(AbaPattern(sequence[i-1], sequence[i]))
    return result


def ContainsBabPattern(sequence: str, patterns: Iterable[AbaPattern]) -> bool:
    for pattern in patterns:
        substring = pattern.b + pattern.a + pattern.b
        if substring in sequence:
            return True
    return False


def SupportsSsl(ip: str) -> bool:
    abaPatterns: set[AbaPattern] = set()
    sequences = SplitSequences(ip)
    for i in range(0, len(sequences), 2):
        abaPatterns |= FindAbaPatterns(sequences[i])
    for i in range(1, len(sequences), 2):
        if ContainsBabPattern(sequences[i], abaPatterns):
            return True
    return False


assert sum(int(SupportsTls(line)) for line in TEST.splitlines()) == 2
part2 = sum(int(SupportsSsl(line)) for line in TEST2.splitlines())
assert part2 == 3

with open('7.txt', 'r') as infile:
    part1 = sum(int(SupportsTls(line)) for line in infile.read().splitlines())
print(f"Part 1: {part1}")

with open('7.txt', 'r') as infile:
    part2 = sum(int(SupportsSsl(line)) for line in infile.read().splitlines())
print(f"Part 2: {part2}")
