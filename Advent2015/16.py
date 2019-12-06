import re
from collections import defaultdict


def passTest(compound, sue, compounds):
    if compound in ("cats", "trees"):
        return sue[compound] > compounds[compound]
    if compound in ("pomeranians", "goldfish"):
        return sue[compound] != -1e15 and sue[compound] < compounds[compound]
    return sue[compound] == compounds[compound]


def day16(tickerTapeName, fileName):
    tickerRegex = re.compile(r"(.+): (\d+)")
    compounds = {}
    with open(tickerTapeName) as infile:
        for line in infile:
            match = tickerRegex.match(line)
            if match:
                compounds[match[1]] = int(match[2])

    sueRegex = re.compile(r"Sue (\d+): (.+): (\d+), (.+): (\d+), (.+): (\d+)")
    with open(fileName) as infile:
        for line in infile:
            sue = defaultdict(lambda: -1e15)
            match = sueRegex.match(line)
            if match:
                for i in range(2, 8, 2):
                    sue[match[i]] = int(match[i+1])
                matchCount = 0
                passCount = 0
                for compound in compounds:
                    if sue[compound] == compounds[compound]:
                        matchCount += 1
                    if passTest(compound, sue, compounds):
                        passCount += 1
                if matchCount == 3:
                    print(f"Part 1: Sue #{match[1]}")
                if passCount == 3:
                    print(f"Part 2: Sue #{match[1]}")


day16("16t.txt", "16.txt")
