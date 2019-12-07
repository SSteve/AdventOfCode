from intcode import IntCode
from itertools import permutations

def calculate_thrust(int_code_program, phase_sequence):
    input_value = 0
    for phase in phase_sequence:
        computer = IntCode(int_code_program, [phase, input_value])
        computer.run()
        input_value = computer.output_values[0]
    return input_value

if __name__ == "__main__":
    # Tests
    assert calculate_thrust("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", [4, 3, 2, 1, 0]) == 43210
    assert calculate_thrust("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0", [0, 1, 2, 3, 4]) == 54321
    assert calculate_thrust("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0", [1, 0, 4, 3, 2]) == 65210

    with open("7.txt") as infile:
        int_code_program = infile.readline().strip()
    maximum_thrust = 0
    for phase_sequence in permutations(range(5)):
        thrust = calculate_thrust(int_code_program, phase_sequence)
        maximum_thrust = max(maximum_thrust, thrust)
    print(f"Part one: maximum thrust = {maximum_thrust}")
