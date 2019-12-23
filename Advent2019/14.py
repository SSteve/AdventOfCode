#I couldn't figure this one out so I copied the solution from https://github.com/joelgrus/advent2019/blob/master/day14/day14.py
from __future__ import annotations

import math
import re

from collections import defaultdict
from typing import Iterable, List, NamedTuple, Dict

REACTIONS1 = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""

REACTIONS2 = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""

REACTIONS3 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

REACTIONS4 = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""

REACTIONS5 = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""

class Ingredient(NamedTuple):
    quantity: int
    compound: str

    @staticmethod
    def from_string(raw: str) -> Ingredient:
        qty, compound = raw.strip().split(" ")
        return Ingredient(int(qty), compound)

class Reaction:
    """Describes an individual reaction in a NanoFactory"""
    def __init__(self, reaction_inputs: Iterable[str], output: str):
        self.reaction_inputs = [Ingredient.from_string(inp) for inp in reaction_inputs]
        self.reaction_output = Ingredient.from_string(output)

    def __repr__(self) -> str:
        string_builder: List[str] = []
        for (index, reaction_input) in enumerate(self.reaction_inputs):
            string_builder.append(f"{reaction_input.quantity} {reaction_input.compound}")
            if index < len(self.reaction_inputs) - 1:
                string_builder.append(", ")
        string_builder.append(f" => {self.reaction_output.quantity} {self.reaction_output.compound}")
        return ''.join(string_builder)


class NanoFactory:
    def __init__(self, reaction_strings: Iterable[str]):
        # Sample reaction_string:
        # 10 NXZXH, 7 ZFXP, 7 ZCBM, 7 MHNLM, 1 BDKZM, 3 VQKM => 5 RMZS
        self.reactions: Dict[str, Reaction] = {}
        for reaction in reaction_strings:
            lhs, rhs = reaction.strip().split(" => ")
            inputs = lhs.split(", ")
            reaction = Reaction(inputs, rhs)
            self.reactions[reaction.reaction_output.compound] = reaction

    def least_ore(self, fuel_needed: int = 1):
        requirements = {'FUEL': fuel_needed}
        ore_needed = 0

        def done() -> bool:
            return all(qty <= 0 for qty in requirements.values())

        while not done():
            key = next(iter(chemical for chemical, qty in requirements.items() if qty > 0))
            qty_needed = requirements[key]
            reaction = self.reactions[key]
            num_times = math.ceil(qty_needed / reaction.reaction_output.quantity)
            requirements[key] -= num_times * reaction.reaction_output.quantity

            for ingredient in reaction.reaction_inputs:
                if ingredient.compound == "ORE":
                    ore_needed += ingredient.quantity * num_times
                else:
                    requirements[ingredient.compound] = requirements.get(ingredient.compound, 0) + num_times * ingredient.quantity

        return ore_needed

    def fuel_from_ore(self, available_ore: int = 1_000_000_000_000):
        fuel_lo = 10
        fuel_hi = 1_000_000_000

        while fuel_lo < fuel_hi - 1:
            fuel_mid = (fuel_lo + fuel_hi) // 2
            ore_mid = self.least_ore(fuel_mid)

            if ore_mid <= available_ore:
                fuel_lo = fuel_mid
            else:
                fuel_hi = fuel_mid

        # We've bracketed the fuel amount. Now we need to figure out which one is correct.
        return fuel_hi if self.least_ore(fuel_hi) < available_ore else fuel_lo

        
factory = NanoFactory(REACTIONS1.split("\n"))
assert(factory.reactions['C'].reaction_inputs) == [Ingredient(7, 'A'), Ingredient(1, 'B')]
assert(factory.reactions['D'].reaction_inputs) == [Ingredient(7, 'A'), Ingredient(1, 'C')]
assert(factory.least_ore() == 31)

factory = NanoFactory(REACTIONS2.split("\n"))
assert(factory.least_ore() == 165)

factory = NanoFactory(REACTIONS3.split("\n"))
assert(factory.least_ore() == 13312)
assert(factory.fuel_from_ore() == 82892753)

factory = NanoFactory(REACTIONS4.split("\n"))
assert(factory.least_ore() == 180697)
assert(factory.fuel_from_ore() == 5586022)

factory = NanoFactory(REACTIONS5.split("\n"))
assert(factory.least_ore() == 2210736)
assert(factory.fuel_from_ore() == 460664)

with open("14.txt") as infile:
    factory = NanoFactory(infile)

print(f"Part one: minimum ore required: {factory.least_ore()}")
fuel_from_ore = factory.fuel_from_ore()
print(f"Part two: can make {fuel_from_ore} fuel from a trillion ore")
print(factory.least_ore(fuel_from_ore))