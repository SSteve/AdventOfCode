from collections import defaultdict
from typing import Dict, List

TEST = """abc

a
b
c

ab
ac

a
a
a
a

b"""

def ReadForms(formLines: List[str]) -> List:
    groups: List[(int, Dict)] = []
    
    form = defaultdict(int)
    formCount = 0
    for formLine in formLines:
        if len(formLine) == 0:
            groups.append((formCount, form))
            form = defaultdict(int)
            formCount = 0
        else:
            formCount += 1
            for answer in formLine:
                form[answer] += 1
    if formCount > 0:
        groups.append((formCount, form))
    return groups
        
    
testGroups = ReadForms(TEST.splitlines())
testAnswer = sum(len(group[1].keys()) for group in testGroups)
assert testAnswer == 11, f"Test answer is {testAnswer}. It should be 11."
testAnswer2 = 0
for count, group in testGroups:
    for letter in group:
        if group[letter] == count:
            testAnswer2 += 1
assert testAnswer2 == 6, f"Test answer 2 is {testAnswer2}. It should be 6."
        

with open("6.txt", "r") as infile:
    groups = ReadForms(infile.read().splitlines())
for count, group in groups:
    print(f"count: {count} keys: {group.keys()}")
answer = sum(len(group[1].keys()) for group in groups)
print(answer)

answer2 = 0
for count, group in groups:
    for letter in group:
        if group[letter] == count:
            answer2 += 1
print(f"Part 2: {answer2}")

