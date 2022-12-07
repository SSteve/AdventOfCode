from dataclasses import dataclass
from typing import Generator

TEST = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


@dataclass(frozen=True)
class FileNode:
    name: str
    size: int


class DirectoryNode:
    name: str
    files: list[FileNode]
    children: dict[str, "DirectoryNode"]

    def __init__(self, name) -> None:
        self.name = name
        self.files = []
        self.children = {}

    def total_size(self) -> int:
        size = sum(file.size for file in self.files)
        size += sum(directory.total_size()
                    for directory in self.children.values())
        return size

    def sub_directories(self) -> Generator["DirectoryNode", None, None]:
        # This is the stack that holds all of the descendents that will be
        # returned to the caller.
        iter_stack: list[DirectoryNode] = []
        # This is the stack of directories yet to process.
        process_stack: list[DirectoryNode] = []
        # We need to process all of the children of this directory.
        for child in self.children.values():
            process_stack.append(child)

        # This is the iterative process of creating the stack of descendents to return.
        while len(process_stack) > 0:
            node = process_stack.pop()
            iter_stack.append(node)
            for child in node.children.values():
                process_stack.append(child)

        # Now we return the descendents in the iter_stack.
        while len(iter_stack):
            yield iter_stack.pop()

    def __repr__(self) -> str:
        return f"Name: {self.name}, {len(self.children)} children, {len(self.files)} files"


def parse_input(terminal_output: list[str]) -> DirectoryNode:
    directory_stack: list[DirectoryNode] = []
    current_directory: DirectoryNode = DirectoryNode("/")
    for line in terminal_output:
        words = line.split(" ")
        # We ignore  "$ ls" in the terminal output because
        # it doesn't change state.
        if words[0] == "$" and words[1] == "cd" and words[2] == "..":
            # Move back up one folder.
            current_directory = directory_stack.pop()
        elif words[0] == "$" and words[1] == "cd":
            if words[2] == "/":
                # We start out in the root directory so no action is needed.
                continue
            # Move into a child directory.
            assert (words[2] in current_directory.children)
            directory_stack.append(current_directory)
            current_directory = current_directory.children[words[2]]
        elif words[0] == "dir":
            current_directory.children[words[1]] = DirectoryNode(words[1])
        elif words[0].isdecimal():
            current_directory.files.append(FileNode(words[1], int(words[0])))

    while len(directory_stack) > 0:
        current_directory = directory_stack.pop()

    return current_directory


def sum_sizes_of_directories(root_directory: DirectoryNode, max_size: int) -> int:
    sum_of_sizes = 0

    directory_size = root_directory.total_size()
    if directory_size <= max_size:
        sum_of_sizes += directory_size

    for directory in root_directory.children.values():
        sum_of_sizes += sum_sizes_of_directories(directory, max_size)

    return sum_of_sizes


def find_smallest_to_delete(root_directory: DirectoryNode, disc_space: int, space_required: int) -> int:
    total_space_used = root_directory.total_size()
    space_available = disc_space - total_space_used
    additional_space_required = space_required - space_available
    smallest_space = total_space_used
    for directory in root_directory.sub_directories():
        directory_size = directory.total_size()
        if directory_size >= additional_space_required and directory_size < smallest_space:
            smallest_space = directory_size
    return smallest_space


if __name__ == "__main__":
    file_structure = parse_input(TEST.splitlines())

    part1test = sum_sizes_of_directories(file_structure, 100000)
    print(f"Part 1 test: {part1test}")
    assert (part1test == 95437)

    part2test = find_smallest_to_delete(file_structure, 70000000, 30000000)
    print(f"Part 2 test: {part2test}")
    assert (part2test == 24933642)

    with open("day7.txt") as infile:
        file_structure = parse_input(infile.read().splitlines())

    part1 = sum_sizes_of_directories(file_structure, 100000)
    print(f"Part 1: {part1}")

    part2 = find_smallest_to_delete(file_structure, 70000000, 30000000)
    print(f"Part 2: {part2}")
    assert (part2 < 41609574)  # My first incorrect answer
