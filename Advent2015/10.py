def day10(input, count):
    previousStep = input
    for _ in range(count):
        newStep = ""
        i = 0
        while i < len(previousStep):
            digitCount = 0
            digit = previousStep[i]
            while i < len(previousStep) and previousStep[i] == digit:
                i += 1
                digitCount += 1
            newStep += f"{digitCount}{digit}"
        previousStep = newStep
    return newStep


sequence = day10("1", 5)
print(len(sequence))
sequence = day10("1321131112", 40)
print(len(sequence))
sequence = day10(sequence, 10)
print(len(sequence))
