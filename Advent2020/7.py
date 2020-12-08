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

    def __repr__(self):
        return self.name

    def CanContain(self, target: str, bags: List['Bag']) -> bool:
        if len(self.contents) == 0:
            return False
        if any(content.name == target for content in self.contents):
            return True
        return any(Bag.FindInList(bag.name, bags).CanContain(target, bags) for bag in self.contents)

    def ContentsCount(self, bags: List['Bag']) -> int:
        if len(self.contents) == 0:
            return 0

        contentsCount = 0
        for bagContents in self.contents:
            contentsCount += bagContents.count
            bag = Bag.FindInList(bagContents.name, bags)
            contentsCount += bagContents.count * bag.ContentsCount(bags)
        return contentsCount

    @staticmethod
    def FindInList(bagName: str, bagList: List['Bag']) -> 'Bag':
        for bag in bagList:
            if bag.name == bagName:
                return bag
        return None


def ParseInput(input: List[str]) -> List[Bag]:
    bags: List[Bag] = []
    for line in input:
        splitPos = line.find(" bags contain ")
        if splitPos > -1:
            bags.append(
                Bag(line[:splitPos], line[splitPos + 14:-1].split(',')))
    return bags


def Part1(target: str, bags: List[Bag]) -> int:
    # Find all the bags that can contain the named bag.
    return sum(bag.CanContain(target, bags) for bag in bags)


def Part2(outerBag: str, bags: List[Bag]) -> int:
    # Count all the bags that this one contains.
    thisBag = Bag.FindInList(outerBag, bags)
    return thisBag.ContentsCount(bags)


TEST = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

TEST2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

if __name__ == "__main__":
    testInput = ParseInput(TEST.splitlines())
    testPart1Count = Part1("shiny gold", testInput)
    assert testPart1Count == 4, f"Part 1 result is {testPart1Count}. Should be 4."
    shinyGoldBag = Bag.FindInList("shiny gold", testInput)
    testPart2Count = shinyGoldBag.ContentsCount(testInput)
    assert testPart2Count == 32, f"Part 2 result is {testPart2Count}. Should be 32."

    test2Input = ParseInput(TEST2.splitlines())
    shinyGoldBag = Bag.FindInList("shiny gold", test2Input)
    test2Part2Count = shinyGoldBag.ContentsCount(test2Input)
    assert test2Part2Count == 126, f"Part 2 test 2 result is {test2Part2Count}. Should be 126."

    with open("7.txt", "r") as infile:
        bags = ParseInput(infile.read().splitlines())
    part1Count = Part1("shiny gold", bags)
    print(f"Part 1: {part1Count}")
    shinyGoldBag = Bag.FindInList("shiny gold", bags)
    print(f"Part 2: {shinyGoldBag.ContentsCount(bags)}")
