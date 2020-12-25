def FindLoopSize(key: int, subjectNumber: int) -> int:
    value = 1
    loopSize = 0
    while value != key:
        value *= 7
        value = value % 20201227
        loopSize += 1
    return loopSize


def FindEncryptionKey(subjectNumber: int, loopSize: int) -> int:
    value = 1
    for _ in range(loopSize):
        value *= subjectNumber
        value %= 20201227
    return value


with open("25.txt", "r") as infile:
    cardPublicKey = int(infile.readline().strip())
    doorPublicKey = int(infile.readline().strip())

cardLoopSize = FindLoopSize(cardPublicKey, 7)
doorLoopSize = FindLoopSize(doorPublicKey, 7)
cardEncryptionKey = FindEncryptionKey(doorPublicKey, cardLoopSize)
doorEncryptionKey = FindEncryptionKey(cardPublicKey, doorLoopSize)
print(cardEncryptionKey, doorEncryptionKey)
