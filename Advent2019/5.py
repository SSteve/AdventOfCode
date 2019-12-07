from intcode import IntCode

if __name__ == "__main__":
    # Tests
    computer = IntCode("1002,4,3,4,33")
    computer.run()
    assert computer.get_memory(4) == 99, "Day 5 assertion (immediate mode) failed."

    # Part 1
    with open("5.txt", "r") as infile:
        computer = IntCode(infile.readline(), [1])
    print("Using input value 1 to test the air conditioner.")
    computer.run()
    print(computer.output_values)

    # Part 2
    with open("5.txt", "r") as infile:
        computer = IntCode(infile.readline(), [5])
    print("Using input value 5 to test the thermal radiator controller.")
    computer.run()
    print(computer.output_values)