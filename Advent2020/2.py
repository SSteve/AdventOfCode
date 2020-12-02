import re
from dataclasses import dataclass
from typing import List


passwordRegex = re.compile(r"(\d+)-(\d+) (.): (\S+)")


@dataclass
class PasswordSpec:
    lowCount: int
    highCount: int
    letter: str
    password: str

    @staticmethod
    def fromString(raw: str) -> 'PasswordSpec':
        line = raw.strip()
        match = passwordRegex.match(line)
        if match:
            return PasswordSpec(int(match[1]), int(match[2]), match[3], match[4])
        else:
            raise ValueError(f"Couldn't match {line}")

    def isValid1(self) -> bool:
        letterCount = self.password.count(self.letter)
        return self.lowCount <= letterCount <= self.highCount

    def isValid2(self) -> bool:
        return (self.password[self.lowCount - 1] == self.letter) ^ (self.password[self.highCount - 1] == self.letter)


def readPasswords(passwordStrings: List[str]):
    passwords = []
    for line in passwordStrings:
        if len(line.strip()) > 0:
            password = PasswordSpec.fromString(line)
            passwords.append(password)
    return passwords


TEST = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""


if __name__ == "__main__":
    passwords = readPasswords(TEST.split("\n"))
    validCount = sum(password.isValid1() for password in passwords)
    assert validCount == 2, "First test should be 2"
    validCount = sum(password.isValid2() for password in passwords)
    assert validCount == 1, "Second test should be 1"

    with open("2.txt", "r") as infile:
        passwords = readPasswords(infile.readlines())

    validCount = sum(password.isValid1() for password in passwords)
    print(f"Valid1 count: {validCount}")
    validCount = sum(password.isValid2() for password in passwords)
    print(f"Valid2 count: {validCount}")
