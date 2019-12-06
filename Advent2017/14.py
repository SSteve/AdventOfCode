from collections import namedtuple


def performReverse(numbers, pos, length):
    for i in range(length // 2):
        swapPos1 = (pos + i) % len(numbers)
        swapPos2 = (pos + length - i - 1) % len(numbers)
        numbers[swapPos1], numbers[swapPos2] = numbers[swapPos2], numbers[
            swapPos1]


def knotHash(value):
    skipSize = 0
    pos = 0
    numbers = list(range(256))
    for _ in range(64):
        for i in range(len(value) + 5):
            if i < len(value):
                length = ord(value[i])
            else:
                length = [17, 31, 73, 47, 23][i % len(value)]
            performReverse(numbers, pos, length)
            pos = (pos + length + skipSize) % 256
            skipSize += 1
    denseHash = []
    for i in range(16):
        x = numbers[i * 16]
        for j in range(i * 16 + 1, i * 16 + 16):
            x ^= numbers[j]
        denseHash.append(x)
    hashStr = ""
    for hashval in denseHash:
        hashStr += f"{hashval:02x}"
    return hashStr


Point = namedtuple("Point", ("x", "y"))


def neighbors(point):
    if point.x > 0:
        yield Point(point.x - 1, point.y)
    if point.y > 0:
        yield Point(point.x, point.y - 1)
    if point.x < 127:
        yield Point(point.x + 1, point.y)
    if point.y < 127:
        yield Point(point.x, point.y + 1)


def findConnected(x, y, map):
    point = Point(x, y)
    connected = set([point])
    frontier = [point]
    while frontier:
        point = frontier.pop()
        for neighbor in neighbors(point):
            if neighbor not in connected and map[neighbor.y][neighbor.x] == "1":
                connected.add(neighbor)
                frontier.append(neighbor)
    return connected


def day14(keyString):
    usedBlocks = 0
    map = []
    for i in range(128):
        hashStr = knotHash(f"{keyString}-{i}")
        hash = int(hashStr, base=16)
        binaryString = f"{hash:0128b}"
        print(binaryString)
        usedBlocks += binaryString.count("1")
        map.append(binaryString)

    regionCount = 0
    allRegions = set()
    for x in range(128):
        for y in range(128):
            point = Point(x, y)
            if point not in allRegions and map[y][x] == "1":
                connected = findConnected(x, y, map)
                allRegions = allRegions.union(connected)
                regionCount += 1

    print(f"{keyString} - part1: {usedBlocks}, part2: {regionCount}")


if __name__ == "__main__":
    day14("flqrgnkx")
    day14("wenycdww")

