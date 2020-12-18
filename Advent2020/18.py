from collections import deque


def Eval(input: deque[str]) -> int:
    stack = []
    for token in input:
        if token in '0123456789':
            stack.append(int(token))
        elif token == '+':
            stack.append(stack.pop() + stack.pop())
        elif token == '*':
            stack.append(stack.pop() * stack.pop())
        else:
            raise ValueError(f"Unknown token: {token}")
    if len(stack) != 1:
        raise ValueError(f"Error evaluating. Stack: {stack}")
    return stack.pop()


def Parse(input: str, precedence: dict[str, int]) -> int:
    output = deque()
    operators = []
    for char in input:
        if char == ' ':
            continue
        elif char in '0123456789':
            output.append(char)
        elif char in '+*':
            while len(operators) and operators[-1] in '+*' and precedence[operators[-1]] >= precedence[char]:
                output.append(operators.pop())
            operators.append(char)
        elif char == '(':
            operators.append(char)
        elif char == ')':
            while len(operators) and operators[-1] != '(':
                output.append(operators.pop())
            if len(operators) == 0:
                raise ValueError("Mis-matched parentheses.")
            # Discard the left parenthesis
            operators.pop()
        else:
            raise ValueError(f"Unknown input: {char}")
    while len(operators):
        output.append(operators.pop())
    return Eval(output)


def Part1(input: str) -> int:
    precedence = {'+': 1, '*': 1}
    return Parse(input, precedence)


def Part2(input: str) -> int:
    precedence = {'+': 2, '*': 1}
    return Parse(input, precedence)


assert Part1("2 * 3 + (4 * 5)") == 26
assert Part1("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert Part1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert Part1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

assert Part2("2 * 3 + (4 * 5)") == 46
assert Part2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert Part2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert Part2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340


with open("18.txt", "r") as infile:
    lines = infile.read().splitlines()
part1 = sum(Part1(line) for line in lines)
print(f"Part 1: {part1}")
part2 = sum(Part2(line) for line in lines)
print(f"Part 2: {part2}")
