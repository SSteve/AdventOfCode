from collections import namedtuple
from dataclasses import dataclass

from typing import Tuple
import math
import re

"""
X & Y are independent. Find the initial velocities that will work for each.

v = initial velocity

t   p
__________________________
0   0
1   v
2   v + (v - 1)                     = 2v - 1
3   v + (v - 1) + (v - 2)           = 3v - 3
4   v + (v - 1) + (v - 2) + (v - 3) = 4v - 6
n = nv - (n * (n - 1)) / 2
  = nv - (n^2 - n) / 2

x stops increasing at n == v. Substituting v for n in the last equation
gives the highest x value:
maxX = v^2 - (v^2 - v) / 2
     = (2v^2 - v^2 + v) / 2
     = (v^2 + v) / 2

In order for x to reach the left side of the area, maxX must be >= the left side:
maxX >= left
(v^2 + v) / 2 >= left
v^2 + v >= 2 * left
v^2 + v - 2 * left >= 0
Using the quadratic formula:
(-1 ± sqrt(1 - 4 * (-2 * left))) / 2 >= 0
We can discard the negative square root because that gives us a negative value.
(-1 + sqrt(1 + 8 * left)) / 2 >= 0
sqrt(8 * left + 1) / 2 >=0

Y is at maximum when its first derivative is zero. The first derivative of
nv - (n^2 - n) / 2 is n so the maximum Y value is when the step number is
the same as the initial velocity.
"""

TEST = """target area: x=20..30, y=-10..-5"""

Point = namedtuple('Point', ['x', 'y'])


@dataclass
class Target:
    minX: int
    maxX: int
    minY: int
    maxY: int


def FindTarget(input: str) -> Target:
    match = re.match(
        r"target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)", input)
    if match is not None:
        target = Target(int(match[1]), int(match[2]),
                        int(match[3]), int(match[4]))
    else:
        target = Target(0, 0, 0, 0)
    return target


def Day17(input: str) -> Tuple[int, int]:
    target = FindTarget(input)

    # Calculate the minimum initial x velocity (see notes above).
    # This is also the largest number of steps it will take to
    # reach the left edge of the target. Any number of steps more than
    # this will be in the left edge of the target.
    minV0x = math.ceil((math.sqrt(8 * target.minX + 1) - 1) / 2)
    maxV0x = target.maxX
    maxV0y = 0
    maxY = 0
    # Use brute force to find the maximum initial y velocity. There's probably
    # a better way to know when to stop searching in higher V0y values, but
    # this works in a reasonable amount of time.
    for V0y in range(1, 1000):
        y = 0
        step = 0
        while y > target.minY:
            step += 1
            y = int(step * V0y - ((step**2 - step) / 2))
            if target.minY <= y <= target.maxY:
                maxV0y = V0y

    maxY = int((maxV0y**2 + maxV0y) / 2)

    # We've found the highest viable initial y velocity. Now find all
    # combinations of initial velocities that result in the probe
    # being within the target at the end of a step.
    startVelocities: set[Point] = set()
    minV0y = target.minY
    for V0y in range(minV0y, maxV0y + 1):
        y = 0
        step = 0
        while y > target.minY:
            step += 1
            y = int(step * V0y - ((step**2 - step) / 2))
            if target.minY <= y <= target.maxY:
                for V0x in range(minV0x, maxV0x + 1):
                    if step <= V0x:
                        x = int(step * V0x - ((step**2 - step) / 2))
                    else:
                        # X velocity has reached 0 so X is at its maximum position.
                        x = int((V0x**2 + V0x) / 2)
                    if target.minX <= x <= target.maxX:
                        startVelocities.add(Point(V0x, V0y))

    return maxY, len(startVelocities)


if __name__ == "__main__":
    part1, part2 = Day17(TEST)
    assert part1 == 45
    assert part2 == 112

    with open("17.txt", "r") as infile:
        input = infile.readline()
    part1, part2 = Day17(input)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
