import re
from dataclasses import dataclass
from typing import List


bagContents = re.compile(r"(\d+) (.+) bag[s]?")


@dataclass
class BagContent:
    count: int
    name: str


class Bag:
    def __init__(self, name: str, contents: List[str]):
        self.name = name
        self.contents: List[BagContent] = []
        for content in contents:
            match = bagContents.match(content.strip())
            if match:
                self.contents.append(BagContent(int(match[1]), match[2]))


def ParseInput(input: List[str]) -> List[Bag]:
    bags: List[Bag] = []
    for line in input:
        splitPos = line.find(" bags contain ")
        if splitPos > -1:
            bags.append(
                Bag(line[:splitPos], line[splitPos + 14:-1].split(',')))
    return bags


def Part1(target: str, bags: List[Bag]) -> int:
    count = 0
    # Find all the bags that can contain target directly.
    directBags: List[Bag] = []

    for bag in bags:
        if any(content.name == target for content in bag.contents):
            directBags.append(bag)

TEST = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""


if __name__ == "__main__":
    testInput = ParseInput(TEST.splitlines())
