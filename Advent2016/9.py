import re

marker = re.compile(r"\((\d+)x(\d+)\)")

TEST1 = "X(8x2)(3x3)ABCY"
TEST2 = "(27x12)(20x12)(13x14)(7x10)(1x12)A"
TEST3 = "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"


def DecompressedLength(text: str) -> int:
    i = 0
    decompressedLength = 0
    while i < len(text):
        while i < len(text) and text[i] != '(':
            i += 1
            decompressedLength += 1
        if i < len(text):
            match = re.match(marker, text[i:])
            if match is None:
                raise ValueError(f"Unable to find marker at position {i}.")
            length = int(match[1])
            repeats = int(match[2])
            decompressedLength += length * repeats
            i += len(match[0]) + length
    return decompressedLength


def DecompressedLength2(text: str) -> int:
    i = 0
    decompressedLength = 0
    while i < len(text):
        while i < len(text) and text[i] != '(':
            i += 1
            decompressedLength += 1
        if i < len(text):
            match = re.match(marker, text[i:])
            if match is None:
                raise ValueError(f"Unable to find marker at position {i}.")
            length = int(match[1])
            repeats = int(match[2])
            decompressedLength += DecompressedLength2(
                text[i + len(match[0]):i + len(match[0]) + length]) * repeats
            i += len(match[0]) + length

    return decompressedLength


part1 = DecompressedLength(TEST1)
assert part1 == 18

with open('9.txt', 'r') as infile:
    part1 = DecompressedLength(infile.read().strip())
print(f"Part 1: {part1}")

part2 = DecompressedLength2(TEST1)
assert part2 == 20

part2 = DecompressedLength2(TEST2)
assert part2 == 241920

part2 = DecompressedLength2(TEST3)
assert part2 == 445

with open('9.txt', 'r') as infile:
    part2 = DecompressedLength2(infile.read().strip())
print(f"Part 2: {part2}")
