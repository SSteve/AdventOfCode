def day6(fileName, shouldPrint=False):
    cycles = 0
    with open(fileName) as infile:
        banks = [int(bankString) for bankString in infile.readline().strip().split("\t")]

    if shouldPrint:
        print(banks)
    previousBanks = []

    while banks not in previousBanks:
        cycles += 1
        previousBanks.append(banks[:])  # put a copy in previousBanks
        largestInx = 0
        for i in range(1, len(banks)):
            if banks[i] > banks[largestInx]:
                largestInx = i
        redistInx = (largestInx + 1) % len(banks)
        blocks = banks[largestInx]
        banks[largestInx] = 0
        for _ in range(blocks):
            banks[redistInx] += 1
            redistInx = (redistInx + 1) % len(banks)
        if shouldPrint:
            print(banks)

    loopLength = len(previousBanks) - previousBanks.index(banks)
    return cycles, loopLength

if __name__ == "__main__":
    cycles, loopLength = day6("6test.txt", shouldPrint=False)
    print(f"{cycles} cycles. Loop length: {loopLength}")
