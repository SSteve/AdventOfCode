from dataclasses import dataclass

TEST = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


@dataclass
class Monkey:

    def __init__(self, lines: list[str]) -> None:
        self.items: list[int] = []
        # operation_value: int
        # divisible_value: int
        # true_destination: int
        # false_destination: int
        for item_input in [item.strip(",") for item in lines[0].split()]:
            if item_input.isnumeric():
                self.items.append(int(item_input))
        operand = lines[1][23]
        self.operand_is_plus = operand == '+'
        operation = lines[1][25:]
        if operation.isnumeric():
            self.operation_value = int(operation)
        else:
            self.operation_value = -1
        self.divisible_value = int(lines[2].split()[-1])
        self.true_destination = int(lines[3].split()[-1])
        self.false_destination = int(lines[4].split()[-1])

    def add_item(self, item: int) -> None:
        self.items.append(item)


def create_monkeys(lines: list[str]) -> list[Monkey]:
    monkeys: list[Monkey] = []

    i = 1
    while i < len(lines):
        monkey = Monkey(lines[i:i+5])
        monkeys.append(monkey)
        i += 7

    return monkeys


def calculate_monkey_business(monkeys: list[Monkey], rounds: int) -> int:
    monkey_inspection_counts: list[int] = [0] * len(monkeys)

    # Since our test is for divisibility, we can multiply all the divisible values together
    # and mod by that product in order to keep the values from increasing without bounds.
    monkey_mod = 1
    for monkey in monkeys:
        monkey_mod *= monkey.divisible_value

    for round in range(rounds):
        for (i, monkey) in enumerate(monkeys):
            monkey_inspection_counts[i] += len(monkey.items)
            for item in monkey.items:
                if monkey.operation_value < 0:
                    item = item * item
                elif monkey.operand_is_plus:
                    item = item + monkey.operation_value
                else:
                    item = item * monkey.operation_value

                if rounds == 20:
                    item = item // 3
                else:
                    item = item % monkey_mod

                if item % monkey.divisible_value == 0:
                    monkeys[monkey.true_destination].add_item(item)
                else:
                    monkeys[monkey.false_destination].add_item(item)
            monkey.items.clear()

    monkey_inspection_counts.sort()
    return monkey_inspection_counts[-1] * monkey_inspection_counts[-2]


if __name__ == "__main__":
    monkeys = create_monkeys(TEST.splitlines())
    part1test = calculate_monkey_business(monkeys, 20)
    print(f"Part 1 test: {part1test}")
    assert (part1test == 10605)
    monkeys = create_monkeys(TEST.splitlines())
    part2test = calculate_monkey_business(monkeys, 10000)
    print(f"Part 2 test: {part2test}")
    assert (part2test == 2713310158)

    with open("day11.txt") as infile:
        monkeys = create_monkeys(infile.read().splitlines())

    part1 = calculate_monkey_business(monkeys, 20)
    print(f"Part 1: {part1}")
    assert (part1 == 55944)

    with open("day11.txt") as infile:
        monkeys = create_monkeys(infile.read().splitlines())

    part2 = calculate_monkey_business(monkeys, 10000)
    print(f"Part 2: {part2}")
