from collections import defaultdict
from typing import Dict, List, Tuple

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
    groups: List[Tuple[int, Dict[str, int]]] = []
    
    group = defaultdict(int)
    formCount = 0
    for formLine in formLines:
        if len(formLine) == 0:
            groups.append((formCount, group))
            group = defaultdict(int)
            formCount = 0
        else:
            formCount += 1
            for answer in formLine:
                group[answer] += 1
    if formCount > 0:
        # We got to the end of the file while still evaluating a group.
        groups.append((formCount, group))
    return groups
    
def CountAny(groups: List[Tuple[int, Dict[str, int]]]) -> int:
    # Return the sum of the total number of letters in each group.
    return sum(len(group[1].keys()) for group in groups)
    
def CountAll(groups: List[Tuple[int, Dict[str, int]]]) -> int:
    # Return the sum of the number of letters that appeared on
    # every form in the group.
    total = 0
    for count, group in groups:
        total += sum(group[letter] == count for letter in group)
    return total
    
testGroups = ReadForms(TEST.splitlines())
testAnswer = CountAny(testGroups)
assert testAnswer == 11, f"Test answer is {testAnswer}. It should be 11."
testAnswer2 = CountAll(testGroups)
assert testAnswer2 == 6, f"Test answer 2 is {testAnswer2}. It should be 6."
        

with open("6.txt", "r") as infile:
    groups = ReadForms(infile.read().splitlines())
answer = CountAny(groups)
print(f"Part 1: {answer}")

answer2 = CountAll(groups)
print(f"Part 2: {answer2}")

