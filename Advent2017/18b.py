import re
from collections import defaultdict, deque
import threading

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
    def __init__(self, instructions, programID):
        self.instructions = instructions
        self.instructionPointer = 0
        self.programID = programID
        self.registers = defaultdict(int)
        self.registers['p'] = programID
        self.queue = deque()
        self.sendCount = 0
        self.stopCommand = self.printSentCount
        self.terminate = False

    def start(self, otherQueue, myEvent, otherEvent):
        self.otherQueue = otherQueue  # The other processor's queue
        self.myEvent = myEvent  # The Event this processor will wait on
        self.otherEvent = otherEvent  # The Event the other processor will wait on
        while self.instructionPointer >= 0 and self.instructionPointer < len(
                self.instructions) and not self.terminate:
            self.lastInstruction = self.instructions[self.instructionPointer]
            self.perform(self.instructions[self.instructionPointer])
            self.instructionPointer += 1
        self.myEvent.clear(
        )  #Indicates to the other process that this process isn't running
        self.stopCommand()

    def getValue(self, field):
        try:
            value = int(field)
        except ValueError:
            value = self.registers[field]
        return value

    def perform(self, instruction):
        if instruction.sourceRegister is not None:
            value = self.registers[instruction.sourceRegister]
        else:
            value = instruction.sourceValue
        eval(f"self.{instruction.opcode}('{instruction.register}', {value})")

    def snd(self, op1, _):
        value = self.getValue(op1)
        self.sendCount += 1
        self.otherQueue.append(value)
        self.otherEvent.set()

    def set(self, register, value):
        self.registers[register] = value

    def add(self, register, value):
        self.registers[register] += value

    def mul(self, register, value):
        self.registers[register] *= value

    def mod(self, register, value):
        self.registers[register] %= value

    def rcv(self, register, value):
        if not self.queue and not self.otherEvent.is_set():
            print(f"Processor {self.programID} detected deadlock")
            self.terminate = True
            self.otherEvent.set()
        else:
            if not self.queue:
                self.myEvent.clear()
                print(f"Processor {self.programID} waiting")
                self.myEvent.wait()
                print(f"Processor {self.programID} resuming")
            if self.queue:
                receivedValue = self.queue.popleft()
                self.registers[register] = receivedValue
            else:
                # The other thread woke us up with no queue
                self.terminate = True

    def jgz(self, op1, value):
        if self.getValue(op1) > 0:
            # Subtract 1 from value because the instruction pointer will be incremented after the instruction is executed
            self.instructionPointer += value - 1

    def printSentCount(self):
        print(f"programID {self.programID} sent {self.sendCount} messages")


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
                    except ValueError:
                        # second operand is register
                        sourceRegister = match[3]
                        sourceValue = None
                instructions.append(
                    Instruction(match[1], match[2], sourceRegister,
                                sourceValue))
            else:
                raise ValueError(f"Couldn't match line {line}")
    processor0 = Processor(instructions, 0)
    processor1 = Processor(instructions, 1)
    p0Event = threading.Event()
    p1Event = threading.Event()
    p0Event.set()
    p1Event.set()
    thread1 = threading.Thread(
        target=processor0.start,
        args=(processor1.queue, p0Event, p1Event),
        name="Processor 0")
    thread2 = threading.Thread(
        target=processor1.start,
        args=(processor0.queue, p1Event, p0Event),
        name="Processor 1")
    thread2.start()
    thread1.start()
    thread1.join()
    thread2.join()


if __name__ == "__main__":
    day18("18.txt")

