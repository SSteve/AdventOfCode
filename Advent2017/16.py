from collections import deque
import re

sRegex = re.compile(r"s(\d+)")
xRegex = re.compile(r"x(\d+)/(\d+)")
pRegex = re.compile(r"p(.)/(.)")


def day16(fileName, progCount, shouldPrint=False):
    with open(fileName) as infile:
        steps = infile.readline().strip().split(",")
    progs = deque([chr(p) for p in range(ord('a'), ord('a') + progCount)])
    history = [''.join(progs)]
    for danceNumber in range(20000):
        for step in steps:
            match = sRegex.match(step)
            if match:
                progs.rotate(int(match[1]))
                continue
            match = xRegex.match(step)
            if match:
                a = int(match[1])
                b = int(match[2])
                progs[a], progs[b] = progs[b], progs[a]
                continue
            match = pRegex.match(step)
            if match:
                a = progs.index(match[1])
                b = progs.index(match[2])
                progs[a], progs[b] = progs[b], progs[a]
                continue
            raise ValueError(f"Couldn't match step \"{step}\"")
        newString = ''.join(progs)
        if newString == "abcdefghijklmnop"[:progCount]:
            print(f"Repeat after dance {danceNumber + 2}")
            break
        history.append(newString)
    return history[1_000_000_000 % len(history)]


if __name__ == "__main__":
    # finish = day16("16test.txt", 5)
    # print(f"part 1: {finish}")
    finish = day16("16.txt", 16)
    print(f"part 2: {finish}")
    # pobanhfgiemdcjlk is wrong
    # dcmljghfinpokeba is wrong
