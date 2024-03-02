from math import ceil, floor, prod, sqrt

TEST = """Time:      7  15   30
Distance:  9  40  200"""


def distance_travelled(time: int, hold_time: int) -> int:
    return (time - hold_time) * hold_time


def count_ways_to_beat_record(time: int, distance: int) -> int:
    winner_count = 0

    for hold_time in range(1, time):
        test_distance = distance_travelled(time, hold_time)
        if test_distance > distance:
            winner_count += 1

    return winner_count


def record_beating_product(lines: list[str]) -> int:
    times = list(map(int, lines[0].split()[1:]))
    distances = list(map(int, lines[1].split()[1:]))

    return prod(count_ways_to_beat_record(time, distance) for time, distance in zip(times, distances))


def record_beating_count(lines: list[str]) -> int:
    time = int("".join(lines[0].split()[1:]))
    distance = int("".join(lines[1].split()[1:]))

    """
    The times where the threshold between being less or greater than the distance are a quadratic equation.
    t: race time
    h: hold time
    d: distance
    (h-t)h = d
    h^2 - th = d
    h^2 - th - d = 0
    Solve with the quadratic formula:
    a = 1
    b = -t
    c = d
    """
    # The first place where the distance becomes greater.
    lower = floor((time - sqrt(time * time - 4 * distance)) / 2)

    # The last place where the distance is greater.
    upper = ceil((time + sqrt(time * time - 4 * distance)) / 2)
    return upper - lower - 1


if __name__ == "__main__":
    part1test = record_beating_product(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 288

    part2test = record_beating_count(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 71503

    with open("day6.txt") as infile:
        lines = infile.read().splitlines()

    part1 = record_beating_product(lines)
    print(f"Part 1: {part1}")

    part2 = record_beating_count(lines)
    print(f"Part 2: {part2}")
