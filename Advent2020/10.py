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


def Part1(valueStrings):
    values = [int(value) for value in valueStrings]
    values.append(0)
    values.append(max(values) + 3)
    values = sorted(values)
    ones = 0
    threes = 0
    for i in range(1, len(values)):
        difference = values[i] - values[i - 1]
        if difference == 1:
            ones += 1
        elif difference == 3:
            threes += 1
    return ones * threes


if __name__ == "__main__":
    assert Part1(TEST1.splitlines()) == 35
    assert Part1(TEST2.splitlines()) == 220
    with open("10.txt", "r") as infile:
        values = infile.read().splitlines()
    print(f"Part 1: {Part1(values)}")
