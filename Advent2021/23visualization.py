from dataclasses import dataclass
from random import randint
from sys import stdout, stdin
from time import sleep
from typing import Tuple

"""
Adapted from https://replit.com/talk/learn/ANSI-Escape-Codes-in-Python/22803
"""


class fg:
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"

    @staticmethod
    def rgb(r, g, b): return f"\u001b[38;2;{r};{g};{b}m"


class bg:
    black = "\u001b[40m"
    red = "\u001b[41m"
    green = "\u001b[42m"
    yellow = "\u001b[43m"
    blue = "\u001b[44m"
    magenta = "\u001b[45m"
    cyan = "\u001b[46m"
    white = "\u001b[47m"

    @staticmethod
    def rgb(r, g, b): return f"\u001b[48;2;{r};{g};{b}m"


class util:
    reset = "\u001b[0m"
    bold = "\u001b[1m"
    underline = "\u001b[4m"
    reverse = "\u001b[7m"

    clear = "\u001b[2J"
    clearline = "\u001b[2K"

    up = "\u001b[1A"
    down = "\u001b[1B"
    right = "\u001b[1C"
    left = "\u001b[1D"

    nextline = "\u001b[1E"
    prevline = "\u001b[1F"

    top = "\u001b[0;0H"

    @staticmethod
    def to(x, y):
        return f"\u001b[{y};{x}H"

    @staticmethod
    def write(text="\n"):
        stdout.write(text)
        stdout.flush()

    @staticmethod
    def writew(text="\n", wait=0.5):
        for char in text:
            stdout.write(char)
            stdout.flush()
            sleep(wait)

    @staticmethod
    def read(begin=""):
        text = ""

        stdout.write(begin)
        stdout.flush()

        while True:
            char = ord(stdin.read(1))

            if char == 3:
                return
            elif char in (10, 13):
                return text
            else:
                text += chr(char)

    @staticmethod
    def readw(begin="", wait=0.5):
        text = ""

        for char in begin:
            stdout.write(char)
            stdout.flush()
            sleep(wait)

        while True:
            char = ord(stdin.read(1))

            if char == 3:
                return
            elif char in (10, 13):
                return text
            else:
                text += chr(char)


def demo():
    util.write(bg.rgb(210, 210, 210) + fg.rgb(50, 50, 50) +
               util.bold + "Hello, World!\n")

    util.write(bg.black + fg.green)
    util.write(util.clear)
    util.write(util.top)

    util.writew("CRT", 0.1)
    util.writew("." * randint(3, 8))
    util.write()

    util.writew("OS", 0.1)
    util.writew("." * randint(3, 8))
    util.write()

    util.write(util.to(30, 6))
    util.writew("USERS", 0.1)
    util.writew("." * randint(3, 8))
    util.write()

    sleep(3)
    util.write(util.clear)
    util.write(util.top)

    login = util.readw("LOGIN: ", 0.1)

    util.writew(f"Logging in as {login}", 0.1)
    util.writew("." * randint(1, 8))
    util.write()

    sleep(3)
    util.write(util.clear)
    util.write(util.top)

    util.write(util.reset)


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y


def WriteChar(c: str):
    util.write(colors[c] + c)


def PointToScreen(p: Point) -> Tuple[int, int]:
    return p.x + 2, -p.y + 2


if __name__ == "__main__":
    colors: dict[str, str] = {
        'A': bg.black + fg.rgb(0x01, 0xD3, 0xFC),
        'B': bg.black + fg.rgb(0xF4, 0xD7, 0x5E),
        'C': bg.black + fg.rgb(0x2E, 0xCC, 0x71),
        'D': bg.black + fg.rgb(0xFB, 0x4C, 0x1F),
        '#': bg.black + fg.rgb(100, 100, 100),
        ' ': bg.black + fg.rgb(100, 100, 100),
        '.': bg.black + fg.rgb(100, 100, 100),
    }

    def MovePoint(char: str, startPoint: Point, endPoint: Point) -> None:
        PAUSE_TIME = 0.15
        if startPoint.y < endPoint.y:
            # Moving from a room to the hall.
            # Move up.
            for y in range(startPoint.y, 0):
                util.write(util.to(*PointToScreen(Point(startPoint.x, y))))
                WriteChar('.')
                util.write(util.to(*PointToScreen(Point(startPoint.x, y + 1))))
                WriteChar(char)
                util.write(util.to(0, 8))
                util.writew(' ', PAUSE_TIME)
            # Move left or right.
            for x in range(startPoint.x, endPoint.x) if endPoint.x > startPoint.x else range(startPoint.x, endPoint.x, -1):
                util.write(util.to(*PointToScreen(Point(x, 0))))
                WriteChar('.')
                util.write(util.to(
                    *PointToScreen(Point(x + 1 if endPoint.x > startPoint.x else x - 1, 0))))
                WriteChar(char)
                util.write(util.to(0, 8))
                util.writew(' ', PAUSE_TIME)
        else:
            # Moving from the hall to a room.
            # Move left or right.
            for x in range(startPoint.x, endPoint.x) if endPoint.x > startPoint.x else range(startPoint.x, endPoint.x, -1):
                util.write(util.to(*PointToScreen(Point(x, 0))))
                WriteChar('.')
                util.write(util.to(
                    *PointToScreen(Point(x + 1 if endPoint.x > startPoint.x else x - 1, 0))))
                WriteChar(char)
                util.write(util.to(0, 8))
                util.writew(' ', PAUSE_TIME)
            # Move down.
            for y in range(0, endPoint.y, -1):
                util.write(util.to(*PointToScreen(Point(endPoint.x, y))))
                WriteChar('.')
                util.write(util.to(*PointToScreen(Point(endPoint.x, y - 1))))
                WriteChar(char)
                util.write(util.to(0, 8))
                util.writew(' ', PAUSE_TIME)

    util.write(util.clear)
    util.write(util.top)

    util.write(colors[' '] + "#############\n")
    util.write("#...........#\n")
    util.write("### # # # ###\n")
    util.write("  # # # # #\n")
    util.write("  # # # # #\n")
    util.write("  # # # # #\n")
    util.write('  #########')

    with open("23output-example.txt", "r") as infile:
        previous = None
        for line in infile:
            current: dict[str, list[Point]] = eval(line)
            if previous is None:
                for char in current:
                    for p in current[char]:
                        util.write(util.to(*PointToScreen(p)) +
                                   colors[char] + char)
                        util.write(util.to(0, 8) + ' ')
                sleep(1)
            else:
                for char in current:
                    previousPoints = set(previous[char])
                    currentPoints = set(current[char])
                    if (previousPoints == currentPoints):
                        continue
                    startPoint = previousPoints.difference(currentPoints).pop()
                    endPoint = currentPoints.difference(previousPoints).pop()
                    MovePoint(char, startPoint, endPoint)
                    break

            previous = current
