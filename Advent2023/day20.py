from collections import deque
from dataclasses import dataclass
from enum import Enum
from math import lcm

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
    rx_status = None

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

    print(f"{len(rounds)} rounds")
    even_multiples = 1000 // len(rounds)
    highs = sum(r[True] for r in rounds) * even_multiples
    lows = sum(r[False] for r in rounds) * even_multiples
    extras = 1000 % len(rounds)
    if extras:
        highs += sum(r[True] for r in rounds[:extras])
        lows += sum(r[False] for r in rounds[:extras])
    total = highs * lows
    return total


def presses_until_rx_low(lines: list[str]) -> int:
    # This brute force method never finishes.
    network = build_network(lines)
    # Set the broadcaster status to True so that the modules aren't all False when we
    # start the while loop.
    network["broadcaster"].status = True
    button_presses: int = 0
    signals: deque[Signal] = deque()
    high_inputs: dict[str, int] = {}
    rx_status = True

    while rx_status and len(high_inputs) < 4:
        # Press the button.
        broadcaster = network["broadcaster"]
        button_presses += 1
        if button_presses % 1000000 == 0:
            print(button_presses)
        for target in broadcaster.targets:
            signals.append(Signal(None, target, False))

        while signals:
            signal = signals.popleft()
            if signal.target == "rx" and signal.status is False:
                rx_status = False
                continue
            if signal.target not in network:
                continue

            signal_target = network[signal.target]
            if signal_target.type == ModuleType.FLIP_FLOP:
                # Flip-flops ignore True signals. If the signal is False, it negates its value
                # and sends that value to its targets.
                if signal.status is False:
                    signal_target.status = not signal_target.status
                    for target in signal_target.targets:
                        signals.append(Signal(signal.target, target, signal_target.status))
            elif signal_target.type == ModuleType.CONJUNCTION:
                signal_target.inputs[signal.source] = signal.status
                signal_target.status = not all(status for status in signal_target.inputs.values())
                for target in signal_target.targets:
                    signals.append(Signal(signal.target, target, signal_target.status))
            else:
                raise ValueError(f"Unexpected module type: {signal_target.type}")

        for input in ("pk", "hf", "mk", "pm"):
            if network[input].status and input not in high_inputs:
                print(f"{input} high at button press {button_presses}.")
                high_inputs[input] = button_presses

    if rx_status:
        button_presses = lcm(high_inputs.values())

    return button_presses


def show_values(lines: list[str]):
    network = build_network(lines)
    button_presses: int = 0
    signals: deque[Signal] = deque()
    rx_status = True

    while rx_status:
        # Press the button.
        broadcaster = network["broadcaster"]
        button_presses += 1

        for target in broadcaster.targets:
            signals.append(Signal(None, target, False))

        while signals:
            signal = signals.popleft()
            if signal.target == "rx" and signal.status is False:
                rx_status = False
                continue
            if signal.target not in network:
                continue

            signal_target = network[signal.target]
            if signal_target.type == ModuleType.FLIP_FLOP:
                # Flip-flops ignore True signals. If the signal is False, it negates its value
                # and sends that value to its targets.
                if signal.status is False:
                    signal_target.status = not signal_target.status
                    for target in signal_target.targets:
                        signals.append(Signal(signal.target, target, signal_target.status))
            elif signal_target.type == ModuleType.CONJUNCTION:
                signal_target.inputs[signal.source] = signal.status
                signal_target.status = not all(status for status in signal_target.inputs.values())
                for target in signal_target.targets:
                    signals.append(Signal(signal.target, target, signal_target.status))
            else:
                raise ValueError(f"Unexpected module type: {signal_target.type}")

        binary_string = ""
        for target in ("ff", "ee", "dd", "cc", "bb", "aa"):
            module = network[target]
            binary_string += str(int(module.status))
        print(f"{binary_string} {int(binary_string, 2)}")

    print(f"rx status low after {button_presses} button presses.")


def make_dot(lines: list[str]) -> str:
    graph = "digraph modules {\n"
    for line in lines:
        name, target_list = line.split(" -> ")
        if name[0] == "%":
            box_shape = "diamond"
            name = name[1:]
        elif name[0] == "&":
            box_shape = "rectangle"
            name = name[1:]
        else:
            box_shape = "circle"

        graph += f"\t{name} [shape={box_shape}];\n"

    for line in lines:
        name, target_list = line.split(" -> ")
        if name[0] in ("&", "%"):
            name = name[1:]

        for target in target_list.split(", "):
            if target == "rx":
                graph += "\trx [shape=star, style=filled, fillcolor=red];\n"
            graph += f"\t{name} -> {target}; \n"
    graph += "}"
    return graph


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
    with open("day20test.txt") as infile:
        lines = infile.read().splitlines()

    part1 = tally_pulses(lines)
    print(f"Part 1: {part1}")
    # assert part1 == 680278040

    with open("day20test.dot", "w") as dot:
        dot.write(make_dot(lines))
    show_values(lines)
    # part2 = presses_until_rx_low(lines)
    # print(f"Part 2: {part2}")

    """
    I did the solution with pen and paper and a test file. The broadcaster sends its pulse
    to the low bit of four 12-digit binary numbers. Each number has a conjunction module. 
    To find the value of the number that contributes to the answer, calculate the binary 
    value of the bits that send to the conjunction module. The LCM of those four values
    is the answer.
    """
