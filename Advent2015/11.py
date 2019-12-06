pwNextLetters = "abcdefghjkmnpqrstuvwxyz"  # The next letter after a valid letter
pwInvalidNextLetters = "ijlmop"  # The next letter after an invalid letter
pwInvalidLetters = "ilo"


def nextLetter(letter):
    sequenceForNext = pwNextLetters if letter not in pwInvalidLetters else pwInvalidNextLetters
    letterPos = sequenceForNext.index(letter)
    if letterPos < len(sequenceForNext) - 1:
        return sequenceForNext[letterPos + 1]
    return None


def nextPassword(pwString):
    pw = [letter for letter in pwString]
    letterIndex = -1
    while pw[letterIndex] == "z":
        pw[letterIndex] = "a"
        letterIndex -= 1
    pw[letterIndex] = nextLetter(pw[letterIndex])
    return ''.join(pw)


def pwIsValid(pw):
    if "i" in pw or "l" in pw or "o" in pw:
        return False
    pairs = set()
    i = 0
    while i < len(pw) - 1:
        if pw[i] == pw[i + 1]:
            pairs.add(pw[i])
            i += 1  # Skip the matching letter. The matching pairs can't overlap
        i += 1
    if len(pairs) < 2:
        return False
    foundTrio = False
    i = 0
    while not foundTrio and i < len(pw) - 2:
        foundTrio = ord(pw[i+1]) == ord(pw[i]) + 1 and ord(pw[i+2]) == ord(pw[i+1]) + 1
        i += 1
    return foundTrio


def day11(input):
    pw = nextPassword(input)
    while not pwIsValid(pw):
        pw = nextPassword(pw)
    return pw


print(day11("abcdefgh"))
print(day11("ghjaaaaa"))
next = (day11("cqjxjnds"))
print(next)
print(day11(next))
