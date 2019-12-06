import re
from enum import Enum
# import pdb

beforePattern = re.compile(r"Before:\s+\[(\d+),\s+(\d+),\s+(\d+),\s+(\d+)\]")
afterPattern = re.compile(r"After:\s+\[(\d+),\s+(\d+),\s+(\d+),\s+(\d+)\]")
instructionPattern = re.compile(r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)")


class ReadState(Enum):
    IDLE = 1
    BEFORE = 2
    SAMPLE_INSTRUCTION = 3
    AFTER = 4
    LIVE_INSTRUCTION = 5


class Instruction():
    def __init__(self, input):
        self.opcode = input[0]
        self.a = input[1]
        self.b = input[2]
        self.c = input[3]

    def __str__(self):
        return f"Opcode: {self.opcode}, a: {self.a} b:{self.b} c:{self.c}"


class Processor:
    def __init__(self, registers=[0, 0, 0, 0]):
        self.registers = registers
        self.unknownOpcodes = [self.addr, self.addi, self.mulr, self.muli, self.banr, self.bani, self.borr, self.bori,
                               self.setr, self.seti, self.gtir, self.gtri, self.gtrr, self.eqir, self.eqri, self.eqrr]
        self.opcodeMap = {}

    def reset(self):
        self.registers = [0, 0, 0, 0]

    def executeInstruction(self, instruction: Instruction):
        opcode = self.opcodeMap[instruction.opcode]
        opcode(instruction.a, instruction.b, instruction.c)

    def registersMatch(self, testRegisters):
        return self.registers[0] == testRegisters[0] and \
            self.registers[1] == testRegisters[1] and \
            self.registers[2] == testRegisters[2] and \
            self.registers[3] == testRegisters[3]

    def testInstruction(self, instruction, beforeRegisters, afterRegisters):
        matchingInstructions = []
        for opcode in self.unknownOpcodes:
            self.registers = beforeRegisters[:]
            opcode(instruction.a, instruction.b, instruction.c)
            if self.registersMatch(afterRegisters):
                matchingInstructions.append(opcode)
        return matchingInstructions

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        self.registers[c] = a

    def gtir(self, a, b, c):
        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def eqir(self, a, b, c):
        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0


def processInput(instruction, before, after):
    processor = Processor(before)
    matching = processor.testInstruction(instruction, after)
    return len(matching)


def a16(fileName):
    # pdb.set_trace()
    threeOrMoreCount = 0
    state = ReadState.IDLE
    with open(fileName, "r") as infile:
        for line in infile:
            match = beforePattern.match(line)
            if match:
                beforeRegisters = [int(match[i + 1]) for i in range(4)]
                state = ReadState.BEFORE
                continue
            match = instructionPattern.match(line)
            if match:
                if state == ReadState.IDLE:
                    break
                instruction = Instruction(
                    [int(match[i + 1]) for i in range(4)])
                state = ReadState.INSTRUCTION
                continue
            match = afterPattern.match(line)
            if match:
                afterRegisters = [int(match[i + 1]) for i in range(4)]
                state = ReadState.AFTER
                if processInput(instruction, beforeRegisters, afterRegisters) >= 3:
                    threeOrMoreCount += 1
                state = ReadState.IDLE
        print(f"{threeOrMoreCount} samples match three or more opcodes")


def b16(fileName):
    state = ReadState.IDLE
    processor = Processor()
    with open(fileName, "r") as infile:
        for line in infile:
            match = beforePattern.match(line)
            if match:
                beforeRegisters = [int(match[i + 1]) for i in range(4)]
                state = ReadState.BEFORE
                continue
            match = instructionPattern.match(line)
            if match:
                instruction = Instruction(
                    [int(match[i + 1]) for i in range(4)])
                if state == ReadState.BEFORE:
                    state = ReadState.SAMPLE_INSTRUCTION
                elif state == ReadState.IDLE:
                    processor.reset()
                    processor.executeInstruction(instruction)
                    state = ReadState.LIVE_INSTRUCTION
                    continue
                elif state == ReadState.LIVE_INSTRUCTION:
                    processor.executeInstruction(instruction)
                    continue
            match = afterPattern.match(line)
            if match:
                afterRegisters = [int(match[i + 1]) for i in range(4)]
                matchingInstructions = processor.testInstruction(instruction, beforeRegisters, afterRegisters)
                if len(matchingInstructions) == 1:
                    processor.opcodeMap[instruction.opcode] = matchingInstructions[0]
                    processor.unknownOpcodes.remove(matchingInstructions[0])
                state = ReadState.IDLE
        print(f"Register 0: {processor.registers[0]}")
        print(processor.opcodeMap)


if __name__ == "__main__":
    b16("16.txt")
