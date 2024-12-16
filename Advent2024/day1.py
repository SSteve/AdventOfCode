TEST = """3   4
4   3
2   5
1   3
3   9
3   3"""


def sum_distances(lines: list[str]) -> int:
    left = []
    right = []
    for line in lines:
        (a, b) = line.split()
        left.append(int(a))
        right.append(int(b))
    left.sort()
    right.sort()
    distances = 0
    for a, b in zip(left, right):
        distances += abs(a - b)
    return distances


def sum_similarities(lines: list[str]) -> int:
    left = []
    right = []
    for line in lines:
        (a, b) = line.split()
        left.append(int(a))
        right.append(int(b))

    similarities = 0
    for left_val in left:
        similarities += left_val * right.count(left_val)
    return similarities


if __name__ == "__main__":
    part1test = sum_distances(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 11

    part2test = sum_similarities(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 31

    with open("day1.txt") as infile:
        lines = infile.read().splitlines()

    part1 = sum_distances(lines)
    print(f"Part 1: {part1}")

    part2 = sum_similarities(lines)
    print(f"Part 2: {part2}")
