from collections import Counter
from operator import itemgetter

TEST = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""


def parseLine(line: str):
    checksum = line[-6:-1]
    pieces = line[:-7].split('-')
    letters = ''.join(pieces[:-1])
    sectorId = int(pieces[-1])
    return letters, checksum, sectorId


def roomIsValid(letters, checksum) -> bool:
    counts = Counter(letters)
    ordered = sorted(list(counts.items()), key=itemgetter(0))
    ordered = sorted(ordered, key=itemgetter(1), reverse=True)
    return ''.join(orderedItem[0] for orderedItem in ordered[:5]) == checksum


def sumValidRooms(lines) -> int:
    result = 0
    for line in lines:
        letters, checksum, sectorId = parseLine(line)
        assert 100 <= sectorId <= 999
        if roomIsValid(letters, checksum):
            result += sectorId
    return result


def shiftedLetter(letter, shift):
    value = ord(letter) - ord('a')
    newValue = (value + shift) % 26
    return chr(newValue + ord('a'))


def shiftedRoomName(text, sectorId):
    result = ''
    for ch in text:
        if ch == '-':
            result += ' '
        else:
            result += shiftedLetter(ch, sectorId)
    return result


def printValidRooms(lines) -> None:
    roomNames = []
    for line in lines:
        letters, checksum, sectorId = parseLine(line)
        if roomIsValid(letters, checksum):
            roomNames.append((shiftedRoomName(line[:-10], sectorId), sectorId))
    roomNames.sort()
    for i in roomNames:
        print(i[0], i[1])


if __name__ == "__main__":
    part1 = sumValidRooms(TEST.splitlines())
    assert part1 == 1514

    with open('4.txt', 'r') as infile:
        part1 = sumValidRooms(infile.read().splitlines())
    print(f"Part 1: {part1}")
    with open('4.txt', 'r') as infile:
        printValidRooms(infile.read().splitlines())
