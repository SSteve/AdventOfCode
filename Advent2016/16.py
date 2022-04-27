TEST = "10000"
INPUT = "10010000000110000"


def Checksum(data: str) -> str:
    assert len(data) & 1 == 0
    checksum = data
    while len(checksum) & 1 == 0:
        data = checksum
        checksum = ""
        for i in range(len(data) // 2):
            newChar = "1" if data[i * 2] == data[i * 2 + 1] else "0"
            checksum += newChar
    return checksum


def ProcessStep(data: str) -> str:
    result = data + "0"
    for i in range(len(data) - 1, -1, -1):
        newChar = "0" if data[i] == "1" else "1"
        result += newChar
    return result


def CreateData(data: str, size: int) -> str:
    while len(data) < size:
        data = ProcessStep(data)
    return data[:size]


if __name__ == '__main__':
    assert ProcessStep("1") == "100"
    assert ProcessStep("1000") == "100001110"
    assert ProcessStep("11111") == "11111000000"
    assert ProcessStep("111100001010") == "1111000010100101011110000"

    assert CreateData("10000", 20) == "10000011110010000111"
    assert CreateData(
        "1001010", 40) == "1001010010101100100101011010110010010100"

    assert Checksum("110010110100") == "100"
    assert Checksum("10000011110010000111") == "01100"
    assert Checksum("1001010010101100100101011010110010010100") == "01110"

    part1 = Checksum(CreateData(INPUT, 272))
    print(f"Part 1 = {part1}")

    part2 = Checksum(CreateData(INPUT, 35651584))
    print(f"Part 2 = {part2}")
