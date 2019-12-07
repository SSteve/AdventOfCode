from queue import SimpleQueue

class IntCode():
    def __init__(self, initial_memory, input_queue = []):
        self.memory = [int(x) for x in initial_memory.split(",")]
        self.instruction_pointer = 0
        self.halted = False
        self.input_queue = input_queue
        self.output_values = []
        
    def run(self):
        while not self.halted:
            opcode = self.memory[self.instruction_pointer] % 100
            if opcode == 1:
                self.add()
            elif opcode == 2:
                self.multiply()
            elif opcode == 3:
                self.input()
            elif opcode == 4:
                self.output()
            elif opcode == 5:
                self.jump_if_true()
            elif opcode == 6:
                self.jump_if_false()
            elif opcode == 7:
                self.less_than()
            elif opcode == 8:
                self.equals()
            elif opcode == 99:
                self.halt()
            else:
                raise ValueError(f"Unknown opcode: {opcode} at position {self.instruction_pointer}")
        
    def set_memory(self, address, value):
        self.memory[address] = value
        
    def get_memory(self, address):
        return self.memory[address]
        
    def core_dump(self):
        return self.memory
        
    def read_next(self, parameter_mode = 0):
        if parameter_mode == 1:
            # immediate mode
            result = self.memory[self.instruction_pointer]
        else:
            # position mode
            result = self.memory[self.memory[self.instruction_pointer]]
        self.instruction_pointer += 1
        return result
            
    def halt(self):
        self.instruction_pointer += 1
        self.halted = True
                
    def add(self):
        instruction = self.read_next(1)
        parameter_modes = instruction // 100
        addend1 = self.read_next(parameter_modes & 1 == 1)
        parameter_modes //= 10
        addend2 = self.read_next(parameter_modes & 1 == 1)
        destination = self.read_next(1)
        summand = addend1 + addend2
        self.memory[destination] = summand
        return summand
        
    def multiply(self):
        instruction = self.read_next(1)
        parameter_modes = instruction // 100
        factor1 = self.read_next(parameter_modes & 1 == 1)
        parameter_modes //= 10
        factor2 = self.read_next(parameter_modes & 1 == 1)
        destination = self.read_next(1)
        product = factor1 * factor2
        self.memory[destination] = product
        return product
        
    def input(self):
        # Bypass the instruction
        _ = self.read_next(1)
        address = self.read_next(1)
        if len(self.input_queue) == 0:
            value = int(input("Enter an integer: "))
        else:
            value = self.input_queue.pop(0)
        self.memory[address] = value
        
    def output(self):
        instruction = self.read_next(1)
        parameter_modes = instruction // 100
        value = self.read_next(parameter_modes & 1 == 1)
        self.output_values.append(value) 
        
    def jump_if_true(self):
        instruction = self.read_next(1)
        parameter_modes = instruction // 100
        value = self.read_next(parameter_modes & 1 == 1)
        parameter_modes //= 10
        address = self.read_next(parameter_modes & 1 == 1)
        if value != 0:
            self.instruction_pointer = address

    def jump_if_false(self):
        instruction = self.read_next(1)
        parameter_modes = instruction // 100
        value = self.read_next(parameter_modes & 1 == 1)
        parameter_modes //= 10
        address = self.read_next(parameter_modes & 1 == 1)
        if value == 0:
            self.instruction_pointer = address
            
    def less_than(self):
        instruction = self.read_next(1)
        parameter_modes = instruction // 100
        param1 = self.read_next(parameter_modes & 1 == 1)
        parameter_modes //= 10
        param2 = self.read_next(parameter_modes & 1 == 1)
        destination = self.read_next(1)
        if param1 < param2:
            self.memory[destination] = 1
        else:
            self.memory[destination] = 0
        
    def equals(self):
        instruction = self.read_next(1)
        parameter_modes = instruction // 100
        param1 = self.read_next(parameter_modes & 1 == 1)
        parameter_modes //= 10
        param2 = self.read_next(parameter_modes & 1 == 1)
        destination = self.read_next(1)
        if param1 == param2:
            self.memory[destination] = 1
        else:
            self.memory[destination] = 0
    
    def disassemble(self):
        instruction_strings = []
        starting_instruction_pointer = self.instruction_pointer
        self.instruction_pointer = 0
        opcode = 0
        while opcode != 99:
            opcode = self.memory[self.instruction_pointer] % 100
            if opcode == 1:
                instruction_strings.append(self.disassemble_add())
            elif opcode == 2:
                instruction_strings.append(self.disassemble_multiply())
            elif opcode == 99:
                instruction_strings.append(self.disassemble_halt())
            else:
                raise ValueError(f"Unknown opcode: {opcode} at position {self.instruction_pointer}")
        self.instruction_pointer = starting_instruction_pointer
        return "\n".join(instruction_strings)
        
    def disassemble_value(self, value, parameter_mode):
        if parameter_mode == 1:
            return f"#{value}"
        else:
            return f"{value}"
            
    def disassemble_add(self):
        instruction = self.read_next(1)
        addend1 = self.read_next(1)
        addend2 = self.read_next(1)
        summand = self.read_next(1)
        parameter_modes = instruction // 100
        return f"{self.instruction_pointer - 4}: {summand} = {self.disassemble_value(addend1, parameter_modes % 10)} + {self.disassemble_value(addend2, parameter_modes // 10 % 10)}"
        
    def disassemble_multiply(self):
        instruction = self.read_next(1)
        factor1 = self.read_next(1)
        factor2 = self.read_next(1)
        product = self.read_next(1)
        parameter_modes = instruction // 100
        return f"{self.instruction_pointer - 4}: {product} = {self.disassemble_value(factor1, parameter_modes % 10)} * {self.disassemble_value(factor2, parameter_modes // 10 % 10)}"
        
    def disassemble_halt(self):
        return f"{self.instruction_pointer}: halt"
       
if __name__ == "__main__":
    # Day 2, Part 1
    with open("2.txt", "r") as infile:
        computer = IntCode(infile.readline())
        
    computer.set_memory(1, 12)
    computer.set_memory(2, 2)
    # print(computer.disassemble())
    computer.run()
    
    assert computer.get_memory(0) == 3765464, "Day 2 assertion (addition and multiplication in position mode) failed."
    
    # Day 5, Part 1
    computer = IntCode("1002,4,3,4,33")
    computer.run()
    assert computer.get_memory(4) == 99, "Day 5 assertion (immediate mode) failed."

    # Day 5, Part 2
    # Equal (position mode) test
    # Output is 1 if input == 8, 0 otherwise
    computer = IntCode("3,9,8,9,10,9,4,9,99,-1,8", [9])
    computer.run()
    assert computer.output_values[0] == 0, "Equal (position mode) test 1 failed"
    computer = IntCode("3,9,8,9,10,9,4,9,99,-1,8", [8])
    computer.run()
    assert computer.output_values[0] == 1, "Equal (position mode) test 2 failed"

    # Less-than (position mode) test
    # Output is 1 if input < 8, 0 otherwise
    computer = IntCode("3,9,7,9,10,9,4,9,99,-1,8", [-5])
    computer.run()
    assert computer.output_values[0] == 1, "Less-than (position mode) test 1 failed"
    computer = IntCode("3,9,7,9,10,9,4,9,99,-1,8", [8475849])
    computer.run()
    assert computer.output_values[0] == 0, "Less-than (position mode) test 2 failed"
    computer = IntCode("3,9,7,9,10,9,4,9,99,-1,8", [8])
    computer.run()
    assert computer.output_values[0] == 0, "Less-than (position mode) test 3 failed"

    # Equal (immediate mode) test
    # Output is 1 if input == 8, 0 otherwise
    computer = IntCode("3,3,1108,-1,8,3,4,3,99", [7])
    computer.run()
    assert computer.output_values[0] == 0, "Equal (immediate mode) test 1 failed"
    computer = IntCode("3,3,1108,-1,8,3,4,3,99", [8])
    computer.run()
    assert computer.output_values[0] == 1, "Equal (immediate mode) test 2 failed"

    # Less-than (immediate mode) test
    # Output is 1 if input < 8, 0 otherwise
    computer = IntCode("3,3,1107,-1,8,3,4,3,99", [-86])
    computer.run()
    assert computer.output_values[0] == 1, "Less-than (immediate mode) test 1 failed"
    computer = IntCode("3,3,1107,-1,8,3,4,3,99", [8])
    computer.run()
    assert computer.output_values[0] == 0, "Less-than (immediate mode) test 2 failed"
    computer = IntCode("3,3,1107,-1,8,3,4,3,99", [9])
    computer.run()
    assert computer.output_values[0] == 0, "Less-than (immediate mode) test 3 failed"

    # Jump (position mode) test
    # Output is 0 if input == 0, 1 otherwise
    computer = IntCode("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [0])
    computer.run()
    assert computer.output_values[0] == 0, "Jump (position mode) test 1 failed"
    computer = IntCode("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [-1])
    computer.run()
    assert computer.output_values[0] == 1, "Jump (position mode) test 2 failed"
    computer = IntCode("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [1])
    computer.run()
    assert computer.output_values[0] == 1, "Jump (position mode) test 3 failed"

    # Jump (immediate mode) test
    # Output is 0 if input == 0, 1 otherwise
    computer = IntCode("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [0])
    computer.run()
    assert computer.output_values[0] == 0, "Jump (immediate mode) test 1 failed"
    computer = IntCode("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [-1])
    computer.run()
    assert computer.output_values[0] == 1, "Jump (immediate mode) test 2 failed"
    computer = IntCode("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [1])
    computer.run()
    assert computer.output_values[0] == 1, "Jump (immediate mode) test 3 failed"

    # Larger jump test
    # Output is 999 if input < 8, 1000 if input == 8, 1001 if input > 8
    computer = IntCode("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [7])
    computer.run()
    assert computer.output_values[0] == 999, "Larger jump test 1 failed"
    computer = IntCode("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [8])
    computer.run()
    assert computer.output_values[0] == 1000, "Larger jump test 2 failed"
    computer = IntCode("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [9])
    computer.run()
    assert computer.output_values[0] == 1001, "Larger jump test 3 failed" 

    print("All tests passed.")