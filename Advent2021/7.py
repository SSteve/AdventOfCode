import math

from functools import lru_cache
from statistics import median

TEST = "16,1,2,0,4,2,7,1,2,14"


def FuelPart1(vals: list[int]) -> int:
    cheapestPosition = median(vals)
    fuel = sum(abs(p - cheapestPosition) for p in vals)
    return int(fuel)


@lru_cache(5000)
def Cost(distance: int) -> int:
    return distance * (distance + 1) // 2


# I'm pretty sure there's a better way to do this. There's probably a way to mathematically
# calculate the best position the way median() works for part 1.
def FuelPart2(vals: list[int]) -> int:
    cheapestPosition = 0
    leastFuel = math.inf
    for position in range(min(vals), max(vals) + 1):
        fuel = sum(Cost(abs(p - position)) for p in vals)
        if fuel < leastFuel:
            leastFuel = fuel
            cheapestPosition = position
    print(f"Cheapest position: {cheapestPosition}")
    return int(leastFuel)


if __name__ == "__main__":
    vals1 = [int(v) for v in TEST.split(",")]
    fuel = FuelPart1(vals1)
    assert fuel == 37
    fuel = FuelPart2(vals1)
    assert fuel == 168

    with open("7.txt", "r") as infile:
        vals2 = [int(v) for v in infile.readline().split(",")]
    print(f"Part 1: {FuelPart1(vals2)}")
    print(f"Part 2: {FuelPart2(vals2)}")
