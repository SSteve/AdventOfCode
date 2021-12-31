from collections import deque
from typing import Callable


TEST1 = """inp z
inp x
mul z 3
eql z x"""

TEST2 = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""


def isinteger(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


class Alu:
    """
    inp a - Read an input value and write it to variable a.
    add a b - Add the value of a to the value of b, then store the result in variable a.
    mul a b - Multiply the value of a by the value of b, then store the result in variable a.
    div a b - Divide the value of a by the value of b, truncate the result to an integer,
              then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
    mod a b - Divide the value of a by the value of b, then store the remainder in variable a.
              (This is also called the modulo operation.)
    eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise,
              store the value 0 in variable a.
    """

    def __init__(self) -> None:
        self.instructions: dict[str, Callable] = {
            'inp': self.inp,
            'add': self.add,
            'mul': self.mul,
            'div': self.div,
            'mod': self.mod,
            'eql': self.eql
        }

    def RunProgram(self, lines: list[str], input: deque[int]) -> None:
        self.input = input
        self.variables: dict[str, int] = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        for line in lines:
            arguments = line.split()
            if arguments[0] not in self.instructions.keys():
                raise ValueError(f"Invalid instruction ({arguments[0]}")
            if arguments[1] not in ('w', 'x', 'y', 'z'):
                raise ValueError(f"Invalid variable ({arguments[1]}")
            if len(arguments) > 2 and not \
                    (arguments[2] in ('w', 'x', 'y', 'z') or isinteger(arguments[2])):
                raise ValueError(f"Invalid second argument ({arguments[2]})")
            self.instructions[arguments[0]](*arguments[1:])

    def ValidateModelNumber(self, monad: list[str], modelNumber: str) -> bool:
        self.RunProgram(monad, deque(int(c) for c in modelNumber))
        return self.variables['z'] == 0

    def SecondArgumentValue(self, secondArgument: str) -> int:
        if isinteger(secondArgument):
            return int(secondArgument)
        return self.variables[secondArgument]

    def inp(self, variable: str) -> None:
        inputValue = self.input.popleft()
        self.variables[variable] = inputValue

    def add(self, variable: str, value: str) -> None:
        self.variables[variable] += self.SecondArgumentValue(value)

    def mul(self, variable: str, value: str) -> None:
        self.variables[variable] *= self.SecondArgumentValue(value)

    def div(self, variable: str, value: str) -> None:
        secondValue = self.SecondArgumentValue(value)
        if secondValue == 0:
            raise ValueError("Division by zero error")
        self.variables[variable] //= secondValue

    def mod(self, variable: str, value: str) -> None:
        secondValue = self.SecondArgumentValue(value)
        if self.variables[variable] < 0 or secondValue <= 0:
            raise ValueError("Invalid modulo values")
        self.variables[variable] %= secondValue

    def eql(self, variable: str, value: str) -> None:
        self.variables[variable] = int(
            self.variables[variable] == self.SecondArgumentValue(value))


if __name__ == "__main__":
    alu = Alu()
    alu.RunProgram(["inp x", "mul x -1"], deque([1]))
    assert alu.variables['x'] == -1

    alu.RunProgram(TEST1.splitlines(), deque([13, 39]))
    assert alu.variables['z'] == 1

    alu.RunProgram(TEST1.splitlines(), deque([13, 38]))
    assert alu.variables['z'] == 0

    with open("24.txt", "r") as infile:
        monad = infile.readlines()
    """
    I read a tutorial on reddit and calculated the model numbers by hand.
    I'm not sure I ever would have figured this out on my own.
    """
    for modelNumber in ['91599994399395', '71111591176151']:
        isValid = alu.ValidateModelNumber(monad, modelNumber)
        print(f"{modelNumber} {'is' if isValid else 'is not'} valid")
