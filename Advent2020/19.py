import re
from collections import deque

initialTerminal = re.compile(r"\"(.)\"")

class Rule:
    def __init__(self, head, body):
        self.head = head
        self.body = body
        
    def __repr__(self):
        return f"Rule({self.head}, {self.body})"
        
        
class Derivation:
    def __init__(self, head, derivation):
        self.head = head
        self.derivation = derivation
        
    def __repr__(self):
        return f"Derivation({self.head}, {self.derivation})"
        
    def __hash__(self):
        return hash(self.head)
        
    def __eq__(self, other):
        return self.head == other

def Day19(lines):
    rules = deque()
    derivations = set()
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
            derivations.add(Derivation(head, [match[1]]))
            line = next(lineIter).strip()
            continue
        optionStrings = productions.split('|')
        body = []
        for optionString in optionStrings:
            options = optionString.strip().split(" ")
            body.append(options)
        rules.append(Rule(head, body))
            
        line = next(lineIter).strip()
        
    # Now convert the rules into derivations.
    while len(rules):
        rule = rules.popleft()
        for options in rule.body:
            completeOptions = sum(option in derivations for option in options)
        if completeOptions == len(options):
            # All of this rule's options are derived so build
            # its derivations.
            print(f"Complete: {rule}, completeOptions == {completeOptions}")
        
    for line in lineIter:
        print(f"in: {line.strip()}")
        
    for rule in rules:
        print(rule)
        
    for derivation in derivations:
        print(derivation)
    
        
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

Day19(TEST.splitlines())
with open("19.txt", "r") as infile:
    Day19(infile.readlines())
