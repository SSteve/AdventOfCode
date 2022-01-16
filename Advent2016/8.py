import re

TEST = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
rect 3x1"""

rectInstruction = re.compile(r"rect (\d+)x(\d+)")
columnInstruction = re.compile(r"rotate column x=(\d+) by (\d+)")
rowInstruction = re.compile(r"rotate row y=(\d+) by (\d+)")


class Screen:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.pixels: list[list[str]] = []
        line = [' '] * width
        for _ in range(height):
            self.pixels.append(line[:])

    def __repr__(self) -> str:
        return '\n'.join(''.join(line) for line in self.pixels)

    def Rect(self, width: int, height: int) -> None:
        for y in range(height):
            for x in range(width):
                self.pixels[y][x] = '#'

    def Column(self, column: int, delta: int) -> None:
        currentColumn = ''.join(self.pixels[y][column]
                                for y in range(self.height))
        for y in range(self.height):
            newY = (y + delta) % self.height
            self.pixels[newY][column] = currentColumn[y]

    def Row(self, row: int, delta: int) -> None:
        pixelRow = self.pixels[row]
        offset = self.width - delta
        pixelRow[delta:], pixelRow[:delta] = pixelRow[:offset], pixelRow[offset:]

    def ProcessInstructions(self, instructions: list[str]) -> None:
        for instruction in instructions:
            if match := re.match(rectInstruction, instruction):
                self.Rect(int(match[1]), int(match[2]))
            elif match := re.match(columnInstruction, instruction):
                self.Column(int(match[1]), int(match[2]))
            elif match := re.match(rowInstruction, instruction):
                self.Row(int(match[1]), int(match[2]))
            else:
                raise ValueError(f"Unrecognized instructions: {instruction}")

    def CountPixels(self) -> int:
        return sum(ch == '#' for ch in repr(self))


if __name__ == '__main__':
    screen = Screen(7, 3)
    screen.ProcessInstructions(TEST.splitlines())
    part1 = screen.CountPixels()
    assert part1 == 8

    screen = Screen(50, 6)
    with open('8.txt', 'r') as infile:
        screen.ProcessInstructions(infile.read().splitlines())
    part1 = screen.CountPixels()
    print(f"Part 1: {part1}")
    print(screen)
