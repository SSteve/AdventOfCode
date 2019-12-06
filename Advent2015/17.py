from itertools import combinations, permutations


def day17(fileName, liters):
    sizes = []
    with open(fileName) as infile:
        for line in infile:
            sizes.append(int(line.strip()))

    validCombinations = 0
    lowestCombinationCount = None
    for i in range(len(sizes)):
        combinationCount = 0
        for c in combinations(sizes, i + 1):
            if sum(c) == liters:
                validCombinations += 1
                combinationCount += 1
        if lowestCombinationCount is None and combinationCount > 0:
            lowestCombinationCount = combinationCount
    return validCombinations, lowestCombinationCount


print(day17("17test.txt", 25))
print(day17("17.txt", 150))
