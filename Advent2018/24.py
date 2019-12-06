import re

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

unitRegex = re.compile(r"(\d+) units each with (\d+) hit points (\(.+\)) with an attack that does (\d+) (\w+) damage at initiative (\d+)")
plainUnitRegex = re.compile(r"(\d+) units each with (\d+) hit points with an attack that does (\d+) (\w+) damage at initiative (\d+)")


class attackType(Enum):
    BLUDGEONING = 1
    COLD = 2
    FIRE = 3
    RADIATION = 4
    SLASHING = 5


attackMap = {
    "bludgeoning": attackType.BLUDGEONING,
    "cold": attackType.COLD,
    "fire": attackType.FIRE,
    "radiation": attackType.RADIATION,
    "slashing": attackType.SLASHING,
}

armyNames = ["Immune system", "Infection"]


@dataclass
class ArmyGroup:
    army: int  # 0 is Immune System, 1 is Infection
    groupID: int  # ID unique in all armies
    groupNumber: int  # Group number within this army
    unitCount: int
    hitPoints: int
    attackDamage: int
    initiative: int
    attackType: attackType
    weaknesses: List[attackType]
    immunities: List[attackType]

    def __lt__(self, other):
        selfPower = self.unitCount * self.attackDamage
        otherPower = other.unitCount * other.attackDamage
        return selfPower < otherPower or \
            selfPower == otherPower and self.initiative < other.initiative


def groupWithID(armies: List[ArmyGroup], ID: int):
    for group in armies:
        if group.groupID == ID:
            return group
    return None


def parseSpecs(specs: str) -> (List[attackType], List[attackType]):
    immunities = []
    weaknesses = []
    splitSpec = specs.split(';')
    for spec in splitSpec:
        if "weak" in spec:
            currentList = weaknesses
        elif "immune" in spec:
            currentList = immunities
        for word in spec.split(" "):
            word = word.strip('(,)')
            if word in attackMap:
                currentList.append(attackMap[word])
    return weaknesses, immunities


def targetPhase(armies: List[ArmyGroup], shouldPrint) -> Dict[ArmyGroup, Optional[ArmyGroup]]:
    if shouldPrint:
        for group in armies:
            print(f"{armyNames[group.army]} group {group.groupNumber} contains {group.unitCount} units")
        print()
    availableTargets = [[group for group in armies if group.army == 0],
                        [group for group in armies if group.army == 1]]
    targeting = {}
    for group in sorted(armies, reverse=True):
        targetGroup = None
        maximumDamage = -1
        for potentialTarget in availableTargets[1 - group.army]:
            if group.attackType in potentialTarget.immunities:
                continue  # Don't consider a group immune to this group's attack type
            effectivePower = group.unitCount * group.attackDamage
            if group.attackType in potentialTarget.weaknesses:
                effectivePower *= 2
            if shouldPrint:
                print(f"{armyNames[group.army]} group {group.groupNumber} would deal defending group {potentialTarget.groupNumber} {effectivePower} damage")
            if effectivePower > maximumDamage or effectivePower == maximumDamage and potentialTarget > targetGroup:
                targetGroup = potentialTarget
                maximumDamage = effectivePower
        if targetGroup is not None:
            # print(f"   chose group {targetGroup.groupNumber}")
            targeting[group.groupID] = targetGroup
            availableTargets[1 - group.army].remove(targetGroup)
    if shouldPrint:
        print()
    return targeting


def attackPhase(armies: List[ArmyGroup], targeting: Dict[int, ArmyGroup], shouldPrint: bool) -> None:
    for attackingGroup in sorted(armies, key=lambda group: group.initiative, reverse=True):
        if attackingGroup.unitCount <= 0 or attackingGroup.groupID not in targeting:
            continue
        attackedGroup = targeting[attackingGroup.groupID]
        effectivePower = attackingGroup.unitCount * attackingGroup.attackDamage
        if attackingGroup.attackType in attackedGroup.weaknesses:
            effectivePower *= 2
        unitsKilled = min(effectivePower // attackedGroup.hitPoints, attackedGroup.unitCount)
        if shouldPrint:
            print(f"{armyNames[attackingGroup.army]} group {attackingGroup.groupNumber} attacks defending group {attackedGroup.groupNumber}, killing {unitsKilled} units")
        attackedGroup.unitCount -= unitsKilled
    for group in armies[:]:
        if group.unitCount <= 0:
            armies.remove(group)
    if shouldPrint:
        print()


def countGroups(armies):
    counts = {0: 0, 1: 0}
    for group in armies:
        counts[group.army] += 1
    return (counts[0], counts[1])


def a24(fileName, attackBoost, shouldPrint):
    armies: List[ArmyGroup] = []
    groupID = 0
    groupNumbers = {0: 1, 1: 1}
    with open(fileName, "r") as infile:
        for line in infile:
            if "Immune System" in line:
                currentArmy = 0
                # print("Immune System:")
                continue
            if "Infection" in line:
                currentArmy = 1
                # print("Infection")
                continue
            match = unitRegex.match(line)
            if match:
                unitCount = int(match[1])
                hitPoints = int(match[2])
                specs = match[3]
                attackDamage = int(match[4])
                attackType = attackMap[match[5]]
                initiative = int(match[6])
            else:
                match = plainUnitRegex.match(line)
                if match:
                    unitCount = int(match[1])
                    hitPoints = int(match[2])
                    specs = ""
                    attackDamage = int(match[3])
                    attackType = attackMap[match[4]]
                    initiative = int(match[5])
                else:
                    continue
            weaknesses, immunities = parseSpecs(specs)
            if currentArmy == 0:
                attackDamage += attackBoost
            group = ArmyGroup(currentArmy, groupID, groupNumbers[currentArmy], unitCount, hitPoints, attackDamage, initiative,
                              attackType, weaknesses, immunities)
            armies.append(group)
            groupID += 1
            groupNumbers[currentArmy] += 1
    (immuneGroupCount, infectionGroupCount) = countGroups(armies)
    while immuneGroupCount > 0 and infectionGroupCount > 0:
        targeting = targetPhase(armies, shouldPrint)
        attackPhase(armies, targeting, shouldPrint)
        (immuneGroupCount, infectionGroupCount) = countGroups(armies)
    print(f"{armyNames[armies[0].army]} has {sum([group.unitCount for group in armies])} armies")
    return armies


if __name__ == "__main__":
    # Boosts of 83-87 cause a stalemate
    largestLoss = 83
    smallestWin = 85
    while smallestWin - largestLoss > 1:
        boost = (smallestWin + largestLoss) // 2
        print(f"Trying {boost}")
        armies = a24("24.txt", boost, False)
        if armies[0].army == 1:
            largestLoss = boost
        else:
            smallestWin = boost

