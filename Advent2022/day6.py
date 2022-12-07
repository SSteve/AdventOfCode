TESTS = [("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
         ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
         ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
         ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
         ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26)]


def find_start(signal: str, chunk_length: int) -> int:
    for i in range(chunk_length, len(signal)):
        unique = set(signal[i-chunk_length:i])
        if len(unique) == chunk_length:
            return i
    return -1


def find_start_of_packet(signal: str) -> int:
    return find_start(signal, 4)


def find_start_of_message(signal: str) -> int:
    return find_start(signal, 14)


if __name__ == "__main__":
    for test in TESTS:
        part1test = find_start_of_packet(test[0])
        print(f"Part 1 test: {part1test}")
        assert (part1test == test[1])
        part2test = find_start_of_message(test[0])
        print(f"Part 2 test: {part2test}")
        assert (part2test == test[2])

    with open("day6.txt") as infile:
        signal = infile.read()

    part1 = find_start_of_packet(signal)
    print(f"Part 1: {part1}")

    part2 = find_start_of_message(signal)
    print(f"Part 2: {part2}")
