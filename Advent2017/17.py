from collections import deque


def day17(stepSize, stopValue, partA):
    buffer = deque([0])
    for insertValue in range(1, stopValue + 1):
        if insertValue % 100_000 == 0:
            print(f"{insertValue:10,}")
        buffer.rotate(-stepSize)
        buffer.append(insertValue)
        pass
    if partA:
        print(buffer[0])
    else:
        print(buffer[(buffer.index(0) + 1) % len(buffer)])


if __name__ == "__main__":
    day17(382, 2017, True)
    day17(382, 50_000_000, False)
