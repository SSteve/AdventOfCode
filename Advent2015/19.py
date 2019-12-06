import re
from collections import defaultdict


def day19(fileName):
    substitutionRegex = re.compile(r"(.+) => (.+)")
    substitutions = defaultdict(list)
    with open(fileName) as infile:
        for inputLine in (line.strip() for line in infile):
            match = substitutionRegex.match(inputLine)
            if match:
                substitutions[match[1]].append(match[2])
                continue
            if len(inputLine) > 0:
                molecule = inputLine

    newMolecules = set()
    for substituted in substitutions:
        foundPosition = 0
        lastSubstitutedLength = 0
        for _ in range(molecule.count(substituted)):
            searchPosition = foundPosition + lastSubstitutedLength
            lastSubstitutedLength = len(substituted)
            foundPosition = molecule.find(substituted, searchPosition)
            for sub in substitutions[substituted]:
                newMolecule = f"{molecule[:foundPosition]}{sub}{molecule[foundPosition + lastSubstitutedLength:]}"
                newMolecules.add(newMolecule)
    return newMolecules


molecules = day19("19.txt")
print(len(molecules))
