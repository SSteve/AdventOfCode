import re

from dataclasses import dataclass
from typing import Iterable

TEST = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

blueprint_regex = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. " +
    r"Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")


@dataclass(frozen=True)
class RobotState:
    minute: int
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int
    ore: int
    clay: int
    obsidian: int
    geode: int


class Blueprint:
    def __init__(self, blueprint_text: str) -> None:
        blueprint_match = blueprint_regex.match(blueprint_text)
        if blueprint_match is None:
            raise ValueError(f"Invalid blueprint: {blueprint_text}")
        self.blueprint_number = int(blueprint_match[1])
        self.ore_robot_cost = int(blueprint_match[2])
        self.clay_robot_cost = int(blueprint_match[3])
        self.obsidian_robot_ore_cost = int(blueprint_match[4])
        self.obsidian_robot_clay_cost = int(blueprint_match[5])
        self.geode_robot_ore_cost = int(blueprint_match[6])
        self.geode_robot_obsidian_cost = int(blueprint_match[7])
        self.state = RobotState(0, 1, 0, 0, 0, 0, 0, 0, 0)

    def successors(self, state: RobotState) -> Iterable[RobotState]:
        if state.ore >= self.ore_robot_cost:

    def __repr__(self) -> str:
        return f"Blueprint {self.blueprint_number}: " + \
            f"Each ore robot costs {self.ore_robot_cost} ore. " + \
            f"Each clay robot costs {self.clay_robot_cost} ore. " + \
            f"Each obsidian robot costs {self.obsidian_robot_ore_cost} ore and {self.obsidian_robot_clay_cost} clay. " + \
            f"Each geode robot costs {self.geode_robot_ore_cost} ore and {self.geode_robot_obsidian_cost} obsidian."

    def successors(self, state: RobotState)


if __name__ == "__main__":
    blueprints = [Blueprint(line) for line in TEST.splitlines()]
    for blueprint in blueprints:
        print(blueprint)

    with open("day19.txt") as infile:
        blueprints = [Blueprint(line) for line in infile.read().splitlines()]
    for blueprint in blueprints:
        print(blueprint)
