from collections import Counter

TEST = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""


def decode(lines: list[str], wantLeast=False):
    result = ''
    for i in range(len(lines[0])):
        count = Counter(line[i] for line in lines)
        if wantLeast:
            result += count.most_common()[-1][0]
        else:
            result += count.most_common(1)[0][0]
    return result


part1 = decode(TEST.splitlines())
assert part1 == 'easter'
part2 = decode(TEST.splitlines(), True)
assert part2 == 'advent'

with open('6.txt', 'r') as infile:
    part1 = decode(infile.read().splitlines())
print(f"Part 1: {part1}")


with open('6.txt', 'r') as infile:
    part2 = decode(infile.read().splitlines(), True)
print(f"Part 2: {part2}")
