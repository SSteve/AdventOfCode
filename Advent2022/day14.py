from dataclasses import dataclass

TEST = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
# Return -1, 0, 1 if x < 0, x == 0, x > 0
def sign(x): return x and (-1 if x < 0 else 1)


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, path_point: str):
        x_str, y_str = path_point.split(",", 1)
        return Point(int(x_str), int(y_str))


class Cavern:
    def __init__(self, input: list[str]) -> None:
        self.locations: dict[Point, str] = {}
        self.left: int = 100000000000
        self.right: int = -1
        self.top: int = 0
        self.bottom: int = -1

        for line in input:
            previous = None
            for path_point in line.split(" -> "):
                this_point = Point.from_str(path_point)
                if previous is not None:
                    delta_x = sign(this_point.x - previous.x)
                    delta_y = sign(this_point.y - previous.y)
                    current_point = previous
                    while current_point != this_point:
                        self.locations[current_point] = "#"
                        current_point = Point(
                            current_point.x + delta_x, current_point.y + delta_y)
                    self.locations[current_point] = "#"
                previous = this_point

                self.left = min(self.left, this_point.x)
                self.right = max(self.right, this_point.x)
                self.top = min(self.top, this_point.y)
                self.bottom = max(self.bottom, this_point.y)

    def __str__(self) -> str:
        this_str = ""
        for y in range(self.top, self.bottom+3):
            for x in range(self.left, self.right + 1):
                this_point = Point(x, y)
                if this_point in self.locations:
                    this_str += self.locations[this_point]
                else:
                    this_str += "."
            this_str += "\n"
        return this_str

    def fill_with_sand(self, from_point: Point) -> int:
        sand_location = from_point
        sand_count = 0
        while self.left <= sand_location.x <= self.right and sand_location.y < self.bottom:
            below = Point(sand_location.x, sand_location.y + 1)
            if below not in self.locations:
                sand_location = below
                continue
            below_left = Point(sand_location.x-1, sand_location.y+1)
            if below_left not in self.locations:
                sand_location = below_left
                continue
            below_right = Point(sand_location.x+1, sand_location.y+1)
            if below_right not in self.locations:
                sand_location = below_right
                continue

            self.locations[sand_location] = "o"
            sand_count += 1
            sand_location = from_point
        return sand_count

    def fill_with_sand_with_floor(self, from_point: Point) -> int:
        sand_location = from_point
        sand_count = 0
        while from_point not in self.locations:
            below = Point(sand_location.x, sand_location.y + 1)
            if below.y < self.bottom + 2 and below not in self.locations:
                sand_location = below
                continue
            below_left = Point(sand_location.x-1, sand_location.y+1)
            if below.y < self.bottom + 2 and below_left not in self.locations:
                sand_location = below_left
                continue
            below_right = Point(sand_location.x+1, sand_location.y+1)
            if below.y < self.bottom + 2 and below_right not in self.locations:
                sand_location = below_right
                continue

            self.locations[sand_location] = "o"
            self.left = min(self.left, sand_location.x)
            self.right = max(self.right, sand_location.x)
            sand_count += 1
            sand_location = from_point
        return sand_count


if __name__ == "__main__":
    cavern = Cavern(TEST.splitlines())
    part1test = cavern.fill_with_sand(Point(500, 0))
    print(f"Part 1 test: {part1test}")
    assert (part1test == 24)

    cavern = Cavern(TEST.splitlines())
    part2test = cavern.fill_with_sand_with_floor(Point(500, 0))
    print(f"Part 2 test: {part2test}")
    assert (part2test == 93)

    with open("day14.txt") as infile:
        cavern = Cavern(infile.read().splitlines())

    part1 = cavern.fill_with_sand(Point(500, 0))
    print(f"Part 1: {part1}")

    with open("day14.txt") as infile:
        cavern = Cavern(infile.read().splitlines())

    part2 = cavern.fill_with_sand_with_floor(Point(500, 0))
    print(f"Part 2: {part2}")
