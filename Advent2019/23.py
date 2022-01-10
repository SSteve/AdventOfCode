from collections import defaultdict
from typing import Tuple

from intcode import IntCode

if __name__ == "__main__":
    with open("23.txt", "r") as infile:
        program = infile.read().strip()

    computers: list[IntCode] = []
    for i in range(50):
        computer = IntCode(program, [i], False)
        computers.append(computer)
        computer.run()

    instructions: dict[int, list[Tuple[int, int]]] = defaultdict(list)
    part1 = None
    part2 = None
    specialX = -1
    specialY = -1
    previousSpecialY = None
    while part1 is None or part2 is None:
        networkIsIdle = True
        for i, computer in enumerate(computers):
            while len(computer.output_values) >= 3:
                addr, x, y = computer.output_values[:3]
                if addr == 255:
                    if part1 is None:
                        part1 = y
                    specialX = x
                    specialY = y
                computer.output_values = computer.output_values[3:]
                instructions[addr].append((x, y))
            if computer.waiting_for_input:
                if i in instructions:
                    networkIsIdle = False
                    valuePairs = instructions.pop(i)
                    for valuePair in valuePairs:
                        computer.accept_input(valuePair[0])
                        computer.accept_input(valuePair[1])
                else:
                    computer.accept_input(-1)
                computer.run()
        if networkIsIdle and specialY >= 0:
            computers[0].accept_input(specialX)
            computers[0].accept_input(specialY)
            if specialY == previousSpecialY:
                part2 = specialY
            previousSpecialY = specialY
            computers[0].run()
    # 24954
    print(f"Part 1: {part1}")
    # 17091
    print(f"Part 2: {part2}")
