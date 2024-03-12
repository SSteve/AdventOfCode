from collections import deque
from dataclasses import dataclass
from enum import Enum

TEST = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

TEST2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


class ModuleType(Enum):
    FLIP_FLOP = 1
    CONJUNCTION = 2
    BROADCAST = 3

    @staticmethod
    def from_character(c: str):
        match c:
            case "%":
                return ModuleType.FLIP_FLOP
            case "&":
                return ModuleType.CONJUNCTION
            case "b":
                return ModuleType.BROADCAST
        raise ValueError(f"Unexpected character for ModuleType: {c}.")


@dataclass
class Module:
    type: ModuleType
    targets: list[str]
    status: bool
    inputs: dict[str, int]


@dataclass(frozen=True)
class Signal:
    source: str
    target: str
    status: bool


def build_network(lines: list[str]) -> dict[str, Module]:
    network: dict[str, Module] = {}
    # Create the modules.
    for line in lines:
        name, target_list = line.split(" -> ")
        module_type = ModuleType.from_character(name[0])
        if module_type != ModuleType.BROADCAST:
            name = name[1:]
        network[name] = Module(module_type, list(target_list.split(", ")), False, {})

    # Create the inputs for the conjunction modules.
    for name, module in network.items():
        for target in module.targets:
            if target in network and network[target].type == ModuleType.CONJUNCTION:
                network[target].inputs[name] = False

    return network


def all_flip_flops_low(network: dict[str, Module]) -> bool:
    for module in network.values():
        if module.type == ModuleType.CONJUNCTION:
            continue
        if module.status:
            return False
    return True


def tally_pulses(lines: list[str]) -> int:
    network = build_network(lines)
    # Set the broadcaster status to True so that the modules aren't all False when we
    # start the while loop.
    network["broadcaster"].status = True
    rounds: list[dict[bool, int]] = []
    signals: deque[Signal] = deque()

    while all_flip_flops_low(network) is False and len(rounds) < 1000:
        round: dict[bool, int] = {True: 0, False: 0}

        broadcaster = network["broadcaster"]
        broadcaster.status = False
        # The button sends a low signal to broadcaster.
        round[False] += 1
        for target in broadcaster.targets:
            # The broadcaster sends a low signal to each of its targets.
            round[False] += 1
            signals.append(Signal(None, target, False))

        while signals:
            signal = signals.popleft()
            if signal.target not in network:
                continue
            signal_target = network[signal.target]
            if signal_target.type == ModuleType.FLIP_FLOP:
                # Flip-flops ignore True signals. If the signal is False, it negates its value
                # and sends that value to its targets.
                if signal.status is False:
                    signal_target.status = not signal_target.status
                    for target in signal_target.targets:
                        round[signal_target.status] += 1
                        signals.append(Signal(signal.target, target, signal_target.status))
            elif signal_target.type == ModuleType.CONJUNCTION:
                signal_target.inputs[signal.source] = signal.status
                signal_target.status = not all(status for status in signal_target.inputs.values())
                for target in signal_target.targets:
                    round[signal_target.status] += 1
                    signals.append(Signal(signal.target, target, signal_target.status))
            else:
                raise ValueError(f"Unexpected module type: {signal_target.type}")

        rounds.append(round)

    even_multiples = 1000 // len(rounds)
    highs = sum(r[True] for r in rounds) * even_multiples
    lows = sum(r[False] for r in rounds) * even_multiples
    extras = 1000 % len(rounds)
    if extras:
        highs += sum(r[True] for r in rounds[:extras])
        lows += sum(r[False] for r in rounds[:extras])
    total = highs * lows
    return total


if __name__ == "__main__":
    part1test = tally_pulses(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 32000000

    part1test = tally_pulses(TEST2.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 11687500

    """ 
    part2test = run_cycles(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 64
 """
    with open("day20.txt") as infile:
        lines = infile.read().splitlines()

    part1 = tally_pulses(lines)
    print(f"Part 1: {part1}")
    # assert part1 == 103614

    """ 
    part2 = run_cycles(lines)
    print(f"Part 2: {part2}")
 """
