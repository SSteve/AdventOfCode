from typing import List

TEST1 = """16
10
15
5
1
11
7
19
6
12
4"""

TEST2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""


def MakeValues(valueStrings: List[str]) -> List[int]:
    values = [int(value) for value in valueStrings]
    values.append(0)
    values.append(max(values) + 3)
    values = sorted(values)
    return values
    
    
def Part1(values: List[int]) -> int:
    ones = 0
    threes = 0
    for i in range(1, len(values)):
        difference = values[i] - values[i - 1]
        if difference == 1:
            ones += 1
        elif difference == 3:
            threes += 1
    return ones * threes
    
    
def Part2(values: List[int]) -> int:
    contributions = {1: 1, 2: 1, 3: 2, 4: 4, 5: 7}
    combinations = 1
    groupSize = 1
    previousValue = -3
    for value in values:
        if value - previousValue == 3:
            combinations *= contributions[groupSize]
            groupSize = 1
        else:
            groupSize += 1
        previousValue = value
    return combinations


if __name__ == "__main__":
    test1Values = MakeValues(TEST1.splitlines())
    assert Part1(test1Values) == 35
    assert Part2(test1Values) == 8
    test2Values = MakeValues(TEST2.splitlines())
    assert Part1(test2Values) == 220
    assert Part2(test2Values) == 19208
    with open("10.txt", "r") as infile:
        values = MakeValues(infile.read().splitlines())
    print(f"Part 1: {Part1(values)}")
    print(f"Part 2: {Part2(values)}")
