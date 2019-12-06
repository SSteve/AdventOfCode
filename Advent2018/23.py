import re

from collections import namedtuple

positionCompiler = re.compile(r"pos=<([\-\d]+),([\-\d]+),([\-\d]+)>, r=(\d+)")

Nanobot = namedtuple('Nanobot', ['x', 'y', 'z', 'radius'])



nanobots = []


def distance(bot1, bot2):
    return abs(bot1.x - bot2.x) + abs(bot1.y - bot2.y) + abs(bot1.z - bot2.z)


def a23(fileName):
    largestRadiusBot = None
    with open(fileName, "r") as infile:
        for line in infile:
            match = positionCompiler.match(line)
            if match:
                bot = Nanobot(*[int(x) for x in match.group(1, 2, 3, 4)])
                if largestRadiusBot is None or bot.radius > largestRadiusBot.radius:
                    largestRadiusBot = bot
                nanobots.append(bot)
    reachableBots = 0
    for bot in nanobots:
        botDistance = distance(bot, largestRadiusBot)
        if botDistance <= largestRadiusBot.radius:
            reachableBots += 1
    print(reachableBots)


if __name__ == "__main__":
    a23("23.txt")
