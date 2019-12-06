def day5(fileName):
    offsets = []
    steps = 0
    with open(fileName) as infile:
        for line in infile:
            offsets.append(int(line.strip()))
    instruction = 0
    while instruction >= 0 and instruction < len(offsets):
        offset = offsets[instruction]
        offsets[instruction] += 1
        instruction += offset
        steps += 1
    return steps


def day5b(fileName):
    offsets = []
    steps = 0
    with open(fileName) as infile:
        for line in infile:
            offsets.append(int(line.strip()))
    instruction = 0
    while instruction >= 0 and instruction < len(offsets):
        offset = offsets[instruction]
        delta = -1 if offsets[instruction] >= 3 else 1
        offsets[instruction] += delta
        instruction += offset
        steps += 1
    return steps


if __name__ == "__main__":
    steps = day5("5test.txt")
    print(f"{steps} steps")
    steps = day5b("5test.txt")
    print(f"{steps} for part 2 test")
    steps = day5b("5.txt")
    print(f"{steps} for part 2")