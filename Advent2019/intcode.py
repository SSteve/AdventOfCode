# TODO: Reduce code duplication by calculating addressing modes in run()

from collections import defaultdict
from enum import IntEnum
from queue import SimpleQueue
from typing import Dict, List

class AddressingMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

class IntCode():
    def __init__(self, initial_memory: str, input_queue: List[int] = [], interactive: bool = True):
        self.memory: List[int] = [int(x) for x in initial_memory.split(",")]
        self.instruction_pointer:int = 0
        self.halted: bool = False
        self.waiting_for_input: bool = False
        self.input_queue: List[int] = input_queue
        self.output_values: List[int] = []
        self.relative_base: int = 0
        # This is kindof a kludge. It was added after the spec of needing more memory than the original
        # program size. But it works.
        self.extended_memory: Dict[int, int] = defaultdict(int)

        # In interactive mode, input is taken from the terminal. When interactive mode
        # is false, the computer stops and can be restarted after input is available.
        # Defaults to true so that previous problems don't break.
        self.interactive_mode: bool = interactive
        
    def run(self):
        # Set waiting_for_input to false in case we are restarting after receiving new input
        self.waiting_for_input = False
        while not self.halted and not self.waiting_for_input:
            opcode: int = self.get_memory(self.instruction_pointer) % 100
            if opcode == 1:
                self._add()
            elif opcode == 2:
                self._multiply()
            elif opcode == 3:
                self._input()
            elif opcode == 4:
                self._output()
            elif opcode == 5:
                self._jump_if_true()
            elif opcode == 6:
                self._jump_if_false()
            elif opcode == 7:
                self._less_than()
            elif opcode == 8:
                self._equals()
            elif opcode == 9:
                self._set_relative_base()
            elif opcode == 99:
                self._halt()
            else:
                raise ValueError(f"Unknown opcode: {opcode} at position {self.instruction_pointer}")
        
    def set_memory(self, address: int, value: int):
        """Set data at given address to value"""
        if address < len(self.memory):
            self.memory[address] = value
        else:
            self.extended_memory[address] = value
        
    def get_memory(self, address: int):
        """Get data at given address"""
        if address < len(self.memory):
            return self.memory[address]
        return self.extended_memory[address]
        
    def core_dump(self):
        return self.memory

    def accept_input(self, input_value: int):
        self.input_queue.append(input_value)

    def _read_next(self, addressing_mode: AddressingMode = AddressingMode.POSITION):
        """Read the next value from memory and advance the instruction pointer."""
        if addressing_mode == AddressingMode.IMMEDIATE:
            result = self.get_memory(self.instruction_pointer)
        elif addressing_mode == AddressingMode.RELATIVE:
            result = self.get_memory(self.get_memory(self.instruction_pointer) + self.relative_base)
        else:
            # position mode
            result = self.get_memory(self.get_memory(self.instruction_pointer))
        self.instruction_pointer += 1
        return result

    def _get_destination(self, addressing_mode: AddressingMode):
        """Get the destination from the next value in memory."""
        destination = self._read_next(AddressingMode.IMMEDIATE)
        if addressing_mode == AddressingMode.RELATIVE:
            destination += self.relative_base
        return destination
            
    def _halt(self):
        self.instruction_pointer += 1
        self.halted = True
                
    def _add(self):
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        addend1 = self._read_next(addressing_modes % 10)
        addressing_modes //= 10
        addend2 = self._read_next(addressing_modes % 10)
        addressing_modes //= 10
        destination = self._get_destination(addressing_modes % 10)
        summand = addend1 + addend2
        self.set_memory(destination, summand)
        return summand
        
    def _multiply(self):
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        factor1 = self._read_next(addressing_modes % 10)
        addressing_modes //= 10
        factor2 = self._read_next(addressing_modes % 10)
        addressing_modes //= 10
        destination = self._get_destination(addressing_modes % 10)
        product = factor1 * factor2
        self.set_memory(destination, product)
        return product
        
    def _input(self):
        if len(self.input_queue) == 0 and not self.interactive_mode:
            # If there's not input and we aren't in interactive mode, set the waiting flag and return
            # before altering the instruction pointer
            self.waiting_for_input = True
            return
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        destination = self._get_destination(addressing_modes % 10)
        if len(self.input_queue) == 0:
               value = int(_input("Enter an integer: "))
        else:
            value = self.input_queue.pop(0)
        self.set_memory(destination, value)
        
    def _output(self):
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        value = self._read_next(addressing_modes % 10)
        self.output_values.append(value) 
        
    def _jump_if_true(self):
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        value = self._read_next(addressing_modes % 10)
        addressing_modes //= 10
        address = self._read_next(addressing_modes % 10)
        if value != 0:
            self.instruction_pointer = address

    def _jump_if_false(self):
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        value = self._read_next(addressing_modes % 10)
        addressing_modes //= 10
        address = self._read_next(addressing_modes % 10)
        if value == 0:
            self.instruction_pointer = address
            
    def _less_than(self):
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        param1 = self._read_next(addressing_modes % 10)
        addressing_modes //= 10
        param2 = self._read_next(addressing_modes % 10)
        addressing_modes //= 10
        destination = self._get_destination(addressing_modes % 10)
        if param1 < param2:
            self.set_memory(destination, 1)
        else:
            self.set_memory(destination, 0)
        
    def _equals(self):
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        param1 = self._read_next(addressing_modes % 10)
        addressing_modes //= 10
        param2 = self._read_next(addressing_modes % 10)
        addressing_modes //= 10
        destination = self._get_destination(addressing_modes % 10)
        if param1 == param2:
            self.set_memory(destination, 1)
        else:
            self.set_memory(destination, 0)

    def _set_relative_base(self):
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        offset = self._read_next(addressing_modes % 10)
        self.relative_base += offset
    
    def disassemble(self):
        raise NotImplementedError("Disassemble needs to be updated")
        """
        instruction_strings = []
        starting_instruction_pointer = self.instruction_pointer
        self.instruction_pointer = 0
        opcode = 0
        while opcode != 99:
            opcode = self.get_memory(self.instruction_pointer) % 100
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
        """
        
    def disassemble_value(self, value, parameter_mode):
        raise NotImplementedError("Disassemble needs to be updated")
        """
        if parameter_mode == 1:
            return f"#{value}"
        else:
            return f"{value}"
        """
            
    def disassemble_add(self):
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        addend1 = self._read_next(AddressingMode.IMMEDIATE)
        addend2 = self._read_next(AddressingMode.IMMEDIATE)
        summand = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        return f"{self.instruction_pointer - 4}: {summand} = {self.disassemble_value(addend1, addressing_modes % 10)} + {self.disassemble_value(addend2, addressing_modes // 10 % 10)}"
        
    def disassemble_multiply(self):
        instruction = self._read_next(AddressingMode.IMMEDIATE)
        factor1 = self._read_next(AddressingMode.IMMEDIATE)
        factor2 = self._read_next(AddressingMode.IMMEDIATE)
        product = self._read_next(AddressingMode.IMMEDIATE)
        addressing_modes = instruction // 100
        return f"{self.instruction_pointer - 4}: {product} = {self.disassemble_value(factor1, addressing_modes % 10)} * {self.disassemble_value(factor2, addressing_modes // 10 % 10)}"
        
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

    # Relative base offset tests
    computer = IntCode("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
    computer.run()
    program = [int(x) for x in "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(",")]
    for i, value in enumerate(program):
        assert value == computer.get_memory(i), "Relative base offset test 1 failed"
    computer = IntCode("1102,34915192,34915192,7,4,7,99,0")
    computer.run()
    output_string = f"{computer.output_values[0]}"
    assert len(output_string) == 16, "Relative base offset test 1 failed"
    computer = IntCode("104,1125899906842624,99")
    computer.run()
    assert computer.output_values[0] == 1125899906842624

    print("All tests passed.")
