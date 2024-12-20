import math
import re
from dataclasses import dataclass

TEST = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

TEST2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


@dataclass(frozen=True)
class Node:
    left: str
    right: str


node_regex = re.compile(r"([A-Z\d]{3}).*([A-Z\d]{3}).*([A-Z\d]{3})")


def count_steps(lines: list[str]) -> int:
    path = lines[0]
    nodes: dict[str, Node] = {}
    for line in lines[2:]:
        match = re.match(node_regex, line)
        nodes[match[1]] = Node(match[2], match[3])

    current_node = "AAA"
    step_count = 0
    current_path_index = 0
    while current_node != "ZZZ":
        if path[current_path_index] == "L":
            current_node = nodes[current_node].left
        else:
            current_node = nodes[current_node].right
        step_count += 1
        current_path_index += 1
        if current_path_index == len(path):
            current_path_index = 0

    return step_count


def count_ghost_steps(lines: list[str]) -> int:
    path = lines[0]
    nodes: dict[str, Node] = {}
    current_nodes: list[str] = []
    for line in lines[2:]:
        match = re.match(node_regex, line)
        nodes[match[1]] = Node(match[2], match[3])
        if match[1][-1] == "A":
            current_nodes.append(match[1])

    # Calculate the cycle length for each of the starting nodes.
    cycle_lengths: list[int] = []
    for node in current_nodes:
        cycle_length = 0
        while node[-1] != "Z":
            if path[cycle_length % len(path)] == "L":
                node = nodes[node].left
            else:
                node = nodes[node].right
            cycle_length += 1
        cycle_lengths.append(cycle_length)

    # The total number of steps is the first time all the cycles line up.
    # (aka the least common multiple.)
    step_count = math.lcm(*cycle_lengths)

    return step_count


if __name__ == "__main__":
    part1test = count_steps(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 2

    part2test = count_ghost_steps(TEST2.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 6

    with open("day8.txt") as infile:
        lines = infile.read().splitlines()

    part1 = count_steps(lines)
    print(f"Part 1: {part1}")
    assert part1 == 22411

    part2 = count_ghost_steps(lines)
    print(f"Part 2: {part2}")
