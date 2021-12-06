from collections import defaultdict

TEST = "3,4,3,1,2"


def SpawnFish(population: list[str], generations) -> int:
    counts = defaultdict(int)
    for timer in population:
        counts[int(timer)] += 1

    for _ in range(generations):
        newGeneration = defaultdict(int)
        for i in range(8):
            newGeneration[i] = counts[i+1]
        newGeneration[6] += counts[0]
        newGeneration[8] = counts[0]
        counts = newGeneration
    return sum([x for x in counts.values()])


if __name__ == "__main__":
    fishCount = SpawnFish(TEST.split(","), 80)
    assert fishCount == 5934
    fishCount = SpawnFish(TEST.split(","), 256)
    assert fishCount == 26984457539

    with open("6.txt", "r") as infile:
        initialCounts = infile.readline().split(",")
    fishCount = SpawnFish(initialCounts, 80)
    print(f"Part 1: {fishCount}")
    fishCount = SpawnFish(initialCounts, 256)
    print(f"Part 2: {fishCount}")
