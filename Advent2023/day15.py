import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Self

TEST = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


@dataclass(frozen=True)
class Lens:
    label: str
    focal_length: int

    def __repr__(self):
        return f"{self.label} {self.focal_length}"

    def __eq__(self, other: Self) -> bool:
        return self.label == other.label

    def __hash__(self) -> int:
        return hash(self.label)


step_regex = re.compile(r"(\w+)")
focal_length_regex = re.compile(r".*(\d)")


def calculate_hash(input: str) -> int:
    result = 0
    for c in input:
        v = ord(c)
        result = result + v
        result = (result + (result << 4)) & 0xFF
    return result


def hash_for_input(input: str) -> int:
    return sum(calculate_hash(s) for s in input.split(","))


def process_instructions(input: str) -> dict[int, Lens]:
    boxes: dict[int, Lens] = defaultdict(list)
    for step in input.split(","):
        label = re.match(step_regex, step)[0]
        box = calculate_hash(label)
        if "-" in step:
            if box in boxes:
                boxes[box] = [lens for lens in boxes[box] if lens.label != label]
        else:
            focal_length = int(re.findall(focal_length_regex, step)[0])
            new_lens = Lens(label, focal_length)
            if any(lens.label == label for lens in boxes[box]):
                index = boxes[box].index(new_lens)
                boxes[box][index] = new_lens
            else:
                boxes[box].append(new_lens)
    return boxes


def box_power(box_index: int, box: list[Lens]) -> int:
    result = 0
    for i, lens in enumerate(box):
        result += (box_index + 1) * (i + 1) * lens.focal_length
    return result


def calculate_focusing_power(input: str) -> int:
    boxes = process_instructions(input)
    focusing_power = 0
    for box_index, box in boxes.items():
        focusing_power += box_power(box_index, box)
    return focusing_power


if __name__ == "__main__":
    part1test = hash_for_input(TEST)
    print(f"Part 1 test: {part1test}")
    assert part1test == 1320

    part2test = calculate_focusing_power(TEST)
    print(f"Part 2 test: {part2test}")
    assert part2test == 145

    with open("day15.txt") as infile:
        lines = infile.read()

    part1 = hash_for_input(lines)
    print(f"Part 1: {part1}")
    assert part1 == 510273

    part2 = calculate_focusing_power(lines)
    print(f"Part 2: {part2}")
