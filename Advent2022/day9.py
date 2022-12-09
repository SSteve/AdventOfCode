from dataclasses import dataclass
from enum import StrEnum

TEST = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

TEST2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


class Direction(StrEnum):
    LEFT = 'L'
    UP = 'U'
    RIGHT = 'R'
    DOWN = 'D'


@dataclass(frozen=True)
class Motion:
    direction: Direction
    steps: int

    @classmethod
    def from_string(cls, s: str) -> "Motion":
        (direction, num) = s.split(" ", 1)
        return cls(Direction(direction), int(num))


# Return -1, 0, 1 if x < 0, x == 0, x > 0
def sign(x): return x and (-1 if x < 0 else 1)


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def in_direction(self, direction: Direction) -> "Point":
        x = self.x
        y = self.y
        match direction:
            case Direction.LEFT:
                x -= 1
            case Direction.UP:
                y += 1
            case Direction.RIGHT:
                x += 1
            case Direction.DOWN:
                y -= 1
        return Point(x, y)

    def after_following_head(self, head: "Point") -> "Point":
        delta_x = head.x - self.x
        delta_y = head.y - self.y
        if abs(delta_x > 2) or abs(delta_y > 2):
            raise ValueError(
                f"Unexpected positioning. Δx = {delta_x}, Δy = {delta_y}.")
        if delta_x == 0 and delta_y == 0 \
                or delta_x == 0 and abs(delta_y) == 1 \
                or delta_y == 0 and abs(delta_x) == 1 \
                or abs(delta_x) == 1 and abs(delta_y) == 1:
            return self
        return Point(self.x + sign(delta_x), self.y + sign(delta_y))


def create_motions(lines: list[str]) -> list[Motion]:
    motions: list[Motion] = []
    for line in lines:
        motion = Motion.from_string(line)
        motions.append(motion)

    return motions


def count_tail_locations(motions: list[Motion]) -> int:
    head = Point(0, 0)
    tail = Point(0, 0)
    tail_locations: set[Point] = {tail}

    for motion in motions:
        for _ in range(motion.steps):
            head = head.in_direction(motion.direction)
            tail = tail.after_following_head(head)
            tail_locations.add(tail)

    return len(tail_locations)


def count_rope_end_locations(motions: list[Motion]) -> int:
    rope = [Point(0, 0), Point(0, 0), Point(0, 0),
            Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)]
    end_locations: set[Point] = {rope[9]}
    for motion in motions:
        for _ in range(motion.steps):
            rope[0] = rope[0].in_direction(motion.direction)
            for i in range(1, 10):
                rope[i] = rope[i].after_following_head(rope[i-1])
            end_locations.add(rope[9])

    return len(end_locations)


if __name__ == "__main__":
    motions = create_motions(TEST.splitlines())
    part1test = count_tail_locations(motions)
    print(f"Part 1 test: {part1test}")
    assert (part1test == 13)
    part2test = count_rope_end_locations(motions)
    print(f"Part 2 test 1: {part2test}")
    assert (part2test == 1)
    motions = create_motions(TEST2.splitlines())
    part2test = count_rope_end_locations(motions)
    print(f"Part 2 test 2: {part2test}")
    assert (part2test == 36)

    with open("day9.txt") as infile:
        motions = create_motions(infile.read().splitlines())

    part1 = count_tail_locations(motions)
    print(f"Part 1: {part1}")

    part2 = count_rope_end_locations(motions)
    print(f"Part 2: {part2}")
