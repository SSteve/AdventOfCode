TEST = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def calculate_hash(input: str) -> int:
    result = 0
    for c in input:
        v = ord(c)
        result = result + v
        result = (result + (result << 4)) & 0xFF
    return result


def hash_for_input(input: str) -> int:
    return sum(calculate_hash(s) for s in input.split(","))


if __name__ == "__main__":
    part1test = hash_for_input(TEST)
    print(f"Part 1 test: {part1test}")
    assert part1test == 1320

    """ 
    part2test = run_cycles(TEST)
    print(f"Part 2 test: {part2test}")
    assert part2test == 64
 """

    with open("day15.txt") as infile:
        lines = infile.read()

    part1 = hash_for_input(lines)
    print(f"Part 1: {part1}")
    # assert part1 == 103614

    """ 
    part2 = run_cycles(lines, 1_000_000_000)
    print(f"Part 2: {part2}")
 """
