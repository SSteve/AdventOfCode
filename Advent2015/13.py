import re
from itertools import permutations

regex = re.compile(r"(.+) would (lose|gain) (\d+) happiness units by sitting next to (.+)\.")


def groupHappiness(group, arrangements):
    totalHappiness = 0
    for i in range(len(group)):
        totalHappiness += arrangements[(group[i], group[(i + 1) % len(group)])]
        totalHappiness += arrangements[(group[(i + 1) % len(group)], group[i])]
    return totalHappiness


def day13(fileName, addMe=False):
    arrangements = {}
    people = set()
    with open(fileName) as infile:
        for line in infile:
            match = regex.match(line)
            if match:
                # print(match.group(1, 2, 3, 4))
                units = int(match[3])
                if match[2] == "lose":
                    units = -units
                arrangements[(match[1], match[4])] = units
                people.add(match[1])
    if addMe:
        for person in people:
            arrangements[(person, "me")] = 0
            arrangements[("me", person)] = 0
        people.add("me")
    happiness = -1e12
    for group in permutations(people):
        h = groupHappiness(group, arrangements)
        happiness = max(h, happiness)
    return happiness


print(day13("13test.txt"))
print(day13("13.txt"))
print(day13("13.txt", True))
