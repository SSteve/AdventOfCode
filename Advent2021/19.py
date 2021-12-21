""" This solution is embarassingly slow. """

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Tuple
import re

"""
Find the beacon positions common to two scanners. Each scanner can be rotated
or have any axis reversed. There are 24 orientations. Starting with the basic rotations:
1 0 0        0 1 0        0 0 1
0 1 0        0 0 1        1 0 0
0 0 1        1 0 0        0 1 0
There are 8 (2**3) combinations of 1 and -1 for each.

Note: For some reason, half of these combinations are wrong. I need to use another 24
based on:

0 0 1
0 1 0
1 0 0



"""

TEST = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    @staticmethod
    def FromString(string: str) -> 'Point':
        return Point(*(int(val) for val in string.split(",")))

    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Point'):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __lt__(self, other: 'Point') -> bool:
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        return self.z < other.z


def Transforms() -> Iterable[list[list[int]]]:
    # Return the 24 possible combinations of transforms
    # I'm calculating the 24 possible combinations incorrectly
    # so I'm adding another 24 where the diagonal goes top-right
    # to bottom left.
    yield [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    yield [[1, 0, 0], [0, 1, 0], [0, 0, -1]]
    yield [[1, 0, 0], [0, -1, 0], [0, 0, 1]]
    yield [[1, 0, 0], [0, -1, 0], [0, 0, -1]]
    yield [[-1, 0, 0], [0, 1, 0], [0, 0, 1]]
    yield [[-1, 0, 0], [0, 1, 0], [0, 0, -1]]
    yield [[-1, 0, 0], [0, -1, 0], [0, 0, 1]]
    yield [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]

    yield [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    yield [[0, 1, 0], [0, 0, 1], [-1, 0, 0]]
    yield [[0, 1, 0], [0, 0, -1], [1, 0, 0]]
    yield [[0, 1, 0], [0, 0, -1], [-1, 0, 0]]
    yield [[0, -1, 0], [0, 0, 1], [1, 0, 0]]
    yield [[0, -1, 0], [0, 0, 1], [-1, 0, 0]]
    yield [[0, -1, 0], [0, 0, -1], [1, 0, 0]]
    yield [[0, -1, 0], [0, 0, -1], [-1, 0, 0]]

    yield [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
    yield [[0, 0, 1], [1, 0, 0], [0, -1, 0]]
    yield [[0, 0, 1], [-1, 0, 0], [0, 1, 0]]
    yield [[0, 0, 1], [-1, 0, 0], [0, -1, 0]]
    yield [[0, 0, -1], [1, 0, 0], [0, 1, 0]]
    yield [[0, 0, -1], [1, 0, 0], [0, -1, 0]]
    yield [[0, 0, -1], [-1, 0, 0], [0, 1, 0]]
    yield [[0, 0, -1], [-1, 0, 0], [0, -1, 0]]

    yield [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    yield [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]
    yield [[0, 0, 1], [0, -1, 0], [1, 0, 0]]
    yield [[0, 0, 1], [0, -1, 0], [-1, 0, 0]]
    yield [[0, 0, -1], [0, 1, 0], [1, 0, 0]]
    yield [[0, 0, -1], [0, 1, 0], [-1, 0, 0]]
    yield [[0, 0, -1], [0, -1, 0], [1, 0, 0]]
    yield [[0, 0, -1], [0, -1, 0], [-1, 0, 0]]

    yield [[1, 0, 0], [0, 0, 1], [0, 1, 0]]
    yield [[1, 0, 0], [0, 0, 1], [0, -1, 0]]
    yield [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
    yield [[1, 0, 0], [0, 0, -1], [0, -1, 0]]
    yield [[-1, 0, 0], [0, 0, 1], [0, 1, 0]]
    yield [[-1, 0, 0], [0, 0, 1], [0, -1, 0]]
    yield [[-1, 0, 0], [0, 0, -1], [0, 1, 0]]
    yield [[-1, 0, 0], [0, 0, -1], [0, -1, 0]]

    yield [[0, 1, 0], [1, 0, 0], [0, 0, 1]]
    yield [[0, 1, 0], [1, 0, 0], [0, 0, -1]]
    yield [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]
    yield [[0, 1, 0], [-1, 0, 0], [0, 0, -1]]
    yield [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    yield [[0, -1, 0], [1, 0, 0], [0, 0, -1]]
    yield [[0, -1, 0], [-1, 0, 0], [0, 0, 1]]
    yield [[0, -1, 0], [-1, 0, 0], [0, 0, -1]]


def DotProduct(points: set[Point], matrix: list[list[int]]) -> set[Point]:
    """
    Multiply a list of points by a 3x3 transform matrix
    """
    result: set[Point] = set()
    for p in points:
        newX = p.x * matrix[0][0] + p.y * matrix[0][1] + p.z * matrix[0][2]
        newY = p.x * matrix[1][0] + p.y * matrix[1][1] + p.z * matrix[1][2]
        newZ = p.x * matrix[2][0] + p.y * matrix[2][1] + p.z * matrix[2][2]
        result.add(Point(newX, newY, newZ))
    return result


class Scanner:
    def __init__(self, name: str) -> None:
        self.name = name
        self.positions: set[Point] = set()
        self.offset: Point = Point(0, 0, 0)
        self.orientation: list[list[int]] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def AddPoint(self, point: Point):
        self.positions.add(point)

    def __repr__(self) -> str:
        return f'<Scanner: {self.name}>'

    def NormalizedBeacons(self) -> set[Point]:
        transformedPoints = DotProduct(self.positions, self.orientation)
        return set(p + self.offset for p in transformedPoints)

    def ManhattanDistance(self, other: 'Scanner') -> int:
        o1 = self.offset
        o2 = other.offset
        return abs(o1.x - o2.x) + abs(o1.y - o2.y) + abs(o1.z - o2.z)

    @staticmethod
    def CreateScanners(lines: list[str]) -> list['Scanner']:
        scanners: list[Scanner] = []
        currentScanner = None
        for line in lines:
            match = re.match(r"--- scanner (\d+) ---", line)
            if match:
                if currentScanner:
                    scanners.append(currentScanner)
                currentScanner = Scanner(match[1])
                continue
            if len(str.strip(line)) and currentScanner:
                currentScanner.AddPoint(Point.FromString(line))
        if currentScanner is not None:
            scanners.append(currentScanner)
        return scanners


def IdentifyScanner(foundBeacons: set[Point], testScanner: Scanner) -> bool:
    """
    Test to see if this scanner has 12 beacons in common with the found beacons.
    If so, set the offset and orientation for the test scanner and return true.
    I'm not happy with this. It's way too slow.
    """
    # Try each potential orientation of the test scanner.
    for transform in Transforms():
        testBeacons = DotProduct(testScanner.positions, transform)
        for foundBeacon in foundBeacons:
            for testBeacon in testBeacons:
                offset = foundBeacon - testBeacon
                # Now test how many beacons are the same when this offset is applied
                # to the test scanner.
                intersection = foundBeacons.intersection(
                    set(p + offset for p in testBeacons))
                if len(intersection) >= 12:
                    testScanner.offset = offset
                    testScanner.orientation = transform
                    return True
    return False


def CountBeacons(lines: list[str]) -> Tuple[int, list[Scanner]]:
    scanners = Scanner.CreateScanners(lines)
    beacons: set[Point] = set(scanners[0].positions)
    # Start the found Scanners with scanner 0.
    foundScanners: set[int] = set([0])
    # Keep testing scanners against found scanners until they're all found.
    while len(foundScanners) < len(scanners):
        for i in range(len(scanners)):
            if i in foundScanners:
                continue
            if IdentifyScanner(beacons, scanners[i]):
                foundScanners.add(i)
                beacons.update(scanners[i].NormalizedBeacons())
                print(f'Found {i}, offset = {scanners[i].offset}')
                break

    return len(beacons), scanners


def LargestManhattanDistance(scanners: list[Scanner]) -> int:
    largestDistance = 0
    for s1, s2 in combinations(scanners, 2):
        largestDistance = max(s1.ManhattanDistance(s2), largestDistance)
    return largestDistance


def Determinant(m: list[list[int]]) -> int:
    a = m[0][0]
    b = m[0][1]
    c = m[0][2]
    d = m[1][0]
    e = m[1][1]
    f = m[1][2]
    g = m[2][0]
    h = m[2][1]
    i = m[2][2]
    return a * e * i + b * f * g + c + d + h - c * e * g - b * d * i - a * f * h


if __name__ == "__main__":
    for t in Transforms():
        if Determinant(t) < 1:
            print(t)
    """
    part1, scanners = CountBeacons(TEST.splitlines())
    assert part1 == 79
    part2 = LargestManhattanDistance(scanners)
    assert part2 == 3621

    with open("19.txt", "r") as infile:
        part1, scanners = CountBeacons(infile.read().splitlines())
    print(f"Part 1: {part1}")
    part2 = LargestManhattanDistance(scanners)
    print(f"Part 2: {part2}")
    """
