from typing import List

BASE_PATTERN = [0, 1, 0, -1]

def pattern_generator(element_number: int) -> int:
    # Return the first value element_number times
    for _ in range(element_number):
        yield BASE_PATTERN[0]
    pattern_index = 1
    while True:
        # Return the rest of the values element_number + 1 times
        for _ in range(element_number + 1):
            yield BASE_PATTERN[pattern_index]
        pattern_index = (pattern_index + 1) % 4

def create_input_signal(input_string: str) -> List[int]:
    return [int(c) for c in input_string]

def perform_phase(input_signal: List[int]) -> List[int]:
    result: List[int] = []
    element_number = 0
    for _ in range(len(input_signal)):
        index = 0
        accumulator = 0
        pg = pattern_generator(element_number)
        for fft_value in pg:
            accumulator += fft_value * input_signal[index]
            index += 1
            if index >= len(input_signal):
                break
        result.append(abs(accumulator) % 10)
        element_number += 1
    return result

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

    offset = int(INPUT_SIGNAL1[0:7])
    signal = create_input_signal(INPUT_SIGNAL1 * 10000)
    for _ in range(100):
        signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal[offset:offset + 8]) == "84462026"

    with open("16.txt") as infile:
        signal = create_input_signal(infile.readline().strip())
    for _ in range(100):
        signal = perform_phase(signal)
    print(''.join(f"{c}" for c in signal[0:8]))

    with open("16.txt") as infile:
        input_signal = infile.readline().strip() * 10000
    offset = int(input_signal[0:7])
    signal = create_input_signal(input_signal)
    for _ in range(100):
        signal = perform_phase(signal)
    print(''.join(f"{c}" for c in signal[offset:offset + 8]))
