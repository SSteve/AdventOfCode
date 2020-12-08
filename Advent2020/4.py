import re
from typing import Dict, List

TEST = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

TEST2 = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""


passportLineRegex = re.compile(r"([a-z]{3}):(\S*)")
hexColor = re.compile(r"#[a-f0-9]{6}")
passportID = re.compile(r"\d{9}")


class Passport:
    fields: Dict[str, str]

    def __init__(self):
        self.fields = dict()

    def addLine(self, line: str):
        lastMatchPos = 0
        while (match := passportLineRegex.match(line[lastMatchPos:])) is not None:
            self.fields[match[1]] = match[2]
            lastMatchPos += match.span()[1] + 1

    def hasRequiredFields(self, requiredFields: List[str]):
        fieldInFields = [field in self.fields.keys() for field in requiredFields]
        return all(fieldInFields)

    @staticmethod
    def hgtValid(fieldValue: str) -> bool:
        try:
            unitPosition = fieldValue.find('cm')
            if unitPosition > 0:
                height = int(fieldValue[:unitPosition])
                return 150 <= height <= 193
            else:
                unitPosition = fieldValue.find('in')
                height = int(fieldValue[:unitPosition])
                return 59 <= height <= 76
        except ValueError:
            return False

    @staticmethod
    def byrValid(fieldValue: str) -> bool:
        try:
            return 1920 <= int(fieldValue) <= 2002
        except ValueError:
            return False

    @staticmethod
    def eyrValid(fieldValue: str) -> bool:
        try:
            return 2020 <= int(fieldValue) <= 2030
        except ValueError:
            return False

    @staticmethod
    def iyrValid(fieldValue: str) -> bool:
        try:
            return 2010 <= int(fieldValue) <= 2020
        except ValueError:
            return False

    @staticmethod
    def hclValid(fieldValue: str) -> bool:
        match = hexColor.match(fieldValue)
        return len(fieldValue) == 7 and match is not None

    @staticmethod
    def eclValid(fieldValue: str) -> bool:
        return fieldValue in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    @staticmethod
    def pidValid(fieldValue: str) -> bool:
        match = passportID.match(fieldValue)
        return len(fieldValue) == 9 and match is not None

    def fieldIsValid(self, field: str) -> bool:
        fieldValue = self.fields[field]
        if field == "byr":
            return Passport.byrValid(fieldValue)
        if field == 'iyr':
            return Passport.iyrValid(fieldValue)
        if field == 'eyr':
            return Passport.eyrValid(fieldValue)
        if field == 'hgt':
            return Passport.hgtValid(fieldValue)
        if field == 'hcl':
            return Passport.hclValid(fieldValue)
        if field == 'ecl':
            return Passport.eclValid(fieldValue)
        if field == 'pid':
            return Passport.pidValid(fieldValue)
        if field == 'cid':
            return True
        raise("Unknown field")

    def isValid(self, requiredFields: List[str]) -> bool:
        return self.hasRequiredFields(requiredFields) and all(
            self.fieldIsValid(field) for field in requiredFields)

    @staticmethod
    def passportsFromText(lines: List[str]) -> List['Passport']:
        currentPassport = None
        passports = []
        for line in lines:
            passportLine = line.strip()
            if len(passportLine) == 0:
                if currentPassport is not None:
                    passports.append(currentPassport)
                    currentPassport = None
            else:
                if currentPassport is None:
                    currentPassport = Passport()
                currentPassport.addLine(line)
        if currentPassport is not None:
            passports.append(currentPassport)
        return passports


if __name__ == "__main__":
    testPassports = Passport.passportsFromText(TEST.split("\n"))

    requiredFields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    assert sum(passport.hasRequiredFields(requiredFields) for passport in testPassports) == 2,\
        "There should be 2 valid test passports"

    test2Passports = Passport.passportsFromText(TEST2.split("\n"))
    assert sum(passport.isValid(requiredFields) for passport in test2Passports) == 4,\
        "There should be 4 valid test2 passports"

    with open("4.txt", "r") as infile:
        passports = Passport.passportsFromText(infile.read().splitlines())
    validPassportCount = sum(passport.hasRequiredFields(requiredFields) for passport in passports)
    print(validPassportCount)

    validPassports = [passport.isValid(requiredFields) for passport in passports]
    print(sum(validPassports))
