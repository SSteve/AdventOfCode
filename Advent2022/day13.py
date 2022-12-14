import json

TEST = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def compare_lists(list1, list2) -> int:
    for i in range(len(list1)):
        if i >= len(list2):
            # Right side ran out of items so items are not in the right order.
            return 1
        if type(list1[i]) == int and type(list2[i]) == int:
            if list1[i] == list2[i]:
                continue
            return -1 if list1[i] < list2[i] else 1
        if type(list1[i]) == list and type(list2[i]) == list:
            list_compare = compare_lists(list1[i], list2[i])
            if list_compare == 0:
                continue
            return list_compare
        if type(list1[i]) == list and type(list2[i]) == int:
            list_compare = compare_lists(list1[i], [list2[i]])
            if list_compare == 0:
                continue
            return list_compare
        if type(list1[i]) == int and type(list2[i]) == list:
            list_compare = compare_lists([list1[i]], list2[i])
            if list_compare == 0:
                continue
            return list_compare

    return -1 if len(list1) < len(list2) else 0


class Packet:
    def __init__(self, input: str) -> None:
        self.values = json.loads(input)

    def __lt__(self, other: "Packet") -> bool:
        return compare_lists(self.values, other.values) < 0


class DistressSignal:
    def __init__(self, lines: list[str]) -> None:
        i = 0
        self.packet_list: list[tuple[Packet, Packet]] = []
        while i < len(lines):
            self.packet_list.append((Packet(lines[i]), Packet(lines[i+1])))
            i += 3

    def sum_correct_indices(self) -> int:
        index_sum = 0
        for i, packets in enumerate(self.packet_list):
            if packets[0] < packets[1]:
                index_sum += i+1
        return index_sum

    def find_decoder_key(self) -> int:
        packets = []
        divider1 = Packet("[[2]]")
        divider2 = Packet("[[6]]")
        packets.append(divider1)
        packets.append(divider2)
        for packet in self.packet_list:
            packets.append(packet[0])
            packets.append(packet[1])
        packets.sort()
        divider1_index = packets.index(divider1)
        divider2_index = packets.index(divider2)
        return (divider1_index + 1) * (divider2_index + 1)


if __name__ == "__main__":
    distress_signal = DistressSignal(TEST.splitlines())

    part1test = distress_signal.sum_correct_indices()
    print(f"Part 1 test: {part1test}")
    assert (part1test == 13)
    part2test = distress_signal.find_decoder_key()
    print(f"Part 2 test: {part2test}")
    assert (part2test == 140)

    with open("day13.txt") as infile:
        distress_signal = DistressSignal(infile.read().splitlines())

    part1 = distress_signal.sum_correct_indices()
    print(f"Part 1: {part1}")
    assert (part1 < 6772)  # First incorrect answer.
    assert (part1 == 6656)

    part2 = distress_signal.find_decoder_key()
    print(f"Part 2: {part2}")
    assert (part2 == 19716)
