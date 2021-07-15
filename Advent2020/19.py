# I completely copied this solution from https://github.com/mebeim/aoc/blob/master/2020/solutions/day19.py
# The walkthrough for this solution is at https://github.com/mebeim/aoc/blob/master/2020/README.md#day-19---monster-messages

from copy import deepcopy


def ParseInput(infile):
    rules = {}

    for line in map(str.rstrip, infile):
        if not line:
            break

        ruleId, options = line.split(': ')
        ruleId = int(ruleId)

        if '"' in options:
            rule = options[1:-1]
        else:
            rule = []
            for option in options.split('|'):
                rule.append(tuple(map(int, option.split())))

        rules[ruleId] = rule

    return rules


def match(rules, string, rule=0, index=0):
    if index == len(string):
        return []

    rule = rules[rule]
    if type(rule) is str:
        if string[index] == rule:
            return [index + 1]
        return []

    matches = []
    for option in rule:
        sub_matches = [index]

        for sub_rule in option:
            new_matches = []
            for idx in sub_matches:
                new_matches += match(rules, string, sub_rule, idx)
            sub_matches = new_matches

        matches += sub_matches

    return matches


infile = open("19.txt", "r")

rules1 = ParseInput(infile)
rules2 = deepcopy(rules1)
rules2[8] = [(42,), (42, 8)]
rules2[11] = [(42, 31), (42, 11, 31)]
valid1 = 0
valid2 = 0

for msg in map(str.rstrip, infile):
    if len(msg) in match(rules1, msg):
        valid1 += 1
    if len(msg) in match(rules2, msg):
        valid2 += 1

print(f"Part 1: {valid1}")
print(f"Part 2: {valid2}")



'''
This was my original solution for Day 1. It's very slow.


import re
from collections import deque

initialTerminal = re.compile(r"\"(.)\"")


class Rule:
    def __init__(self, head: str, body: deque[str]):
        self.head = head
        self.body = body

    def __repr__(self):
        return f"Rule({self.head}, {self.body})"


class Derivation:
    def __init__(self, head: str, derivation: list[str]):
        self.head = head
        self.derivation = derivation

    def __repr__(self):
        return f"Derivation({self.head}, {self.derivation})"

    def __hash__(self):
        return hash(self.head)

    def __eq__(self, other):
        return self.head == other


def BuildString(option: deque[str], prefix: str, derivations: dict[str, list[str]], strings: list[str]):
    head = option.popleft()
    if len(option):
        for derivation in derivations[head]:
            newPrefix = prefix + derivation
            BuildString(deque(option), newPrefix, derivations, strings)
    else:
        for derivation in derivations[head]:
            strings.append(prefix + derivation)


def Derive(rule: Rule, derivations: dict[str, list[str]]) -> list[str]:
    strings: list[str] = []
    for options in rule.body:
        BuildString(deque(options), "", derivations, strings)
    return strings


def BuildStrings(lines: list[str], makeSubstitutions=False) -> tuple[dict[str, list[str]], list[str]]:
    rules: deque[Rule] = deque()
    derivations: dict[str, list[str]] = {}
    lineIter = iter(lines)

    # Read all of the rules. If a rule is already a terminal,
    # add it to derivations.
    line = next(lineIter).strip()
    while len(line):
        split = line.split(':')
        head = split[0]
        productions = split[1].strip()
        match = initialTerminal.match(productions)
        if match:
            derivations[head] = [match[1]]
            line = next(lineIter).strip()
            continue
        optionStrings = productions.split('|')
        if head == '8' and makeSubstitutions:
            optionStrings = ['42', '42 8']
        if head == '11' and makeSubstitutions:
            optionStrings = ['42 31', '42 11 31']
        body = deque()
        for optionString in optionStrings:
            options = optionString.strip().split(" ")
            body.append(options)
        rules.append(Rule(head, body))

        line = next(lineIter).strip()

    # Now convert the rules into derivations.
    while len(rules):
        rule = rules.popleft()
        valid = True
        # Check to see if all of the options in this rule's body
        # have been derived.
        for options in rule.body:
            for option in options:
                if option not in derivations:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            # Not all of its rules have been derived yet, so move it to the
            # end of the list.
            rules.append(rule)
            continue
        else:
            # All of this rule's options are derived so build
            # its derivations.
            derivation = Derive(rule, derivations)
            derivations[rule.head] = derivation

    strings = [line.strip() for line in lineIter]

    return derivations, strings


def Part1(derivations: dict[str, list[str]], strings: list[str]) -> int:
    matches = 0
    rule0 = derivations['0']
    derivationLength = len(rule0[0])
    for string in strings:
        stringPos = 0
        while string[stringPos: stringPos + derivationLength] in rule0:
            stringPos += derivationLength
            if stringPos == len(string):
                # We've made it exactly to the end of the string so
                # this is a match.
                matches += 1
                break
            if stringPos + derivationLength > len(string):
                # We've gone beyond the end of the string so this one
                # doesn't match rule 0
                break
    return matches


TEST = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

TEST2 = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
ababbbababbb
abbbabababbb
abbbabababbb
abbbabaaabbb
abbbabababbba
aaabbb
aaaabbb"""

TEST3 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""


testDerivations, testStrings = BuildStrings(TEST.splitlines())
testMatches = Part1(testDerivations, testStrings)
assert testMatches == 2

testDerivations, testStrings = BuildStrings(TEST2.splitlines())
testMatches = Part1(testDerivations, testStrings)
assert testMatches == 4


with open("19.txt", "r") as infile:
    derivations, strings = BuildStrings(infile.readlines())
part1 = Part1(derivations, strings)
print(f"Part 1: {part1}")
# with open("19.txt", "r") as infile:
#     derivations, strings = BuildStrings(infile.readlines(), True)
'''