def generator(seedA, factorA, seedB, factorB):
    previousValueA = seedA
    previousValueB = seedB
    while True:
        valA = previousValueA * factorA % 0x7FFF_FFFF
        valB = previousValueB * factorB % 0x7FFF_FFFF
        yield valA, valB
        previousValueA = valA
        previousValueB = valB


def generatorA(seedA, factorA):
    previousValueA = seedA
    while True:
        valA = previousValueA * factorA % 0x7FFF_FFFF
        if valA & 0x03 == 0:
            yield valA
        previousValueA = valA


def generatorB(seedB, factorB):
    previousValueB = seedB
    while True:
        valB = previousValueB * factorB % 0x7FFF_FFFF
        if valB & 0x07 == 0:
            yield valB
        previousValueB = valB


def day15(seedA, seedB):
    generators = generator(seedA, 16807, seedB, 48271)
    rounds = 0
    matches = 0
    while rounds < 40_000_000:
        valA, valB = next(generators)
        rounds += 1
        if (valA & 0xFFFF) == (valB & 0xFFFF):
            matches += 1
            print(f"matches: {matches}")


def day15b(seedA, seedB):
    genA = generatorA(seedA, 16807)
    genB = generatorB(seedB, 48271)
    rounds = 0
    matches = 0
    while rounds < 5_000_000:
        valA = next(genA)
        valB = next(genB)
        rounds += 1
        if (valA & 0xFFFF) == (valB & 0xFFFF):
            matches += 1
            print(f"matches: {matches:5}, rounds: {rounds:10,}")


if __name__ == "__main__":
    # day15(65, 8921)
    # day15(116, 299)
    # day15b(65, 8921)
    day15b(116, 299)
