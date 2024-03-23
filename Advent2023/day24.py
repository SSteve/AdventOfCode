from dataclasses import dataclass
from itertools import combinations
from typing import Self

TEST = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


# Return -1, 0, 1 if x < 0, x == 0, x > 0
def sign(x):
    return x and (-1 if x < 0 else 1)


@dataclass(frozen=True)
class Hailstone:
    x: int
    y: int
    z: int
    delta_x: int
    delta_y: int
    delta_z: int
    m: float
    b: float

    @classmethod
    def from_line(cls, line: str):
        coords, deltas = line.split(" @ ")
        x, y, z = map(int, coords.split(", "))
        delta_x, delta_y, delta_z = map(int, deltas.split(", "))
        m = delta_y / delta_x
        b = y - m * x
        return cls(x, y, z, delta_x, delta_y, delta_z, m, b)

    def x_intersection(self, other: Self) -> float:
        return (other.b - self.b) / (self.m - other.m)


def count_intersections(lines: list[str], low: int, high: int) -> int:
    hailstones: set[Hailstone] = set()
    discarded = 0
    for line in lines:
        hailstone = Hailstone.from_line(line)
        if hailstone in hailstones:
            raise ValueError(f"Hailstone {hailstone} already found.")
        if (
            (hailstone.x > high and hailstone.delta_x > 0)
            or (hailstone.x < low and hailstone.delta_x < 0)
            or (hailstone.y > high and hailstone.delta_y > 0)
            or (hailstone.y < low and hailstone.delta_y < 0)
        ):
            discarded += 1
            continue
        hailstones.add(hailstone)

    intersections = 0
    for h1, h2 in combinations(hailstones, 2):
        if h1.m == h2.m:
            continue
        x = h1.x_intersection(h2)
        if x < low or x > high or sign(x - h1.x) != sign(h1.delta_x) or sign(x - h2.x) != sign(h2.delta_x):
            continue
        y = h1.m * x + h1.b
        # print(f"{x=}, {y=}, {h1}, {h2}")
        if y >= low and y <= high and sign(y - h1.y) == sign(h1.delta_y) and sign(y - h2.y) == sign(h2.delta_y):
            intersections += 1

    return intersections


if __name__ == "__main__":
    part1test = count_intersections(TEST.splitlines(), 7, 27)
    print(f"Part 1 test: {part1test}")
    assert part1test == 2

    """ 
    part2test = find_longest_hike2(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 154
 """
    with open("day24.txt") as infile:
        lines = infile.read().splitlines()

    part1 = count_intersections(lines, 200000000000000, 400000000000000)
    print(f"Part 1: {part1}")
    # assert part1 == 2402

    """ 
    part2 = find_longest_hike2(lines)
    print(f"Part 2: {part2}")
    assert part2 == 6450
 """
