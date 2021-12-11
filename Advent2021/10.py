from typing import Tuple

TEST = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


class ChunkError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def IncompleteChunks(line: str) -> list[str]:
    chunkStack: list[str] = []
    pairs: dict[str, str] = {')': '(', ']': '[', '}': '{', '>': '<'}
    for c in line:
        if c in '([{<':
            chunkStack.append(c)
        else:
            if chunkStack.pop() != pairs[c]:
                raise ChunkError(c)
    return chunkStack


def SumSyntaxErrors(lines: list[str]) -> Tuple[int, list[list[str]]]:
    result = 0
    incompleteLines: list[list[str]] = []
    syntaxScores: dict[str, int] = {')': 3, ']': 57, '}': 1197, '>': 25137}
    for line in lines:
        try:
            incompleteChunks = IncompleteChunks(line)
            if len(incompleteChunks):
                incompleteLines.append(incompleteChunks)
        except ChunkError as e:
            result += syntaxScores[e.args[0]]
    return result, incompleteLines


def CompletionScore(line: list[str]) -> int:
    syntaxScores: dict[str, int] = {'(': 1, '[': 2, '{': 3, '<': 4}
    score = 0
    while len(line):
        c = line.pop()
        score = score * 5 + syntaxScores[c]
    return score


def SortedCompletionScores(lines: list[list[str]]) -> list[int]:
    scores: list[int] = []
    for line in lines:
        scores.append(CompletionScore(line))
    return sorted(scores)


if __name__ == "__main__":
    part1, incompleteLines = SumSyntaxErrors(TEST.splitlines())
    assert part1 == 26397
    sortedScores = SortedCompletionScores(incompleteLines)
    part2 = sortedScores[len(sortedScores) // 2]
    assert part2 == 288957

    with open("10.txt", "r") as infile:
        part1, incompleteLines = SumSyntaxErrors(infile.read().splitlines())
    print(f"Part 1: {part1}")
    assert part1 == 339477
    sortedScores = SortedCompletionScores(incompleteLines)
    part2 = sortedScores[len(sortedScores) // 2]
    print(f"Part 2: {part2}")
