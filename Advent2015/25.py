import re


def TargetIndex(targetRow: int, targetColumn: int) -> int:
    """
             1   2   3   4   5   6
       ---+---+---+---+---+---+---+
        1 |  1   3   6  10  15  21
        2 |  2   5   9  14  20
        3 |  4   8  13  19
        4 |  7  12  18
        5 | 11  17
        6 | 16
    """
    target_index = (((targetRow + targetColumn - 1) ** 2 +
                    targetRow + targetColumn - 1) // 2) - (targetRow - 1)
    return target_index


def FindCode(targetRow: int, targetColumn: int) -> int:
    """
    const ROW = 3010;
    const COLUMN = 3019;
    const FIRST_CODE = 20151125;
    const TARGET_INDEX = ((Math.pow(ROW + COLUMN - 1, 2) + ROW + COLUMN - 1) / 2) - ((ROW + COLUMN - 1) - COLUMN);

    let result = FIRST_CODE;
    for (var i = 1; i < TARGET_INDEX; i++) {
    result = (result * 252533) % 33554393;
    }
    """
    result = 20151125
    targetIndex = TargetIndex(targetRow, targetColumn)
    for _ in range(1, targetIndex):
        result = (result * 252533) % 33554393

    return result


if __name__ == '__main__':
    with open('25.txt', 'r') as infile:
        match = re.match(
            r"To continue, please consult the code grid in the manual.  Enter the code at row (\d+), column (\d+).",
            infile.readline())
    if match is None:
        raise ValueError("Couldn't parse input.")
    part1 = FindCode(int(match[1]), int(match[2]))
    print(f"Part 1: {part1}")
