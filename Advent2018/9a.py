from collections import deque
import re


def showMarbles(marbles, currentIndex, currentPlayer):
    print(f"[{currentPlayer + 1}] ", end='')
    for marbleIndex, marble in enumerate(marbles):
        if marbleIndex == currentIndex:
            print(f"({marble})", end='')
        else:
            print(f" {marble} ", end='')
    print()


compiled = re.compile(r"(\d+) players; last marble is worth (\d+) points")

with open("9.txt", "r") as infile:
    for line in infile:
        match = compiled.match(line)
        if match:
            playerCount = int(match[1])
            lastMarble = int(match[2])

marbles = deque([0])
currentMarbleIndex = 0
scores = [0] * playerCount
currentPlayer = 0

for marble in range(1, lastMarble + 1):
    if marble % 23:
        # Normal marble: place the marble in the circle
        marbles.rotate(-1)
        marbles.append(marble)
    else:
        # Marble is a multiple of 23, so do special action
        scores[currentPlayer] += marble
        marbles.rotate(7)
        scores[currentPlayer] += marbles.pop()
        marbles.rotate(-1)

    # showMarbles(marbles, currentMarbleIndex, currentPlayer)

    currentPlayer = (currentPlayer + 1) % playerCount

print(max(scores))
