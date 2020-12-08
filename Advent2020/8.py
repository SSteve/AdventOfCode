from collections import namedtuple
from typing import List


Instruction = namedtuple('Instruction', 'operation, argument')


class Processor:
    def __init__(self, input: List[str]):
        self.instructions: List[Instruction] = []
        for line in input:
            operation, argument = line.split(" ")
            self.instructions.append(Instruction(operation, int(argument)))

    def SwapOperation(self, instructionNumber):
        if instructionNumber in range(len(self.instructions)):
            if self.instructions[instructionNumber].operation == "jmp":
                self.instructions[instructionNumber] = Instruction("nop",
                    self.instructions[instructionNumber].argument)
            elif self.instructions[instructionNumber].operation == "nop":
                self.instructions[instructionNumber] = Instruction("jmp",
                    self.instructions[instructionNumber].argument)

    def Run(self):
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
            gotToEnd = instructionPointer == len(self.instructions)

        return (accumulator, gotToEnd)


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
    assert result[0] == 5, f"Part 1 test is {result}. Should be 5."
    testProcessor.SwapOperation(7)
    result2 = testProcessor.Run()
    assert result2[0] == 8, f"Part 2 test is {result}. Should be 8."

    with open("8.txt", "r") as infile:
        processor = Processor(infile.read().splitlines())
    part1 = processor.Run()
    print(f"Part 1: {part1[0]}")
    assert part1[0] == 2058, f"Part 1 is broken. Should be 2058 but is {part1[0]}."
    
    # Brute force the solution
    lastSwapped = -1
    while lastSwapped < len(processor.instructions):
        part2 = processor.Run()
        if part2[1]:
            break
        processor.SwapOperation(lastSwapped)
        lastSwapped += 1
        while lastSwapped < len(processor.instructions) and processor.instructions[lastSwapped].operation == 'acc':
            lastSwapped += 1
        processor.SwapOperation(lastSwapped)
    
    print(f"Part 2: {part2[0]}")
    
