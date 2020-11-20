from typing import List

INPUT_SIGNAL1 = "12345678"
INPUT_SIGNAL2 = "80871224585914546619083218645595"
INPUT_SIGNAL3 = "19617804207202209144916044189917"
INPUT_SIGNAL4 = "69317163492948606335995924319873"


def create_input_signal(input_string: str) -> List[int]:
    return [int(c) for c in input_string]


def add_range(values: List[int], element_number: int) -> int:
    result = 0
    for i in range(element_number - 1, len(values), element_number * 4):
        result += sum(values[i:i + element_number])
    return result


def subtract_range(values: List[int], element_number: int) -> int:
    result = 0
    for i in range(element_number * 3 - 1, len(values), element_number * 4):
        result += sum(values[i:i + element_number])
    return result


def perform_phase(values: List[int]) -> List[int]:
    result: List[int] = []
    for i in range(len(values)):
        phase_result = add_range(values, i + 1) - subtract_range(values, i + 1)
        result.append(abs(phase_result) % 10)
    return result


if __name__ == '__main__':
    start_index = 0
    signal = create_input_signal(INPUT_SIGNAL1)
    signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal) == "48226158"
    signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal) == "34040438"
    signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal) == "03415518"
    signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal) == "01029498"

    offset = 0
    signal = create_input_signal(INPUT_SIGNAL2)
    for _ in range(100):
        signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal[0:8]) == "24176176"
    print(''.join(f"{c}" for c in signal[offset:offset + 8]))

    signal = create_input_signal(INPUT_SIGNAL3)
    for _ in range(100):
        signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal[0:8]) == "73745418"
    print(''.join(f"{c}" for c in signal[offset:offset + 8]))

    signal = create_input_signal(INPUT_SIGNAL4)
    for _ in range(100):
        signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal[0:8]) == "52432133"
    print(''.join(f"{c}" for c in signal[offset:offset + 8]))
    
    with open("16.txt") as infile:
        signal = create_input_signal(infile.readline().strip())
    for _ in range(100):
        signal = perform_phase(signal)
    print(''.join(f"{c}" for c in signal[0:8]))

    offset = int(INPUT_SIGNAL2[0:7])
    signal = create_input_signal(INPUT_SIGNAL2 * 10000)
    for _ in range(100):
        signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal[offset:offset + 8]) == "84462026"
    print(''.join(f"{c}" for c in signal[offset:offset + 8]))

    offset = int(INPUT_SIGNAL3[0:7])
    signal = create_input_signal(INPUT_SIGNAL3 * 10000)
    for _ in range(100):
        signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal[offset:offset + 8]) == "78725270"
    print(''.join(f"{c}" for c in signal[offset:offset + 8]))

    offset = int(INPUT_SIGNAL4[0:7])
    signal = create_input_signal(INPUT_SIGNAL4 * 10000)
    for _ in range(100):
        signal = perform_phase(signal)
    assert ''.join(f"{c}" for c in signal[offset:offset + 8]) == "53553731"
    print(''.join(f"{c}" for c in signal[offset:offset + 8]))
