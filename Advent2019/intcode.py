class IntCode():
    def __init__(self, initial_memory):
        self.memory = [int(x) for x in initial_memory.split(",")]
        self.instruction_pointer = 0
        self.halted = False
        
    def run(self):
        while not self.halted:
            opcode = self.memory[self.instruction_pointer] % 100
            if opcode == 1:
                self.add()
            elif opcode == 2:
                self.multiply()
            elif opcode == 99:
                self.halt()
            else:
                raise ValueError(f"Unknown opcode: {opcode} at position {self.instruction_pointer}")
        
    def store(self, address, value):
        self.memory[address] = value
        
    def read(self, address):
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
        
    computer.store(1, 12)
    computer.store(2, 2)
    print(computer.disassemble())
    computer.run()
    
    assert computer.read(0) == 3765464, "Day 2 assertion (addition and multiplication in position mode) failed."
