from datetime import datetime
from functools import lru_cache
from hashlib import md5
from typing import Callable


def GetMd5(value: str) -> str:
    return md5(bytes(value, 'utf-8')).hexdigest()


@lru_cache(maxsize=None)
def GetHash(salt: str, value: int) -> str:
    hash = GetMd5(salt + str(value))
    return hash


@lru_cache(maxsize=None)
def GetStretchedHash(salt: str, value: int) -> str:
    hash = GetMd5(salt + str(value))
    for _ in range(2016):
        hash = GetMd5(hash)
    return hash


@lru_cache(maxsize=None)
def TripletCharacter(hash: str) -> str:
    """
    Return the first character that occurs three consecutive times
    in the hash string. If no character occurs three consecutive
    times, return the empty string.
    """
    firstIndex = -1  # The first position of a triplet.
    for i in range(16):
        triplet = hex(i)[-1] * 3
        index = hash.find(triplet)
        if index >= 0 and (firstIndex == -1 or index < firstIndex):
            firstIndex = index
    if firstIndex >= 0:
        return hash[firstIndex]
    else:
        return ""


@lru_cache(maxsize=None)
def ContainsQuintuplet(hash: str, character: str) -> bool:
    quintuplet = character * 5
    if hash.find(quintuplet) >= 0:
        return True
    return False


def QuintupletInNextThousand(salt: str, index: int, character: str,
                             hashAlgorithm) -> bool:
    for testIndex in range(index, index+1000):
        if ContainsQuintuplet(hashAlgorithm(salt, testIndex), character):
            return True
    return False


def FindKey(salt: str, hashAlgorithm: Callable) -> int:
    found = 0
    index = 0
    while found < 64:
        repeatedCharacter = TripletCharacter(hashAlgorithm(salt, index))
        if len(repeatedCharacter) > 0:
            if QuintupletInNextThousand(salt, index + 1, repeatedCharacter,
                                        hashAlgorithm):
                found += 1
        if found < 64:
            index += 1
    return index


if __name__ == '__main__':
    assert GetStretchedHash('abc', 0) == 'a107ff634856bb300138cac6568c0f24'
    assert TripletCharacter(GetStretchedHash('abc', 5)) == '2'
    assert not QuintupletInNextThousand('abc', 6, '2', GetStretchedHash)
    assert TripletCharacter(GetStretchedHash('abc', 10)) == 'e'
    assert QuintupletInNextThousand('abc', 11, 'e', GetStretchedHash)

    start = datetime.now()
    part1 = FindKey('abc', GetHash)
    assert part1 == 22728

    GetHash.cache_clear()
    TripletCharacter.cache_clear()
    ContainsQuintuplet.cache_clear()

    part1 = FindKey('cuanljph', GetHash)
    print(f"Part 1: {part1}")
    end = datetime.now()
    print(f"Part 1 total time: {end - start}")

    GetHash.cache_clear()
    TripletCharacter.cache_clear()
    ContainsQuintuplet.cache_clear()
    GetStretchedHash.cache_clear()

    start = datetime.now()
    part2 = FindKey('abc', GetStretchedHash)
    assert part2 == 22551

    GetHash.cache_clear()
    TripletCharacter.cache_clear()
    ContainsQuintuplet.cache_clear()
    GetStretchedHash.cache_clear()

    part2 = FindKey('cuanljph', GetStretchedHash)
    print(f"Part 2: {part2}")
    end = datetime.now()
    print(f"Total time: {end - start}")
