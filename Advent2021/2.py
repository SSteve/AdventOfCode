from typing import Tuple

TEST = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def TravelCourse(lines: list[str]) -> Tuple[int, int]:
    position = 0
    depth1 = 0  # This is also aim for part 2
    depth2 = 0
    for line in lines:
        step = line.split(" ")
        if step[0] == "forward":
            position += int(step[1])
            depth2 += depth1 * int(step[1])
        elif step[0] == "down":
            depth1 += int(step[1])
        elif step[0] == "up":
            depth1 -= int(step[1])

    return position * depth1, position * depth2


if __name__ == "__main__":
    part1, part2 = TravelCourse(TEST.splitlines())
    assert part1 == 150
    assert part2 == 900

    with open("2.txt", "r") as infile:
        part1, part2 = TravelCourse(infile.read().splitlines())
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    assert part1 == 1488669
    assert part2 == 1176514794
