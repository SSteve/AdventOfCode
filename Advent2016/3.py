def CountValidTriangles(lines: list[str]) -> int:
    result = 0
    for line in lines:
        values = sorted(list(map(int, line.strip().split())))
        if values[0] + values[1] > values[2]:
            result += 1
    return result


def CountValidTriangles2(lines: list[str]) -> int:
    result = 0
    i = 0
    while i < len(lines):
        triangles: list[list[int]] = [[], [], []]
        for _ in range(3):
            values = list(map(int, lines[i].strip().split()))
            for j in range(3):
                triangles[j].append(values[j])
            i += 1
        for j in range(3):
            triangles[j].sort()
            if triangles[j][0] + triangles[j][1] > triangles[j][2]:
                result += 1
    return result


if __name__ == '__main__':
    with open('3.txt', 'r') as infile:
        part1 = CountValidTriangles(infile.read().splitlines())
    print(f"Part 1: {part1}")

    with open('3.txt', 'r') as infile:
        part2 = CountValidTriangles2(infile.read().splitlines())
    print(f"Part 2: {part2}")
