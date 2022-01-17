from __future__ import annotations
from collections import defaultdict, deque
from typing import Iterable, Tuple
import re

giveValue = re.compile(r"value (\d+) goes to bot (\d+)")
botAction = re.compile(
    r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)")

TEST = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""


class Bot:
    def __init__(self) -> None:
        self.microchips: set[int] = set()

    def Accept(self, chipValue: int) -> bool:
        # Accept a microchip with the given value. Return true if the bot contains
        # two microchips.
        self.microchips.add(chipValue)
        return len(self.microchips) == 2

    def FollowInstruction(self, instruction: str,
                          bots: dict[int, Bot], outputs: dict[int, set[int]]) -> Iterable[int]:
        readyBots: list[int] = []
        match = re.match(botAction, instruction)
        if match is None:
            raise ValueError(f"Instruction '{instruction}' not recognized.")
        lowDestination = match[2]
        lowDestinationLocation = int(match[3])
        highDestination = match[4]
        highDestinationLocation = int(match[5])
        low = min(self.microchips)
        high = max(self.microchips)
        if lowDestination == 'output':
            outputs[lowDestinationLocation].add(low)
        else:
            botIsReady = bots[lowDestinationLocation].Accept(low)
            if botIsReady:
                readyBots.append(lowDestinationLocation)
        if highDestination == 'output':
            outputs[highDestinationLocation].add(high)
        else:
            botIsReady = bots[highDestinationLocation].Accept(high)
            if botIsReady:
                readyBots.append(highDestinationLocation)
        return readyBots

    def HasMicrochips(self, values: set[int]) -> bool:
        return self.microchips == values


def ProcessInstructions(instructions: list[str], target: set[int]) -> None:
    readyBots: deque[int] = deque()
    bots: dict[int, Bot] = defaultdict(Bot)
    outputs: dict[int, set[int]] = defaultdict(set)
    waitingInstructions: deque[Tuple[int, str]] = deque()

    for instruction in instructions:
        if match := re.match(giveValue, instruction):
            value = int(match[1])
            botNumber = int(match[2])
            botIsReady = bots[botNumber].Accept(value)
            if botIsReady:
                readyBots.append(botNumber)
        elif match := re.match(botAction, instruction):
            botNumber = int(match[1])
            waitingInstructions.append((botNumber, instruction))
        else:
            raise ValueError(f"Instruction '{instruction}' not recognized.")
        botIndex = 0
        while botIndex < len(readyBots):
            readyBotNumber = readyBots[botIndex]
            botHadInstruction = False
            if bots[readyBotNumber].HasMicrochips(target):
                print(f"Part 1: {readyBotNumber}")
            instructionIndex = 0
            while instructionIndex < len(waitingInstructions):
                instruction = waitingInstructions[instructionIndex]
                if instruction[0] == readyBotNumber:
                    botHadInstruction = True
                    newReadyBots = bots[readyBotNumber].FollowInstruction(
                        instruction[1], bots, outputs)
                    readyBots.extend(newReadyBots)
                    del waitingInstructions[instructionIndex]
                else:
                    instructionIndex += 1
            if botHadInstruction:
                del readyBots[botIndex]
            else:
                botIndex += 1

    print(f"Part 2: {outputs[0].pop() * outputs[1].pop() * outputs[2].pop()}")


if __name__ == '__main__':
    # ProcessInstructions(TEST.splitlines(), set((5, 2)))

    with open('10.txt', 'r') as infile:
        instructions = infile.read().splitlines()
    ProcessInstructions(instructions, set((17, 61)))
