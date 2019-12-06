import re
from collections import defaultdict

instructionRegex = re.compile(r"(...) (.)\s?(.*)")


class Instruction:
    def __init__(self, opcode, register, sourceRegister, sourceValue):
        self.opcode = opcode
        self.register = register
        self.sourceRegister = sourceRegister
        self.sourceValue = sourceValue

    def __repr__(self):
        valueStr = ""
        if self.sourceRegister is not None:
            valueStr = self.sourceRegister
        elif self.sourceValue is not None:
            valueStr = f"{self.sourceValue}"
        return f"{self.opcode} {self.register} {valueStr}"


class Processor:
    def __init__(self, instructions):
        self.registers = defaultdict(int)
        self.instructions = instructions
        self.instructionPointer = 0
        self.lastFrequency = 0
        self.recoveredFrequency = 0

    def start(self):
        while self.instructionPointer >= 0 and self.instructionPointer < len(self.instructions):
            self.lastInstruction = self.instructions[self.instructionPointer]
            self.perform(self.instructions[self.instructionPointer])
            if self.testStopCondition():
                self.stopCommand()
                break
            self.instructionPointer += 1

    def perform(self, instruction):
        if instruction.sourceRegister is not None:
            value = self.registers[instruction.sourceRegister]
        else:
            value = instruction.sourceValue
        eval(f"self.{instruction.opcode}('{instruction.register}', {value})")

    def snd(self, register, value):
        self.lastFrequency = self.registers[register]

    def set(self, register, value):
        self.registers[register] = value

    def add(self, register, value):
        self.registers[register] += value

    def mul(self, register, value):
        self.registers[register] *= value

    def mod(self, register, value):
        self.registers[register] %= value

    def rcv(self, register, value):
        if self.registers[register]:
            self.recoveredFrequency = self.lastFrequency

    def jgz(self, register, value):
        if self.registers[register] > 0:
            # Subtrace 1 from value because the instruction pointer will be incremented after the instruction is executed
            self.instructionPointer += value - 1

    def rcvWithNonZero(self):
        return self.lastInstruction.opcode == "rcv" and self.registers[self.lastInstruction.register] != 0

    def printRecoveredFrequency(self):
        print(f"Last frequency: {self.recoveredFrequency}")


def day18(fileName):
    instructions = []
    with open(fileName) as infile:
        for line in infile:
            match = instructionRegex.match(line)
            if match:
                if len(match[3]) == 0:
                    # No second operand
                    sourceRegister = None
                    sourceValue = None
                else:
                    try:
                        # Second operand is numerical value
                        sourceRegister = None
                        sourceValue = int(match[3])
                    except:
                        # second operand is register
                        sourceRegister = match[3]
                        sourceValue = None
                instructions.append(Instruction(match[1], match[2], sourceRegister, sourceValue))
            else:
                raise ValueError(f"Couldn't match line {line}")
    processor = Processor(instructions)
    processor.testStopCondition = processor.rcvWithNonZero
    processor.stopCommand = processor.printRecoveredFrequency
    processor.start()


if __name__ == "__main__":
    day18("18.txt")
