from collections import deque
from functools import reduce
from operator import mul
from typing import Iterable, Tuple


class BitProvider:
    def __init__(self, characters: str) -> None:
        self.characters: deque[str] = deque(characters)
        self.currentBits: deque[int] = deque()

    def _BitsFromNextChar(self) -> None:
        nextChar = self.characters.popleft()
        value = int(nextChar, 16)
        for i in range(4):
            self.currentBits.append(value >> (3-i) & 1)

    def GetBits(self, bitCount: int) -> deque[int]:
        bits = deque()
        while len(self.currentBits) < bitCount:
            self._BitsFromNextChar()
        for _ in range(bitCount):
            bits.append(self.currentBits.popleft())
        return bits

    def ValueFromBits(self, bitCount) -> int:
        result = 0
        bits = self.GetBits(bitCount)
        for i in range(bitCount):
            result = (result << 1) + bits.popleft()
        return result

    def GetLiteralValue(self) -> Tuple[int, int]:
        """
        Get the next literal value from the bit provider. We've already
        read the version and type id. The next bits from the provider
        will be the ones that make up the value.
        """
        done = False
        bitsRead = 0
        result = 0
        while not done:
            done = self.ValueFromBits(1) == 0
            value = self.ValueFromBits(4)
            result = (result << 4) + value
            bitsRead += 5
        return result, bitsRead


class Packet:
    def __init__(self) -> None:
        self.bitsRead = 0
        self.version = -1
        self.typeId = -1
        self.literalValue = -1
        self.subPackets: list['Packet'] = []

    def VersionSum(self) -> int:
        return self.version + sum(child.VersionSum() for child in self.subPackets)

    def TotalBitsRead(self) -> int:
        return self.bitsRead + sum(child.TotalBitsRead() for child in self.subPackets)

    def ChildCalculations(self) -> Iterable[int]:
        for child in self.subPackets:
            yield child.PerformCalculation()

    def PerformCalculation(self) -> int:
        if self.typeId == 4:
            return self.literalValue
        elif self.typeId == 0:
            return sum(self.ChildCalculations())
        elif self.typeId == 1:
            return reduce(mul, (self.ChildCalculations()), 1)
        elif self.typeId == 2:
            return min(self.ChildCalculations())
        elif self.typeId == 3:
            return max(self.ChildCalculations())
        elif self.typeId == 5:
            return int(self.subPackets[0].PerformCalculation() > self.subPackets[1].PerformCalculation())
        elif self.typeId == 6:
            return int(self.subPackets[0].PerformCalculation() < self.subPackets[1].PerformCalculation())
        elif self.typeId == 7:
            return int(self.subPackets[0].PerformCalculation() == self.subPackets[1].PerformCalculation())
        else:
            raise ValueError(f"Invalid typeID ({self.typeId})")

    def DotRepresentation(self) -> Iterable[str]:
        if self.typeId == 4:
            label = self.literalValue
        else:
            label = ['+', '×', 'min', 'max', '', '>', '<', '='][self.typeId]
        yield f'    x{id(self)} [label="{label}"]'
        for child in self.subPackets:
            for line in child.DotRepresentation():
                yield line
            yield f'    x{id(self)} -> x{id(child)}'

    def WriteToDotFile(self, filename: str) -> None:
        """
        Return a Graphviz representation to the given file.
        The dot file can be converted to PDF with the command:
        dot -Tpdf -O 16.dot
        """
        with open("16.dot", "w") as dotFile:
            print("digraph packets {", file=dotFile)
            for line in self.DotRepresentation():
                print(line, file=dotFile)
            print("}", file=dotFile)

    @classmethod
    def FromBits(cls, bits: BitProvider) -> 'Packet':
        packet = Packet()
        packet.version = bits.ValueFromBits(3)
        packet.typeId = bits.ValueFromBits(3)
        packet.bitsRead = 6
        if packet.typeId == 4:
            packet.literalValue, bitsRead = bits.GetLiteralValue()
            packet.bitsRead += bitsRead
        else:
            lengthTypeId = bits.GetBits(1).pop()
            packet.bitsRead += 1
            if lengthTypeId == 0:
                # The next 15 bits are the total length in bits of the sub-packets
                # contained by this packet.
                subPacketBits = bits.ValueFromBits(15)
                packet.bitsRead += 15
                subPacketBitsRead = 0
                while subPacketBitsRead < subPacketBits:
                    childPacket = Packet.FromBits(bits)
                    subPacketBitsRead += childPacket.TotalBitsRead()
                    packet.subPackets.append(childPacket)
            else:
                # The next 11 bits are the total number of sub-packets immediately
                # contained by this packet.
                subPacketCount = bits.ValueFromBits(11)
                packet.bitsRead += 11
                for _ in range(subPacketCount):
                    childPacket = Packet.FromBits(bits)
                    packet.subPackets.append(childPacket)

        return packet


if __name__ == "__main__":
    transmission = BitProvider("D2FE28")
    packet = Packet.FromBits(transmission)
    assert packet.literalValue == 2021 and packet.bitsRead == 21

    transmission = BitProvider("38006F45291200")
    packet = Packet.FromBits(transmission)
    assert packet.subPackets[0].literalValue == 10 and \
        packet.subPackets[1].literalValue == 20

    transmission = BitProvider("EE00D40C823060")
    packet = Packet.FromBits(transmission)
    assert packet.subPackets[0].literalValue == 1 and \
        packet.subPackets[1].literalValue == 2 and \
        packet.subPackets[2].literalValue == 3

    transmission = BitProvider("8A004A801A8002F478")
    packet = Packet.FromBits(transmission)
    assert packet.VersionSum() == 16

    transmission = BitProvider("620080001611562C8802118E34")
    packet = Packet.FromBits(transmission)
    assert packet.VersionSum() == 12

    transmission = BitProvider("C0015000016115A2E0802F182340")
    packet = Packet.FromBits(transmission)
    assert packet.VersionSum() == 23

    transmission = BitProvider("A0016C880162017C3686B18A3D4780")
    packet = Packet.FromBits(transmission)
    assert packet.VersionSum() == 31

    transmission = BitProvider("C200B40A82")
    assert Packet.FromBits(transmission).PerformCalculation() == 3

    transmission = BitProvider("04005AC33890")
    assert Packet.FromBits(transmission).PerformCalculation() == 54

    transmission = BitProvider("880086C3E88112")
    assert Packet.FromBits(transmission).PerformCalculation() == 7

    transmission = BitProvider("CE00C43D881120")
    assert Packet.FromBits(transmission).PerformCalculation() == 9

    transmission = BitProvider("D8005AC2A8F0")
    assert Packet.FromBits(transmission).PerformCalculation() == 1

    transmission = BitProvider("F600BC2D8F")
    assert Packet.FromBits(transmission).PerformCalculation() == 0

    transmission = BitProvider("9C005AC2F8F0")
    assert Packet.FromBits(transmission).PerformCalculation() == 0

    transmission = BitProvider("9C0141080250320F1802104A08")
    assert Packet.FromBits(transmission).PerformCalculation() == 1

    with open("16.txt", "r") as infile:
        transmission = BitProvider(infile.readline())
    packet = Packet.FromBits(transmission)
    part1 = packet.VersionSum()
    part2 = packet.PerformCalculation()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

    packet.WriteToDotFile("16.dot")
