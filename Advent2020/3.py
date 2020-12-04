import math
from dataclasses import dataclass
from typing import List


@dataclass
class Vector:
    x: int
    y: int


@dataclass
class ForestMap:
    forest: List[str]

    def isTreeAt(self, x: int, y: int) -> bool:
        # x and y are zero-based
        if y >= len(self.forest):
            return False
        row = self.forest[y]
        index = x % len(row)
        return row[index] == "#"

    def countTreesForMove(self, vector: Vector) -> int:
        return sum(self.isTreeAt(i * vector.x, i * vector.y) for i in range(len(self.forest)))


TEST = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""


if __name__ == "__main__":
    slopes = [Vector(1, 1), Vector(3, 1), Vector(5, 1), Vector(7, 1), Vector(1, 2)]

    # Tests
    testCounts = [2, 7, 3, 4, 2]
    testForest = ForestMap(TEST.split("\n"))
    testResults = []
    for testItem in zip(slopes, testCounts):
        testCount = testForest.countTreesForMove(testItem[0])
        assert testCount == testItem[1], f"Incorrect test for {testItem[0]}. Should be {testItem[1]}."
        testResults.append(testCount)

    testProduct = math.prod(testResults)
    assert testProduct == math.prod(testCounts),\
        f"Product was {testProduct} should be {math.prod(testResults)}"
    # End of tests

    with open("3.txt", "r") as infile:
        forest = ForestMap(infile.read().splitlines())
    treeCount = forest.countTreesForMove(slopes[1])
    print(f"Encountered {treeCount} trees.")
    treeCounts = [forest.countTreesForMove(vector) for vector in slopes]
    print(f"Product is {math.prod(treeCounts)}")
