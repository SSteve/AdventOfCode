
TEST = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def CountUniquePatterns(lines: list[str]) -> int:
    count = 0
    for line in lines:
        outputValues = line.split("|")[1].split()
        for outputValue in outputValues:
            valueLen = len(outputValue)
            if valueLen == 2 or valueLen == 4 or valueLen == 3 or valueLen == 7:
                count += 1
    return count


def MapSegments(uniqueValues: list[str]) -> dict[str, str]:
    result = {}

    one = set(next(v for v in uniqueValues if len(v) == 2))
    seven = set(next(v for v in uniqueValues if len(v) == 3))
    four = set(next(v for v in uniqueValues if len(v) == 4))
    # The 'a' segment is the one in the digit seven that isn't in the digit one.
    aSegment = (seven - one).pop()
    result[aSegment] = 'a'

    # Make sets of all the segment lists.
    values = [set(v) for v in uniqueValues]
    # Remove the 'a' segment from each set.
    for v in values:
        v.discard(aSegment)

    # The 'b', 'c', 'e', and 'f' segments can be identified by their unique count.
    # 'd' and 'g' both occur seven times so we'll make a set containing both of those.
    # We will distinguish 'd' from 'g' by removing all the identified segments from the
    # digit four.
    dOrG = set()
    for c in 'abcdefg':
        letterCount = sum(c in v for v in values)
        if letterCount == 4:
            result[c] = 'e'
        elif letterCount == 6:
            result[c] = 'b'
            four.discard(c)
        elif letterCount == 7:
            dOrG.add(c)
        elif letterCount == 8:
            result[c] = 'c'
            four.discard(c)
        elif letterCount == 9:
            result[c] = 'f'
            four.discard(c)
    # The segment remaining in four is d. After discarding it from dOrG
    # the remaining segment in dOrG is g.
    dSegment = four.pop()
    dOrG.discard(dSegment)
    gSegment = dOrG.pop()
    result[dSegment] = 'd'
    result[gSegment] = 'g'
    return result


def IdentifyDigit(map: dict[str, str], segments: str) -> int:
    mappedSegments = set()
    for c in segments:
        mappedSegments.add(map[c])
    if mappedSegments == set('abcefg'):
        return 0
    if mappedSegments == set('cf'):
        return 1
    if mappedSegments == set('acdeg'):
        return 2
    if mappedSegments == set('acdfg'):
        return 3
    if mappedSegments == set('bcdf'):
        return 4
    if mappedSegments == set('abdfg'):
        return 5
    if mappedSegments == set('abdefg'):
        return 6
    if mappedSegments == set('acf'):
        return 7
    if mappedSegments == set('abcdefg'):
        return 8
    if mappedSegments == set('abcdfg'):
        return 9
    raise ValueError(f"Can't identify {mappedSegments}")


def AddOutputValues(lines: list[str]) -> int:
    result = 0
    for line in lines:
        splitLine = line.split("|")
        segmentMap = MapSegments(splitLine[0].split())
        lineValue = 0
        for segments in splitLine[1].split():
            lineValue = lineValue * 10 + IdentifyDigit(segmentMap, segments)
        result += lineValue

    return result


if __name__ == "__main__":
    part1 = CountUniquePatterns(TEST.splitlines())
    assert part1 == 26
    part2 = AddOutputValues(TEST.splitlines())
    assert part2 == 61229

    with open("8.txt", "r") as infile:
        lines = infile.read().splitlines()
    part1 = CountUniquePatterns(lines)
    part2 = AddOutputValues(lines)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
