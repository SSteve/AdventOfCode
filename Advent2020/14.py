import re
from collections import defaultdict
from itertools import combinations
from typing import List

TEST = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

TEST2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

maskRegex = re.compile(r"mask = (.*)")
memRegex = re.compile(r"mem\[(\d+)\] = (\d+)")


def Part1(program: List[str]) -> int:
    orMask = 0
    andMask = 2**36 - 1
    memory = defaultdict(int)
    for instruction in program:
        match = maskRegex.match(instruction)
        if match:
            orString = ''
            andString = ''
            for char in match[1]:
                if char == 'X':
                    orString += '0'
                    andString += '1'
                else:
                    orString += char
                    andString += char
            orMask = int(orString, 2)
            andMask = int(andString, 2)
        else:
            match = memRegex.match(instruction)
            value = (int(match[2]) | orMask) & andMask
            memory[int(match[1])] = value
    return sum(memory[key] for key in memory)


def Part2(program: List[str]) -> int:
    memory = defaultdict(int)
    orMask = 0
    memoryBits = []
    for instruction in program:
        match = maskRegex.match(instruction)
        if match:
            memoryBits = []
            orString = ''
            memoryString = ''
            for char in match[1]:
                if char == 'X':
                    # We'll start off by setting all the floating bits so put
                    # a '1' in the or mask.
                    orString += '1'
                    memoryString += '1'
                else:
                    orString += char
                    memoryString += '0'
            orMask = int(orString, 2)
            memoryValue = int(memoryString, 2)
            for bit in range(36):
                bitValue = 2 ** bit
                if memoryValue & bitValue:
                    memoryBits.append(bitValue)

        else:
            match = memRegex.match(instruction)
            # Set all the overwritten bits and floating bits in the address.
            address = int(match[1]) | orMask
            value = int(match[2])
            # Write to the address with all floating bits set.
            memory[address] = value
            # Go through all bit combinations and turn off the address bits
            # in that combination.
            for maskCount in range(len(memoryBits)):
                for bitValues in combinations(memoryBits, maskCount + 1):
                    bitMask = 2 ** 36 - 1 - sum(bitValues)
                    maskedAddress = address & bitMask
                    memory[maskedAddress] = value
    return sum(memory[key] for key in memory)


if __name__ == "__main__":
    testPart1 = Part1(TEST.splitlines())
    assert testPart1 == 165
    testPart2 = Part2(TEST2.splitlines())
    assert testPart2 == 208

    with open("14.txt", "r") as infile:
        instructions = infile.read().splitlines()
    part1 = Part1(instructions)
    print(f"Part 1: {part1}")
    part2 = Part2(instructions)
    print(f"Part 2: {part2}")
