from functools import reduce
from itertools import combinations


def FindBestGroup(weights, numberOfGroups):
    targetWeight = sum(weights) / numberOfGroups
    entanglement = 0
    for i in range(len(weights)):
        for combination in combinations(weights, i + 1):
            if sum(combination) == targetWeight:
                # The first one we find is the best group because we're looking at the smallest
                # groups first and are sorted in ascending order.
                entanglement = reduce(lambda x, y: x * y, combination, 1)
                break
        if entanglement != 0:
            break
    return entanglement


if __name__ == '__main__':
    with open("24.txt", "r") as infile:
        weights = list(map(int, infile.readlines()))
    part1 = FindBestGroup(weights, 3)
    print(f"Part 1: {part1}")
    part2 = FindBestGroup(weights, 4)
    print(f"Part 2: {part2}")
