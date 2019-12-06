if __name__ == "__main__":
    with open("2.txt", "r") as infile:
        integers = infile.readline()
    registers = []
    for x in integers.split(","):
        registers.append(int(x))
    
    registers[1] = 12
    registers[2] = 2
    print(registers)
    index = 0
    while registers[index] != 99:
        opcode = registers[index]
        op1 = registers[registers[index + 1]]
        op2 = registers[registers[index + 2]]
        if opcode == 1:
            result = op1 + op2
        elif opcode == 2:
            result = op1 * op2
        else:
            raise ValueError(f"Unknown opcode: {opcode} at position {index}")
        registers[registers[index + 3]] = result
        index += 4

    print(f"Register 0 = {registers[0]}")