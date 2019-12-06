import re
from collections import defaultdict

assignRegex = re.compile(r"(\d+) -> (.+)")
regAssignRegex = re.compile(r"^(.{1,2}) -> (.+)")
shiftRegex = re.compile(r"(.+) (L|R)SHIFT (\d+) -> (.+)")
notRegex = re.compile(r"NOT (.+) -> (.+)")
binaryRegex = re.compile(r"(.+) (AND|OR) (.+) -> (.+)")


class Shift:
    def __init__(self, source, op, val, dest):
        self.source = source
        self.op = op
        self.val = val
        self.dest = dest

    def perform(self, values):
        values[self.dest] = self.op(values[self.source], self.val) & 0xFFFF

    def __repr__(self):
        return f"{self.source} {self.op.__name__} {self.val} -> {self.dest}"


class Not:
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    def perform(self, values):
        values[self.dest] = ~values[self.source] & 0xFFFF

    def __repr__(self):
        return f"NOT {self.source} -> {self.dest}"


class Binary:
    def __init__(self, source1, source2, op, dest):
        self.source1 = source1
        self.source2 = source2
        self.op = op
        self.dest = dest

    def perform(self, values):
        values[self.dest] = self.op(values[self.source1],
                                    values[self.source2]) & 0xFFFF

    def __repr__(self):
        return f"{self.source1} {self.op.__name__} {self.source2} -> {self.dest}"


class Assign:
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    def perform(self, values):
        values[self.dest] = values[self.source]


def day7(fileName, initialWire = None, initialValue = None):
    values = {'1': 1}
    waiting = defaultdict(list)
    with open(fileName) as infile:
        for line in infile:
            match = assignRegex.match(line)
            if match:
                values[match[2]] = int(match[1])
                continue
            match = regAssignRegex.match(line)
            if match:
                waiting[(match[1], )].append(Assign(match[1], match[2]))
                continue
            match = shiftRegex.match(line)
            if match:
                source = match[1]
                op = int.__lshift__ if match[2] == "L" else int.__rshift__
                val = int(match[3])
                dest = match[4]
                waiting[(source, )].append(Shift(source, op, val, dest))
                continue
            match = notRegex.match(line)
            if match:
                source = match[1]
                dest = match[2]
                waiting[(source, )].append(Not(source, dest))
                continue
            match = binaryRegex.match(line)
            if match:
                op = int.__and__ if match[2] == "AND" else int.__or__
                waiting[(match[1], match[3]
                         )].append(Binary(match[1], match[3], op, match[4]))
                continue
            print(f"Couldn't match line: {line}")

    if initialWire is not None:
        values[initialWire] = initialValue

    previousLength = -1
    while len(waiting) != previousLength:
        deleteKeys = set()
        for key in waiting.keys():
            if all(source in values for source in key):
                for op in waiting[key]:
                    op.perform(values)
                deleteKeys.add(key)
        previousLength = len(waiting)
        for deleteKey in deleteKeys:
            del waiting[deleteKey]

    return values, waiting


# values, waiting = day7("7test.txt")
# print()
values, waiting = day7("7.txt")
print(values['a'])
values, waiting = day7("7.txt", 'b', 16076)
print(values['a'])
