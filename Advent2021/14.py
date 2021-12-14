from collections import Counter

TEST = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


class Polymer:
    def __init__(self, input: str) -> None:
        template, ruleText = input.split("\n\n")
        # When we count elements, they all get double-counted except the
        # ones at the beginning and end so keep track of those.
        self.firstElement = template[0]
        self.lastElement = template[-1]
        self.pairs = Counter()
        for i in range(len(template) - 1):
            pair = template[i:i+2]
            self.pairs[pair] += 1
        self.rules: dict[str, str] = {}
        for rule in ruleText.split("\n"):
            parent, child = rule.split(" -> ")
            self.rules[parent] = child

    def PerformStep(self) -> None:
        newPairs = Counter()
        for pair in self.pairs:
            child = self.rules[pair]
            newPair1 = pair[0] + child
            newPair2 = child + pair[1]
            newPairs[newPair1] += self.pairs[pair]
            newPairs[newPair2] += self.pairs[pair]
        self.pairs = newPairs

    def MostMinusLeast(self) -> int:
        elements = Counter()
        for pair in self.pairs:
            elements[pair[0]] += self.pairs[pair]
            elements[pair[1]] += self.pairs[pair]
        # Add one to the first and last elements to adjust for double-counting.
        elements[self.firstElement] += 1
        elements[self.lastElement] += 1
        for element in elements.keys():
            elements[element] //= 2
        return elements.most_common()[0][1] - elements.most_common()[-1][1]

    def DoPart1(self) -> int:
        for _ in range(10):
            self.PerformStep()

        return self.MostMinusLeast()

    def DoPart2(self) -> int:
        for _ in range(30):
            self.PerformStep()

        return self.MostMinusLeast()


if __name__ == "__main__":
    polymer = Polymer(TEST)
    part1 = polymer.DoPart1()
    assert part1 == 1588
    part2 = polymer.DoPart2()
    assert part2 == 2188189693529

    with open("14.txt", "r") as infile:
        polymer = Polymer(infile.read())
    part1 = polymer.DoPart1()
    print(f"Part 1: {part1}")
    part2 = polymer.DoPart2()
    print(f"Part 2: {part2}")
