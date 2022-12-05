import re

TEST = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

line_regex = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")


def pair_is_contained(pair_string: str) -> bool:


def count_contained_pairs(pair_strings: list[str]) -> int:
    count = 0


if __name__ == "__main__":
    part1test = sum_priorities(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert (part1test == 157)
