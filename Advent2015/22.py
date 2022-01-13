from __future__ import annotations
from typing import Callable, Optional


class Spell:
    def __init__(self) -> None:
        self.name = ""
        self.cost: int = 0
        self.start: Optional[Callable] = None
        self.effect: Optional[Callable] = None
        self.end: Optional[Callable] = None
        self.duration = 0


class MagicMissile(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Magic Missile"
        self.cost = 53
        self.start = self.Start

    def Start(self, player: Player, boss: Boss):
        boss.hp -= 4


class Drain(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Drain"
        self.cost = 73
        self.start = self.Start

    def Start(self, player: Player, boss: Boss):
        player.hp += 2
        boss.hp -= 2


class Shield(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Shield"
        self.cost = 113
        self.duration = 6
        self.start = self.Start
        self.end = self.End

    def Start(self, player: Player, boss: Boss):
        player.armor += 7

    def End(self, player: Player, boss: Boss):
        player.armor -= 7


class Poison(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Poison"
        self.cost = 173
        self.duration = 6
        self.effect = self.Effect

    def Effect(self, player: Player, boss: Boss):
        boss.hp -= 3


class Recharge(Spell):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Recharge"
        self.cost = 229
        self.duration = 5
        self.effect = self.Effect

    def Effect(self, player: Player, boss: Boss):
        player.mana += 101


SPELLS: list[Spell] = [
    MagicMissile(), Drain(), Shield(), Poison(), Recharge()]


class Boss:
    def __init__(self, hp: int, damage: int) -> None:
        self.hp = hp
        self.damage = damage

    @classmethod
    def FromFile(cls, lines: list[str]) -> Boss:
        hp = int(lines[0].split()[-1])
        damage = int(lines[1].split()[-1])
        return Boss(hp, damage)

    def __repr__(self) -> str:
        return f"hp: {self.hp}, damage: {self.damage}"

    def Duplicate(self) -> Boss:
        return Boss(self.hp, self.damage)

    def Attack(self, player: Player) -> None:
        if self.hp > 0 and player.hp > 0:
            player.hp -= max(1, self.damage - player.armor)


class Player:
    def __init__(self, hp: int, mana: int, armor: int = 0, spent: int = 0) -> None:
        self.hp = hp
        self.mana = mana
        self.armor = armor
        self.spent = spent

        # Key is spell index. Value is remaining duration.
        self.activeSpells: dict[int, int] = {}

    def __repr__(self) -> str:
        return f"hp: {self.hp}, mana: {self.mana}, armor: {self.armor}"

    def Duplicate(self) -> Player:
        clone = Player(self.hp, self.mana, self.armor, self.spent)
        clone.activeSpells = self.activeSpells.copy()
        return clone

    def CastSpell(self, spellIndex: int, boss: Boss) -> None:
        """
        Cast the spell at the given index.
        """
        if self.hp <= 0 or boss.hp <= 0:
            return
        spell = SPELLS[spellIndex]
        self.mana -= spell.cost
        self.spent += spell.cost
        if spell.duration > 0:
            self.activeSpells[spellIndex] = spell.duration
        if spell.start:
            spell.start(self, boss)

    def ApplyEffects(self, boss: Boss) -> None:
        """
        Apply any spell effects.
        """
        if self.hp <= 0 or boss.hp <= 0:
            return
        for spellIndex in list(self.activeSpells.keys()):
            spell: Spell = SPELLS[spellIndex]
            if spell.effect:
                spell.effect(self, boss)
            if self.activeSpells[spellIndex] > 1:
                self.activeSpells[spellIndex] -= 1
            else:
                # The spell duration is over. Remove it from activeSpells
                # and perform its End action if it exists.
                self.activeSpells.pop(spellIndex)
                if spell.end:
                    spell.end(self, boss)


def PlayGame(player: Player, boss: Boss, lowestCost: int = 2**30, hpPerTurn: int = 0) -> int:
    for spellIndex, spell in enumerate(SPELLS):
        # Can't cast a spell if it's active.
        if spell in player.activeSpells:
            continue
        # Can't cast a spell if it costs more mana than the player has.
        if spell.cost > player.mana:
            continue

        newPlayer = player.Duplicate()
        newBoss = boss.Duplicate()

        newPlayer.hp -= hpPerTurn
        newPlayer.ApplyEffects(newBoss)
        newPlayer.CastSpell(spellIndex, newBoss)
        newPlayer.ApplyEffects(newBoss)
        newBoss.Attack(newPlayer)

        if (newBoss.hp <= 0):
            lowestCost = min(lowestCost, newPlayer.spent)
            continue
        if (newPlayer.hp > 0 and newPlayer.spent < lowestCost):
            lowestCost = PlayGame(newPlayer, newBoss, lowestCost, hpPerTurn)
    return lowestCost


if __name__ == '__main__':
    player = Player(10, 250)
    boss = Boss(13, 8)
    part1 = PlayGame(player, boss)
    assert part1 == 173 + 53

    player = Player(10, 250)
    boss = Boss(14, 8)
    part1 = PlayGame(player, boss)
    assert part1 == 229 + 113 + 73 + 173 + 53

    with open('22.txt', 'r') as infile:
        boss = Boss.FromFile(infile.read().splitlines())

    player = Player(50, 500)
    part1 = PlayGame(player, boss.Duplicate())
    print(f"Part 1: {part1}")  # 953

    player = Player(50, 500)
    part2 = PlayGame(player, boss, hpPerTurn=1)
    print(f"Part 2: {part2}")  # 1289
