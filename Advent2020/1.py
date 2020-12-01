def part1(values):
    for lineNo, value1 in enumerate(values):
        for value2 in values[lineNo + 1:]:
            if value1 + value2 == 2020:
                print(value1 * value2)
                return
                
                
def part2(values):
    for lineNo1, value1 in enumerate(values):
        for lineNo2, value2 in enumerate(values[lineNo1 + 1:]):
            for value3 in values[lineNo2 + 1:]:
                if value1 + value2 + value3 == 2020:
                    print(value1 * value2 * value3)
                    return
                    
                    
if __name__ == "__main__":
    values = []
    with open("1.txt", "r") as infile:
        for value in infile:
            if len(value.strip()) > 0:
                values.append(int(value.strip()))
    part1(values)
    part2(values)

