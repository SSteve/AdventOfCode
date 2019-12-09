from intcode import IntCode

if __name__ == "__main__":
    # Tests
    # Relative mode tests are in intcode.py

    with open("9.txt") as infile:
        int_code_program = infile.readline().strip()
    computer = IntCode(int_code_program, [1], interactive=False)
    computer.run()
    if len(computer.output_values) == 1:
        print(f"Part one: BOOST keycode = {computer.output_values}")
    else:
        print(f"Errors found in part one: {computer.output_values}")

    computer = IntCode(int_code_program, [2], interactive=False)
    computer.run()
    print(f"Part two: coordinates of distress signal: {computer.output_values}")