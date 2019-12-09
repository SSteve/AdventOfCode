from intcode import IntCode

if __name__ == "__main__":
    # Tests
    # Relative mode tests are in intcode.py

    with open("9.txt") as infile:
        int_code_program = infile.readline().strip()
    computer = IntCode(int_code_program, [1], interactive=False)
    computer.run()
    print(computer.output_values)