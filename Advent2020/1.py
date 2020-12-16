from itertools import combinations


def Part1(values):
    for value1, value2 in combinations(values, 2):
        if value1 + value2 == 2020:
            return value1 * value2
                
                
def Part2(values):
    for value1, value2, value3 in combinations(values, 3):
        if value1 + value2 + value3 == 2020:
            return value1 * value2 * value3
                    
                    
if __name__ == "__main__":
    values = []
    with open("1.txt", "r") as infile:
        for value in infile.read().splitlines():
            if len(value) > 0:
                values.append(int(value))
                
    part1 = Part1(values)
    print(f"Part 1: {part1}")
    assert part1 == 703131

    part2 = Part2(values)
    print(f"Part 2: {part2}")
    assert part2 == 272423970
