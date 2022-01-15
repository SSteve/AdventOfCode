from hashlib import md5
from typing import Optional, Tuple

TEST = 'abc'
PUZZLE = 'ffykfhsq'


def passwordCharacter(string: str) -> Optional[str]:
    digest = md5(bytes(string, 'utf-8')).hexdigest()
    if digest[:5] == '00000':
        return digest[5]


def findPassword(string: str) -> str:
    result = ''
    i = 0
    while len(result) < 8:
        nextChar = passwordCharacter(string + str(i))
        if nextChar:
            result += nextChar
        i += 1
    return result


def password2Character(string: str) -> Tuple[int, str]:
    digest = md5(bytes(string, 'utf-8')).hexdigest()
    if digest[:5] == '00000' and int(digest[5], base=16) < 8:
        return int(digest[5]), digest[6]
    return -1, ' '


def findPassword2(string: str) -> str:
    result: list[str] = [' '] * 8
    i = 0
    found = 0
    while found < 8:
        position, nextChar = password2Character(string + str(i))
        if position >= 0 and result[position] == ' ':
            result[position] = nextChar
            print(position, nextChar, result)
            found += 1
        i += 1
        if i % 1000000 == 0:
            print(i)
    return ''.join(result)


assert findPassword(TEST) == '18f47a30'
part1 = findPassword2(TEST)
assert part1 == '05ace8e3'

part1 = findPassword(PUZZLE)
print(f"Part 1: {part1}")
part2 = findPassword2(PUZZLE)
print(f"Part 2: {part2}")
