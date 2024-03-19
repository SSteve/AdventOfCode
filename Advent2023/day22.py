from collections import defaultdict, deque
from dataclasses import dataclass
from functools import cache
from typing import Self

TEST = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

"""
This is one of those where the brute force method is n-squared at best or n! at worst. I didn't jump in and start coding
right away. I left it and let my brain work on it in the background. I eventually decided to try representing the bricks
by Z range since testing for which bricks are on which others will be done based on their Z position. I'm not optimizing
them per layer in the first attempt. Hopefully optimizing by Z will be enough. Worked on second run. In the first run I
forgot to allow for bricks on the ground that were not supporting any bricks. It is plenty fast.

My first attempt at part 2 didn't work. It didn't allow for vertical bricks. My second attempt worked the first time. 
"""


@dataclass(frozen=True)
class Brick:
    x_min: int
    y_min: int
    z_min: int
    x_max: int
    y_max: int
    z_max: int

    @classmethod
    def from_line(cls, line: str):
        start, end = line.split("~")
        x_start, y_start, z_start = map(int, start.split(","))
        x_end, y_end, z_end = map(int, end.split(","))
        return cls(
            min(x_start, x_end),
            min(y_start, y_end),
            min(z_start, z_end),
            max(x_start, x_end),
            max(y_start, y_end),
            max(z_start, z_end),
        )

    def with_z_min(self, new_z_min: int) -> Self:
        # Return this brick with the new z_min value.
        return Brick(self.x_min, self.y_min, new_z_min, self.x_max, self.y_max, new_z_min + self.z_max - self.z_min)

    def is_vertical(self) -> bool:
        return self.z_min != self.z_max

    def x_intersects(self, other: Self) -> bool:
        return other.x_min <= self.x_max and other.x_max >= self.x_min

    def y_intersects(self, other: Self) -> bool:
        return other.y_min <= self.y_max and other.y_max >= self.y_min

    def is_on(self, other: Self) -> bool:
        # Return True if this brick is resting on the other brick.
        return self.x_intersects(other) and self.y_intersects(other) and self.z_min == other.z_max + 1


@dataclass
class Relatives:
    parents: set[Brick]
    children: set[Brick]


def relatives_factory():
    return Relatives(set(), set())


class BrickMap:
    bricks: dict[int, set[Brick]]
    graph: dict[Brick, Relatives]

    def __init__(self, lines: list[str]):
        """
        Take the representation of the bricks in mid-air and drop them all to their
        lowest possible position.
        """
        self.bricks = defaultdict(set)

        falling_bricks = set(Brick.from_line(line) for line in lines)
        self.bricks[1] = set(filter(lambda b: b.z_min == 1, falling_bricks))
        falling_bricks -= self.bricks[1]

        # Put the bricks already on the ground into the final representation.
        for brick in self.bricks[1]:
            if brick.z_max > 1:
                self.bricks[brick.z_max].add(brick)

        # Sort the bricks still in the air by their lower Z value.
        bricks_to_process = deque(sorted(falling_bricks, key=lambda brick: brick.z_min))

        # Settle all the bricks onto the brick they will rest on.
        while bricks_to_process:
            brick = bricks_to_process.popleft()
            for layer in range(brick.z_min, 0, -1):
                if layer == 1 or (
                    layer - 1 in self.bricks
                    and any(brick.x_intersects(b) and brick.y_intersects(b) for b in self.bricks[layer - 1])
                ):
                    new_brick = brick.with_z_min(layer)
                    for new_layer in range(new_brick.z_min, new_brick.z_max + 1):
                        self.bricks[new_layer].add(new_brick)
                    break

            self.graph: dict[Brick, Relatives] = defaultdict(relatives_factory)

        # Create the graph of bricks and their parents and children.
        for layer in sorted(self.bricks.keys()):
            for brick in self.bricks[layer]:
                if brick not in self.graph:
                    self.graph[brick] = Relatives(set(), set())
                # Look for parents.
                layer_above = brick.z_max + 1
                if layer_above in self.bricks:
                    for brick_above in self.bricks[layer_above]:
                        if brick_above.is_on(brick):
                            self.graph[brick].parents.add(brick_above)
                            self.graph[brick_above].children.add(brick)

    @cache
    def get_all_ancestors(self, brick: Brick) -> set[Brick]:
        ancestors: set[Brick] = set()

        for parent in self.graph[brick].parents:
            ancestors.add(parent)
            ancestors |= self.get_all_ancestors(parent)

        return ancestors

    def count_chain_reaction(self, bricks_to_disintegrate: set[Brick]) -> int:
        combined_ancestors: set[Brick] = set()

        for brick in bricks_to_disintegrate:
            combined_ancestors |= self.get_all_ancestors(brick)

        bricks_to_remove: set[Brick] = set()
        for brick in combined_ancestors:
            if brick not in bricks_to_remove and any(
                child not in bricks_to_disintegrate and child not in combined_ancestors for child in self.graph[brick].children
            ):
                # For any brick that has a child that isn't one of the bricks we're disintegrating or any of their ancestors, remove that brick
                # and all its ancestors because it will be holding them all up.
                bricks_to_remove.add(brick)
                bricks_to_remove |= self.get_all_ancestors(brick)

        return len(combined_ancestors - bricks_to_remove)

    def count_chain_reactions(self) -> int:
        chain_reactions = 0

        for brick in self.graph:
            brick_to_collapse = set([brick])
            chain_reactions += self.count_chain_reaction(brick_to_collapse)

        return chain_reactions


def count_bricks(lines: list[str]) -> int:
    brick_map = BrickMap(lines)
    assert len(brick_map.graph.keys()) == len(lines)

    brick_count = 0

    for relatives in brick_map.graph.values():
        if len(relatives.parents) == 0 or all(len(brick_map.graph[parent].children) > 1 for parent in relatives.parents):
            brick_count += 1

    return brick_count


def count_chain_reactions(lines: list[str]) -> int:
    brick_map = BrickMap(lines)
    return brick_map.count_chain_reactions()


if __name__ == "__main__":
    part1test = count_bricks(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 5

    part2test = count_chain_reactions(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 7

    with open("day22.txt") as infile:
        lines = infile.read().splitlines()

    part1 = count_bricks(lines)
    print(f"Part 1: {part1}")
    assert part1 == 524

    part2 = count_chain_reactions(lines)
    print(f"Part 2: {part2}")
    assert part2 == 77070
