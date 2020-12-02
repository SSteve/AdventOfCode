from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Artifact:
    name: str
    location: Point

    def at_location(self, location: Point) -> bool:
        return self.location == location

    def __eq__(self, o: 'Artifact') -> bool:
        return self.name == o.name


class Tunnels:
    def __init__(self, tunnel_map: Iterable[str]):
        self.locations: Sequence[Point] = []
        self.keys: Sequence[Artifact] = []
        self.doors: Sequence[Artifact] = []
        self.current_location: Point
        self.height = 0
        self.width = 0
        for y, row in enumerate(tunnel_map):
            row = row.strip()
            if len(row) > 0:
                self.height += 1
                self.width = len(row)
                for x, map_char in enumerate(row):
                    if map_char == "#":
                        continue
                    self.locations.append(Point(x, y))
                    if map_char == "@":
                        self.current_location = Point(x, y)
                        continue
                    if map_char == ".":
                        continue
                    # Now we know this cell contains a key or a door.
                    if map_char == map_char.lower:
                        # It's a key.
                        self.keys.append(Artifact(map_char, Point(x, y)))
                    else:
                        self.doors.append(Artifact(map_char.lower, Point(x, y)))

    def __repr__(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                location = Point(x, y)
                if location == self.current_location:
                    print("@", end="")
                    continue
                if location in self.locations:
                    if location in 



TEST1="""#########
#b.A.@.a#
#########"""


