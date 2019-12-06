import re


class Instruction():
    def __init__(self, *args):
        self.opcode = args[0]
        self.a = args[1][0]
        self.b = args[1][1]
        self.c = args[1][2]

    def __str__(self):
        return f"{self.opcode} {self.a} {self.b} {self.c}"


class Processor:
    def __init__(self, registers=[0, 0, 0, 0, 0, 0]):
        self.registers = registers
        self.opcodeMap = {"addi": self.addi, "bani": self.bani, "gtir": self.gtir, "borr": self.borr,
                          "eqrr": self.eqrr, "bori": self.bori, "gtrr": self.gtrr, "setr": self.setr,
                          "muli": self.muli, "seti": self.seti, "banr": self.banr, "gtri": self.gtri,
                          "eqir": self.eqir, "eqri": self.eqri, "addr": self.addr, "mulr": self.mulr}
        self.instructionRegister = -1
        self.instructionPointer = 0
        self.shouldPrint = False
        self.program = []

    def reset(self):
        self.instructionPointer = 0
        self.registers = [1, 0, 0, 0, 0, 0]

    def setPrinting(self, onOff):
        self.shouldPrint = onOff

    def setInstructionRegister(self, register):
        self.instructionRegister = register

    def readInstruction(self, instruction: Instruction):
        self.program.append(instruction)

    def start(self):
        self.reset()
        while self.instructionPointer >= 0 and self.instructionPointer < len(self.program):
            instruction = self.program[self.instructionPointer]
            self.executeInstruction(instruction)
            self.instructionPointer += 1

    def executeInstruction(self, instruction):
        if self.instructionRegister >= 0:
            self.registers[self.instructionRegister] = self.instructionPointer
        opcode = self.opcodeMap[instruction.opcode]
        if self.shouldPrint:
            traceString = f"ip={self.instructionPointer} {self.registers} {instruction!s} "
        opcode(instruction.a, instruction.b, instruction.c)
        if self.instructionRegister >= 0:
            self.instructionPointer = self.registers[self.instructionRegister]
        if self.shouldPrint:
            print(f"{traceString} {self.registers}")

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


instructionPattern = re.compile(r"(\w+)\s+(\d+)\s+(\d+)\s+(\d+)")
directivePattern = re.compile(r"#ip (\d)")


def a19(fileName):
    processor = Processor()
    with open(fileName, "r") as infile:
        for line in infile:
            match = instructionPattern.match(line)
            if match:
                instruction = Instruction(match[1], [int(match[i + 2]) for i in range(3)])
                processor.readInstruction(instruction)
                continue
            match = directivePattern.match(line)
            if match:
                processor.setInstructionRegister(int(match[1]))
    processor.setPrinting(True)
    processor.start()
    print(processor.registers)


if __name__ == "__main__":
    a19("19.txt")
