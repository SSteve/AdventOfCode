from typing import Tuple

with open("1.txt", "r") as infile:
    directions = infile.readline().strip().split(", ")
# n=0, w=1, s=2, e=3
offsets = {0: (0, 1), 1: (-1, 0), 2: (0, -1), 3: (1, 0)}
heading = 0
x, y = 0, 0
locations: set[Tuple[int, int]] = set([(0, 0)])
part2 = None
for direction in directions:
    turn = direction[:1]
    if turn == "L":
        heading = (heading + 1) % 4
    else:
        heading = (heading - 1) % 4
    distance = int(direction[1:])
    for step in range(distance):
        x += offsets[heading][0]
        y += offsets[heading][1]
        if part2 is None:
            if (x, y) in locations:
                part2 = abs(x) + abs(y)
            else:
                locations.add((x, y))
print(f"Part 1: {abs(x) + abs(y)}")
print(f"Part 2: {part2}")
