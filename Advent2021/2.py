from typing import Tuple

TEST = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def TravelCourse1(lines: list[str]) -> Tuple[int, int]:
    position = 0
    depth = 0
    for line in lines:
        step = line.split(" ")
        if step[0] == "forward":
            position += int(step[1])
        elif step[0] == "down":
            depth += int(step[1])
        elif step[0] == "up":
            depth -= int(step[1])

    return position, depth

def TravelCourse2(lines: list[str]) -> Tuple[int, int]:
    position = 0
    depth = 0
    aim = 0
    for line in lines:
        step = line.split(" ")
        if step[0] == "forward":
            position += int(step[1])
            depth += aim * int(step[1])
        elif step[0] == "down":
            aim += int(step[1])
        elif step[0] == "up":
            aim -= int(step[1])

    return position, depth


if __name__ == "__main__":
    position, depth = TravelCourse1(TEST.splitlines())
    assert position * depth == 150
    position, depth = TravelCourse2(TEST.splitlines())
    assert position * depth == 900

    with open("2.txt", "r") as infile:
        position, depth = TravelCourse1(infile.read().splitlines())
    print(f"Part 1: {position} * {depth} = {position * depth}")
    with open("2.txt", "r") as infile:
        position, depth = TravelCourse2(infile.read().splitlines())
    print(f"Part 2: {position} * {depth} = {position * depth}")
