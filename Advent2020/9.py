from itertools import combinations
from typing import List

TEST1 = """20
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
1
21
22
23
24
25
45"""

TEST2 = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""


def IsValid(target: int, startIndex: int, preambleSize: int, values: List[int]) -> bool:
    for a, b in combinations(values[startIndex:startIndex + preambleSize], 2):
        if a + b == target:
            return True
    return False


def Part1(preambleSize: int, values: List[int]) -> int:
    for index in range(len(values) - preambleSize):
        targetValue = values[index + preambleSize]
        if IsValid(targetValue, index, preambleSize, values) is False:
            return targetValue


def Part2(targetValue: int, values: List[int]) -> int:
    for index in range(len(values)):
        for index2 in range(index, len(values)):
            rangeSum = sum(values[index:index2])
            if rangeSum == targetValue:
                return max(values[index:index2]) + min(values[index:index2])
            if rangeSum > targetValue:
                break
    return -1


if __name__ == "__main__":
    test1Values = [int(val) for val in TEST1.splitlines()]
    assert IsValid(26, 0, 25, test1Values)
    assert IsValid(49, 0, 25, test1Values)
    assert IsValid(100, 0, 25, test1Values) is False
    assert IsValid(50, 0, 25, test1Values) is False
    assert IsValid(26, 1, 25, test1Values)
    assert IsValid(65, 1, 25, test1Values) is False
    assert IsValid(64, 1, 25, test1Values)
    assert IsValid(66, 1, 25, test1Values)

    test2Values = [int(val) for val in TEST2.splitlines()]
    testPart1 = Part1(5, test2Values)
    assert testPart1 == 127
    testPart2 = Part2(testPart1, test2Values)
    assert testPart2 == 62, f"Part 2 is {testPart2}. Should be 62."

    with open("9.txt", "r") as infile:
        values = [int(val) for val in infile.read().splitlines()]
    part1 = Part1(25, values)
    assert part1 == 2089807806, f"Part 1 is broken. It's {part1} but it should be 2089807806."
    print(f"Part 1: {part1}")
    print(f"Part 2: {Part2(part1, values)}")
