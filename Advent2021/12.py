from collections import defaultdict
from typing import Iterable, Union

TEST1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

TEST2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

TEST3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


def CreateMap(lines: list[str]) -> dict[str, set[str]]:
    map: dict[str, set[str]] = defaultdict(set)
    for line in lines:
        cave1, cave2 = line.split("-")
        if cave1 == cave2:
            raise ValueError("A cave can't lead to itself.")
        map[cave1].add(cave2)
        map[cave2].add(cave1)
    return map


def CanVisit1(cave: str, visited: list[str]) -> bool:
    return cave.isupper() or cave not in visited


def CanVisit2(cave: str, visited: list[str]) -> bool:
    # We can never visit start twice
    if cave == "start":
        return False
    # We can always revisit a large cave
    if cave.isupper():
        return True
    # If we haven't visited this small cave yet, we can visit it.
    if cave not in visited:
        return True
    # If we've visited this cave once, we can visit it again on the condition
    # that no other small cave has been visited twice.
    if sum(c == cave for c in visited) == 1:
        canVisit = True
        for c2 in visited:
            if c2.islower() and sum(c2 == c3 for c3 in visited) == 2:
                canVisit = False
                break
        return canVisit
    # We've exhausted all the scenerios where we can visit a cave@app.
    return False


def FindPath(map: dict[str, set[str]], visited: list[str], visit_function) -> Iterable[Union[list[str], None]]:
    for cave in map[visited[-1]]:
        newList = visited[:]
        if cave == "end":
            newList.append("end")
            yield newList
        elif visit_function(cave, newList):
            newList.append(cave)
            for path in FindPath(map, newList, visit_function):
                yield path
        else:
            yield None


def FindPaths(map: dict[str, set[str]], visit_function) -> set[str]:
    paths: set[str] = set()
    for cave in map["start"]:
        for path in FindPath(map, ["start", cave], visit_function):
            if path:
                paths.add(",".join(path))
    return paths


if __name__ == "__main__":
    map = CreateMap(TEST1.splitlines())
    paths = FindPaths(map, CanVisit1)
    assert len(paths) == 10
    paths = FindPaths(map, CanVisit2)
    assert len(paths) == 36

    map = CreateMap(TEST2.splitlines())
    paths = FindPaths(map, CanVisit1)
    assert len(paths) == 19
    paths = FindPaths(map, CanVisit2)
    assert len(paths) == 103

    map = CreateMap(TEST3.splitlines())
    paths = FindPaths(map, CanVisit1)
    assert len(paths) == 226
    paths = FindPaths(map, CanVisit2)
    assert len(paths) == 3509

    with open("12.txt", "r") as infile:
        map = CreateMap(infile.read().splitlines())
    paths = FindPaths(map, CanVisit1)
    part1 = len(paths)
    print(f"Part 1: {part1}")
    paths = FindPaths(map, CanVisit2)
    part2 = len(paths)
    print(f"Part 2: {part2}")
