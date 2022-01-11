from typing import Callable


class Computer:
    def __init__(self, instructions: list[str]) -> None:
        self.instructions = instructions
        self.program_counter = 0
        self.registers: dict[str, int] = {'a': 0, 'b': 0}

    def hlf(self, register: str):
        self.registers[register] //= 2

    def tpl(self, register: str):
        self.registers[register] *= 3

    def inc(self, register: str):
        self.registers[register] += 1

    def jmp(self, offset: int):
        # Subtract one from offset because the program counter is always
        # incremented by 1 after an instruction.
        self.program_counter += offset - 1

    def jie(self, register: str, offset: int):
        if (self.registers[register] & 1) == 0:
            self.program_counter += offset - 1

    def jio(self, register: str, offset: int):
        if self.registers[register] == 1:
            self.program_counter += offset - 1

    def run(self):
        while 0 <= self.program_counter < len(self.instructions):
            arguments = self.instructions[self.program_counter].split()
            if arguments[0] == 'hlf':
                self.hlf(arguments[1])
            elif arguments[0] == 'tpl':
                self.tpl(arguments[1])
            elif arguments[0] == 'inc':
                self.inc(arguments[1])
            elif arguments[0] == 'jmp':
                self.jmp(int(arguments[1]))
            elif arguments[0] == 'jie':
                # Only use first character of arguments[1] because there's a comma
                # after the register name.
                self.jie(arguments[1][0], int(arguments[2]))
            elif arguments[0] == 'jio':
                # Only use first character of arguments[1] because there's a comma
                # after the register name.
                self.jio(arguments[1][0], int(arguments[2]))
            else:
                raise ValueError(f"Unknown instruction {arguments[0]}")
            self.program_counter += 1


if __name__ == '__main__':
    with open('23.txt', 'r') as infile:
        instructions = infile.read().splitlines()
    computer = Computer(instructions)
    computer.run()
    part1 = computer.registers['b']
    print(f"Part 1: {part1}")

    computer = Computer(instructions)
    computer.registers['a'] = 1
    computer.run()
    part2 = computer.registers['b']
    print(f"Part 2: {part2}")
