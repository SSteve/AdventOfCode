from typing import Iterable

BASE_PATTERN = [0, 1, 0, -1]


def pattern_generator(element_number: int) -> Iterable[int]:
    # Return the first value element_number times
    for _ in range(element_number):
        yield BASE_PATTERN[0]
    pattern_index = 1
    while True:
        # Return the rest of the values element_number + 1 times
        for _ in range(element_number + 1):
            yield BASE_PATTERN[pattern_index]
        pattern_index = (pattern_index + 1) % 4


def create_input_signal(input_string: str) -> list[int]:
    return [int(c) for c in input_string]


def perform_phase(input_signal: list[int]) -> list[int]:
    length = len(input_signal)
    old = input_signal[:]
    for i in range(length):
        # Skip the numbers corresponding to 0 in the pattern.
        j = i
        step = i + 1
        total = 0
        while j < length:
            # Sum all the digits where there's a 1 in the pattern.
            total += sum(old[j: j + step])
            # Skip all the digits where there's a 0 in the pattern.
            j += 2 * step
            # Sum all the digits where there's a -1 in the pattern and subtract from total.
            total -= sum(old[j:j + step])
            # Skip all the digits where there's a 0 in the pattern.
            j += 2 * step
        input_signal[i] = abs(total) % 10
    return input_signal


def part2_100_phases(input_signal: list[int]) -> str:
    # Copied from https://github.com/mebeim/aoc
    to_skip = int(''.join(map(str, input_signal[:7])))
    assert to_skip > len(input_signal)//2

    digits = (input_signal * 10000)[to_skip:]
    length = len(digits)
    for _ in range(100):
        cumulative_sum = 0
        for i in range(length - 1, -1, -1):
            cumulative_sum += digits[i]
            digits[i] = cumulative_sum % 10
    return ''.join(map(str, digits[:8]))


INPUT_SIGNAL1 = "12345678"
INPUT_SIGNAL2 = "80871224585914546619083218645595"
INPUT_SIGNAL3 = "19617804207202209144916044189917"
INPUT_SIGNAL4 = "69317163492948606335995924319873"

if __name__ == '__main__':
    signal = create_input_signal(INPUT_SIGNAL1)
    signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal) == "48226158"
    signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal) == "34040438"
    signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal) == "03415518"
    signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal) == "01029498"

    signal = create_input_signal(INPUT_SIGNAL2)
    for _ in range(100):
        signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal[0:8]) == "24176176"

    signal = create_input_signal(INPUT_SIGNAL3)
    for _ in range(100):
        signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal[0:8]) == "73745418"

    signal = create_input_signal(INPUT_SIGNAL4)
    for _ in range(100):
        signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal[0:8]) == "52432133"

    with open("16.txt") as infile:
        signal = create_input_signal(infile.readline().strip())
    for _ in range(100):
        signal = perform_phase(signal)
    print("Part 1:", ''.join(f"{c}" for c in signal[0:8]))

    with open("16.txt") as infile:
        signal = create_input_signal(infile.readline().strip())
    part2 = part2_100_phases(signal)
    print(f"Part 2: {part2}")
