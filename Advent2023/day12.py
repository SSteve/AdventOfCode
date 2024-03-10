from collections import deque
from dataclasses import dataclass

TEST = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

"""
https://www.reddit.com/r/adventofcode/comments/18ghux0/2023_day_12_no_idea_how_to_start_with_this_puzzle/
if it starts with a ., discard the . and recursively check again.

if it starts with a ?, replace the ? with a . and recursively check again, AND replace it with a # and recursively check again.

it it starts with a #, check if it is long enough for the first group, check if all characters in the first [grouplength] characters are not '.', and then remove the first [grouplength] chars and the first group number, recursively check again.

at some point you will get to the point of having an empty string and more groups to do - that is a zero. or you have an empty string with zero gropus to do - that is a one.

there are more rules to check than these few, which are up to you to find. but this is a way to work out the solution.
"""


@dataclass(frozen=True)
class SpringRecord:
    springs: str
    counts: tuple[int]


def count_arrangements(springs: SpringRecord) -> int:
    to_count: deque[SpringRecord] = deque()
    to_count.append(springs)
    count = 0

    while to_count:
        next = to_count.popleft()
        if len(next.springs) == 0:
            if len(next.counts) == 0:
                count += 1
            continue

        if next.springs[0] == ".":
            to_count.append(SpringRecord(next.springs[1:], next.counts))
            continue

        if next.springs[0] == "?":
            # Replace '?' with '.' and go ahead and remove the '.' to avoid a loop.
            to_count.append(SpringRecord(next.springs[1:], next.counts))
            to_count.append(SpringRecord("#" + next.springs[1:], next.counts))
            continue

        # Now we know the first character is '#'.
        if len(next.counts) == 0 or len(next.springs) < next.counts[0]:
            # Not a valid arrangement.
            continue

        if any(c == "." for c in next.springs[: next.counts[0]]):
            # There's a working string within this count. Not a valid arrangement.
            continue

        if len(next.springs) > next.counts[0] and next.springs[next.counts[0]] == "#":
            # The character after the count is a broken spring. Not a valid arrangement.
            continue

        # Remove the number of characters in this count and the count. The character after
        # the characters we're removing must be a working spring (whether it's an unknown
        # condition or known working) so we'll remove that too.
        to_count.append(
            SpringRecord(next.springs[next.counts[0] + 1 :], next.counts[1:])
        )

    return count


def count_all_arrangements(lines: list[str]) -> int:
    counts = 0

    for line in lines:
        springs, count_string = line.split()
        count_tuple = tuple(map(int, count_string.split(",")))
        counts += count_arrangements(SpringRecord(springs, count_tuple))

    return counts


if __name__ == "__main__":
    part1test = count_all_arrangements(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 21

    """     
    part2test = trench_size_2(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    # assert part2test == 952_408_144_115
 """
    with open("day12.txt") as infile:
        lines = infile.read().splitlines()

    part1 = count_all_arrangements(lines)
    print(f"Part 1: {part1}")
    # assert part1 == 106459

    """ 
    part2 = trench_size_2(lines)
    print(f"Part 2: {part2}")
 """
