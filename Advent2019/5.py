from intcode import IntCode

if __name__ == "__main__":
    # Tests
    computer = IntCode("1002,4,3,4,33")
    computer.run()
    assert computer.get_memory(4) == 99, "Day 5 assertion (immediate mode) failed."

    # Part 1
    with open("5.txt", "r") as infile:
        computer = IntCode(infile.readline())
    print("Enter 1 to test the air conditioner.")
    computer.run()

    # Part 2
    with open("5.txt", "r") as infile:
        computer = IntCode(infile.readline())
    print("Enter 5 to test the thermal radiator controller.")
    computer.run()
        