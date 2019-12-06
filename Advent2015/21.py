import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class BattleItem:
    name: str
    cost: int
    damage: int
    armor: int


@dataclass
class Player:
    hitPoints: int
    damage: int
    armor: int
    name: str
    items: List[BattleItem] = field(default_factory=list, compare=False)

    def attack(self, other, shouldPrint=False):
        attackDamage = max(1, self.damage - other.armor)
        other.hitPoints -= attackDamage
        if shouldPrint:
            print(f"The {self.name} deals {self.damage}-{other.armor} = {attackDamage} damage; the {other.name} goes down to {other.hitPoints} hit points.")

    def wield(self, item):
        self.damage += item.damage
        self.armor += item.armor
        self.items.append(item.name)


def startBattle(boss, player, shouldPrint):
    while boss.hitPoints > 0 and player.hitPoints > 0:
        player.attack(boss, shouldPrint)
        if boss.hitPoints > 0:
            boss.attack(player, shouldPrint)
    return player.hitPoints > 0


def readItems(fileName):
    itemRegex = re.compile(r"(\S+)\s*(\d+)\s*(\d+)\s*(\d+)")
    items = []
    with open(fileName) as infile:
        for line in infile:
            match = itemRegex.match(line)
            if match:
                items.append(BattleItem(match[1], int(match[2]), int(match[3]), int(match[4])))
            else:
                raise ValueError(f"Couldn't match {line}")
    return items

def day21(fileName, shouldPrint):
    characteristicRegex = re.compile(r".*: (\d+)")
    with open(fileName) as infile:
        match = characteristicRegex.match(infile.readline())
        bossHitPoints = int(match[1])
        match = characteristicRegex.match(infile.readline())
        bossDamage = int(match[1])
        match = characteristicRegex.match(infile.readline())
        bossArmor = int(match[1])

    weapons = readItems("21weapons.txt")
    armor = readItems("21armor.txt")
    rings = readItems("21rings.txt")

    lowestCost = 1e6
    highestCost = 0
    for weapon in weapons:
        for myArmor in armor:
            for leftRing in rings:
                for rightRing in rings:
                    if leftRing == rightRing:
                        continue
                    boss = Player(bossHitPoints, bossDamage, bossArmor, "boss")
                    me = Player(100, 0, 0, "player")
                    me.wield(weapon)
                    me.wield(myArmor)
                    me.wield(leftRing)
                    me.wield(rightRing)
                    cost = weapon.cost + myArmor.cost + leftRing.cost + rightRing.cost
                    if startBattle(boss, me, shouldPrint):
                        if cost < lowestCost:
                            lowestCost = cost
                            winningItems = me.items[:]
                    else:
                        if cost > highestCost:
                            highestCost = cost
                            losingItems = me.items[:]
                    # else:
                    #     print(f"Player loses with cost of {cost}")
                    # for item in me.items:
                    #     print(f"  - {item}")
    print(f"Lowest winning cost: {lowestCost}")
    for item in winningItems:
        print(f"  - {item}")

    print(f"Highest winning cost: {highestCost}")
    for item in losingItems:
        print(f"  - {item}")



day21("21.txt", False)
