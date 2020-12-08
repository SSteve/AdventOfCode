from dataclasses import dataclass
from typing import List


@dataclass
class Instruction:
    operation: str
    argument: int


class Processor:
    def __init__(self, input: List[str]):
        self.instructions: List[Instruction] = []
        for line in input:
            operation, argument = line.split(" ")
            self.instructions.append(Instruction(operation, int(argument)))

    def SwapOperation(self, instructionNumber):
        if instructionNumber in range(len(self.instructions)):
            if self.instructions[instructionNumber].operation == "jmp":
                self.instructions[instructionNumber].operation = "nop"
            elif self.instructions[instructionNumber].operation == "nop":
                self.instructions[instructionNumber].operation = "jmp"

    def Run(self) -> int:
        self.executedLines = set()
        instructionPointer = 0
        accumulator = 0
        while instructionPointer not in self.executedLines \
                and instructionPointer < len(self.instructions):
            self.executedLines.add(instructionPointer)
            instruction = self.instructions[instructionPointer]
            if instruction.operation == 'acc':
                accumulator += instruction.argument
                instructionPointer += 1
            elif instruction.operation == 'nop':
                instructionPointer += 1
            elif instruction.operation == 'jmp':
                instructionPointer += instruction.argument
            self.gotToEnd = instructionPointer == len(self.instructions)

        return accumulator

    def FixBadInstruction(self) -> bool:
        lastSwapped = -1
        while lastSwapped < len(self.instructions):
            self.Run()
            if self.gotToEnd:
                break
            self.SwapOperation(lastSwapped)
            lastSwapped += 1
            while lastSwapped < len(self.instructions) and self.instructions[lastSwapped].operation == 'acc':
                lastSwapped += 1
            self.SwapOperation(lastSwapped)
        return lastSwapped < len(self.instructions)


TEST = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

if __name__ == "__main__":
    testProcessor = Processor(TEST.splitlines())
    result = testProcessor.Run()
    assert result == 5, f"Part 1 test is {result}. Should be 5."
    testProcessor.FixBadInstruction()
    result2 = testProcessor.Run()
    assert result2 == 8, f"Part 2 test is {result}. Should be 8."

    with open("8.txt", "r") as infile:
        processor = Processor(infile.read().splitlines())
    part1 = processor.Run()
    print(f"Part 1: {part1}")
    assert part1 == 2058, f"Part 1 is broken. Should be 2058 but is {part1}."
    processor.FixBadInstruction()
    part2 = processor.Run()
    print(f"Part 2: {part2}")
