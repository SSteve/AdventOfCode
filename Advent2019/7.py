from intcode import IntCode
from itertools import permutations

def calculate_thrust(int_code_program, phase_sequence):
    input_value = 0
    for phase in phase_sequence:
        computer = IntCode(int_code_program, [phase, input_value])
        computer.run()
        input_value = computer.output_values[0]
    return input_value

def calculate_thrust2(int_code_program, phase_sequence):
    input_value = 0
    computers = []
    for phase in phase_sequence:
        computers.append(IntCode(int_code_program, [phase], interactive=False))
    while not computers[4].halted:
        for i in range(5):
            computers[i].accept_input(input_value)
            computers[i].run()
            input_value = computers[i].output_values[-1]
    return input_value    

if __name__ == "__main__":
    # Tests
    assert calculate_thrust("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", [4, 3, 2, 1, 0]) == 43210
    assert calculate_thrust("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0", [0, 1, 2, 3, 4]) == 54321
    assert calculate_thrust("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0", [1, 0, 4, 3, 2]) == 65210
    assert calculate_thrust2("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5", [9, 8, 7, 6, 5]) == 139629729
    assert calculate_thrust2("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10", [9, 7, 8, 5, 6]) == 18216

    with open("7.txt") as infile:
        int_code_program = infile.readline().strip()
    maximum_thrust = 0
    for phase_sequence in permutations(range(5)):
        thrust = calculate_thrust(int_code_program, phase_sequence)
        maximum_thrust = max(maximum_thrust, thrust)
    print(f"Part one: maximum thrust = {maximum_thrust}")

    # Make sure nothing broke after solving part one
    assert maximum_thrust == 34852, "Part one answer is no longer correct"

    maximum_thrust2 = 0
    for phase_sequence in permutations(range(5, 10)):
        thrust = calculate_thrust2(int_code_program, phase_sequence)
        maximum_thrust2 = max(maximum_thrust2, thrust)
    print(f"Part two: maximum thrust = {maximum_thrust2}")