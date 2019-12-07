from intcode import IntCode

if __name__ == "__main__":
    # Tests
    computer = IntCode("1,9,10,3,2,3,11,0,99,30,40,50")
    computer.run()
    assert computer.get_memory(0) == 3500, "Day 2 test 1 failed."
    computer = IntCode("1,0,0,0,99")
    computer.run()
    assert computer.get_memory(0) == 2, "Day 2 test 2 failed."
    computer = IntCode("2,3,0,3,99")
    computer.run()
    assert computer.get_memory(3) == 6, "Day 2 test 3 failed."
    computer = IntCode("2,4,4,5,99,0")
    computer.run()
    assert computer.get_memory(5) == 9801, "Day 2 test 4 failed."
    computer = IntCode("1,1,1,4,99,5,6,0,99")
    computer.run()
    assert computer.get_memory(0) == 30, "Day 2 test 5 failed."

    # Part 1
    with open("2.txt", "r") as infile:
        computer = IntCode(infile.readline())
        
    computer.set_memory(1, 12)
    computer.set_memory(2, 2)
    computer.run()
    
    print(f"Part one: register 0 == {computer.get_memory(0)}")

    # Part 2
    # I disassembled the program to find that this is the calculation:
    noun = 12
    verb = 2
    x = ((((((((noun * 4 + 9) * 2 + 6) * 4 + 2) * 3 + 1) * 3 + 15) * 6 + 12) * 3 + 2) * 3 + 3) * 16 + 6 + verb
    # Test to make sure my equation returns the same result as the program
    assert x == 3765464, "Disassembled calculation is incorrect"
    
    # I could have simplified the equation but that would have been a bunch of error-prone
    # manual math so I decided to skip it.
    
    # After that, I put the formula in a spreadsheet. Since verb is added in the final calculation,
    # I entered values for noun with verb set to 0 until I found the highest value for noun that
    # resulted in a number less than 19690720. It turned out to be 19690710 which means that 
    # verb is 10.

    with open("2.txt", "r") as infile:
        computer = IntCode(infile.readline())
        
    noun = 76
    verb = 10
    computer.set_memory(1, noun)
    computer.set_memory(2, verb)
    computer.run()
    
    print(f"Part two: register 0 == {computer.get_memory(0)}")
    print(f"100 * noun + verb = {100 * noun + verb}")