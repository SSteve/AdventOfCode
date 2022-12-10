from dataclasses import dataclass

TEST = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


@dataclass(frozen=True)
class Instruction:
    instruction: str
    value: int


def create_instructions(lines: list[str]) -> list[Instruction]:
    instructions: list[Instruction] = []

    for line in lines:
        if line == "noop":
            instructions.append(Instruction(line, 0))
        else:
            (instruction, value) = line.split(" ", 1)
            instructions.append(Instruction(instruction, int(value)))

    return instructions


def sum_signal_strengths(instructions: list[Instruction]) -> int:
    cycles = [20, 60, 100, 140, 180, 220]
    cycles_index = 0
    current_cycle = 0
    sum = 0
    x = 1
    x_for_calculation = x
    for instruction in instructions:
        mid_cycle = False
        if instruction.instruction == "noop":
            current_cycle += 1
        else:
            current_cycle += 2
            if current_cycle >= cycles[cycles_index]:
                x_for_calculation = x
                mid_cycle = True
            x += instruction.value

        if current_cycle >= cycles[cycles_index]:
            signal_strength = (x_for_calculation if mid_cycle else x) * \
                cycles[cycles_index]
            sum += signal_strength
            cycles_index += 1
            if cycles_index >= len(cycles):
                break

    return sum


def sprite_is_visible(cycle: int, x: int) -> bool:
    horizontal_position = cycle % 40
    is_visible = horizontal_position-1 <= x <= horizontal_position+1
    return is_visible


def draw_screen(instructions) -> list[str]:
    screen = ["", "", "", "", "", ""]
    screen_index = 0
    x = 1
    current_cycle = 0

    for instruction in instructions:
        screen[screen_index] += "#" if sprite_is_visible(
            current_cycle, x) else " "
        if instruction.instruction == "noop":
            current_cycle += 1
        else:
            current_cycle += 1
            if current_cycle % 40 == 0:
                screen_index += 1
            screen[screen_index] += "#" if sprite_is_visible(
                current_cycle, x) else " "
            current_cycle += 1
            x += instruction.value
        if current_cycle % 40 == 0:
            screen_index += 1
        if current_cycle >= 240:
            break

    return screen


if __name__ == "__main__":
    instructions = create_instructions(TEST.splitlines())
    part1test = sum_signal_strengths(instructions)
    print(f"Part 1 test: {part1test}")
    assert (part1test == 13140)
    part2test = draw_screen(instructions)
    for line in part2test:
        print(line)

    with open("day10.txt") as infile:
        instructions = create_instructions(infile.read().splitlines())

    part1 = sum_signal_strengths(instructions)
    print(f"Part 1: {part1}")
    part2 = draw_screen(instructions)
    for line in part2:
        print(line)
