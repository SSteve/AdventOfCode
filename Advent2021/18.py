from collections import deque
from itertools import permutations
from typing import Iterable, Optional


class Node:
    def __init__(self, parent):
        self.parent: 'Node' = parent

    def Magnitude(self) -> int:
        raise TypeError("Node abstract type does not implement Magnitude().")

    def Depth(self) -> int:
        raise TypeError("Node abstract type does not implement Depth().")

    def Split(self) -> bool:
        raise TypeError("Node abstract type does not implement Split().")

    def SplitValue(self) -> Optional['Node']:
        raise TypeError("Node abstract type does not implement SplitValue().")

    def DotRepresentation(self) -> Iterable[str]:
        raise TypeError(
            "Node abstract type does not implement DotRepresentation().")

    def WriteToDotFile(self, filename: str) -> None:
        """
        Return a Graphviz representation to the given file.
        The dot file can be converted to PDF with the command:
        dot -Tpdf -O 18.dot
        """
        with open(filename, "w") as dotFile:
            print("digraph snailfish_numbers {", file=dotFile)
            for line in self.DotRepresentation():
                print(line, file=dotFile)
            print("}", file=dotFile)


class Pair(Node):
    def __init__(self, parent):
        super().__init__(parent)
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __repr__(self):
        return f'[{self.left},{self.right}]'

    def __add__(self, other: 'Pair'):
        node = Pair(None)
        node.left = self
        node.right = other
        self.parent = node
        other.parent = node
        node.Reduce()
        return node

    @classmethod
    def CreateTree(cls, string: str) -> 'Pair':
        return Pair.FromString(None, deque(string[1:]))

    @classmethod
    def FromString(cls, parent: Optional[Node], string: deque[str]) -> 'Pair':
        node = Pair(parent)

        char = string.popleft()
        if char.isdigit():
            node.left = Value(node, int(char))
        elif char == '[':
            node.left = Pair.FromString(node, string)
        else:
            raise ValueError(
                f'First position expected "[" or a digit, got {char}.')

        char = string.popleft()
        if char != ',':
            raise ValueError(f'Expected ",", got {char}.')

        char = string.popleft()
        if char.isdigit():
            node.right = Value(node, int(char))
        elif char == '[':
            node.right = Pair.FromString(node, string)
        else:
            raise ValueError(
                f'Second position expected "[" or a digit, got {char}.')

        char = string.popleft()
        if char != ']':
            raise ValueError(f'Expected "]", got {char}.')
        return node

    def Reduce(self) -> None:
        while self.Explode() or self.Split():
            pass

    def Magnitude(self) -> int:
        if self.left is None or self.right is None:
            raise ValueError("Both child nodes must be defined")
        return 3 * self.left.Magnitude() + 2 * self.right.Magnitude()

    def Depth(self) -> int:
        if self.parent is None:
            return 0
        return self.parent.Depth() + 1

    def Split(self) -> bool:
        """
        Perform a SplitValue on the first value in the tree that requires
        splitting. Once a value in the tree is split, stop. Return True
        if a split was performed.
        """
        if type(self.left) is Value:
            newNode = self.left.SplitValue()
            if newNode:
                self.left = newNode
                return True
        elif type(self.left) is Pair:
            leftWasSplit = self.left.Split()
            if leftWasSplit:
                return True
        else:
            raise ValueError("Node's left tree should not be None.")

        if type(self.right) is Value:
            newNode = self.right.SplitValue()
            if newNode:
                self.right = newNode
                return True
            else:
                return False
        elif type(self.right) is Pair:
            return self.right.Split()
        else:
            raise ValueError("Node's right tree should not be None.")

    def FirstValueToLeft(self) -> Optional['Value']:
        """
        Find the first regular number to the left of this pair.
        """
        # First find the nearest ancestor that has a child to the left
        # of this one
        parent: Pair = self.parent  # type: ignore
        child = self
        while parent is not None and child == parent.left:
            child = parent
            parent: Pair = parent.parent  # type: ignore
        # If we made it past the top of the tree, there is nothing to
        # the left of this pair.
        if parent is None:
            return None
        # Now search the left branch of this Pair and find the
        # right-most value.
        child = parent.left
        while type(child) is Pair:
            child = child.right
        # The leaf node must always be a Value.
        if type(child) is Value:
            return child
        raise ValueError("Child wasn't Value.")

    def FirstValueToRight(self) -> Optional['Value']:
        """
        Find the first regular number to the right of this pair.
        """
        # First find the nearest ancestor that has a child to the right
        # of this one
        parent: Pair = self.parent  # type: ignore
        child = self
        while parent is not None and child == parent.right:
            child = parent
            parent: Pair = parent.parent  # type: ignore
        # If we made it past the top of the tree, there is nothing to
        # the right of this pair.
        if parent is None:
            return None
        # Now search the right branch of this Pair and find the
        # left-most value.
        child = parent.right
        while type(child) is Pair:
            child = child.left
        if type(child) is Value:
            return child
        raise ValueError("Child wasn't Value.")

    def ExplodePair(self) -> None:
        leftChild = self.left
        if type(leftChild) is not Value:
            raise ValueError("Left child must be Value.")
        rightChild = self.right
        if type(rightChild) is not Value:
            raise ValueError("Right child must be Value.")
        valueToLeft = self.FirstValueToLeft()
        if valueToLeft:
            valueToLeft.value += leftChild.value
        valueToRight = self.FirstValueToRight()
        if valueToRight:
            valueToRight.value += rightChild.value
        newValue = Value(self.parent, 0)
        if self.parent.left == self:  # type: ignore
            self.parent.left = newValue  # type: ignore
        elif self.parent.right == self:  # type: ignore
            self.parent.right = newValue  # type: ignore
        else:
            raise ValueError("Parent doesn't contain this Pair.")

    def FindPairToExplode(self) -> Optional['Pair']:
        if self.Depth() == 4:
            return self
        if type(self.left) is Pair:
            explodee = self.left.FindPairToExplode()
            if explodee:
                return explodee
        if type(self.right) is Pair:
            return self.right.FindPairToExplode()
        return None

    def Explode(self) -> bool:
        """
        Explode the first Pair that is nested four levels deep. Return True if
        a pair was exploded.
        """
        pairToExplode = self.FindPairToExplode()
        if type(pairToExplode) is Pair:
            pairToExplode.ExplodePair()
            return True
        return False

    def DotRepresentation(self) -> Iterable[str]:
        yield f'    x{id(self)} [label="depth={self.Depth()}", shape=box]'
        if self.left is not None:
            for line in self.left.DotRepresentation():
                yield line
            yield f'    x{id(self)} -> x{id(self.left)}'
        if self.right is not None:
            for line in self.right.DotRepresentation():
                yield line
            yield f'    x{id(self)} -> x{id(self.right)}'


class Value(Node):
    def __init__(self, parent, value):
        super().__init__(parent)
        self.value = value

    def __repr__(self):
        return str(self.value)

    def Magnitude(self):
        return self.value

    def SplitValue(self) -> Optional[Node]:
        if self.value < 10:
            return None
        node = Pair(self.parent)
        leftValue = self.value // 2
        node.left = Value(node, leftValue)
        node.right = Value(node, self.value - leftValue)
        return node

    def DotRepresentation(self) -> Iterable[str]:
        yield f'    x{id(self)} [label="{str(self.value)}" shape=circle]'


def ExplodeTests():
    a = Pair.CreateTree("[[[[[9,8],1],2],3],4]")
    # a.WriteToDotFile("18ex1-before.dot")
    assert a.Explode()
    b = Pair.CreateTree("[[[[0,9],2],3],4]")
    assert str(a) == str(b)
    # a.WriteToDotFile("18ex1-after.dot")

    a = Pair.CreateTree("[7,[6,[5,[4,[3,2]]]]]")
    # a.WriteToDotFile("18ex2-before.dot")
    assert a.Explode()
    b = Pair.CreateTree("[7,[6,[5,[7,0]]]]")
    assert str(a) == str(b)
    # a.WriteToDotFile("18ex2-after.dot")

    a = Pair.CreateTree("[[6,[5,[4,[3,2]]]],1]")
    # a.WriteToDotFile("18ex3-before.dot")
    assert a.Explode()
    b = Pair.CreateTree("[[6,[5,[7,0]]],3]")
    assert str(a) == str(b)
    # a.WriteToDotFile("18ex3-after.dot")

    a = Pair.CreateTree("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    # a.WriteToDotFile("18ex4-before.dot")
    assert a.Explode()
    b = Pair.CreateTree("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    assert str(a) == str(b)
    # a.WriteToDotFile("18ex4-after.dot")

    a = Pair.CreateTree("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    # a.WriteToDotFile("18ex5-before.dot")
    assert a.Explode()
    b = Pair.CreateTree("[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
    assert str(a) == str(b)
    # a.WriteToDotFile("18ex5-after.dot")


def AdditionTest():
    a = Pair.CreateTree("[[[[4,3],4],4],[7,[[8,4],9]]]")
    b = Pair.CreateTree("[1,1]")
    c = a + b
    d = Pair.CreateTree("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
    assert str(c) == str(d)


TEST = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""


def DoHomework(lines: list[str]) -> int:
    a = Pair.CreateTree(lines[0])
    for line in lines[1:]:
        b = Pair.CreateTree(line)
        a = a + b
    a.WriteToDotFile("18.dot")
    return a.Magnitude()


def FindLargest(lines: list[str]) -> int:
    largest = -1
    for line1, line2 in permutations(lines, 2):
        a = Pair.CreateTree(line1)
        b = Pair.CreateTree(line2)
        c = a + b
        mag = c.Magnitude()
        largest = max(largest, mag)
    return largest


if __name__ == "__main__":
    # ExplodeTests()
    # AdditionTest()
    lines = TEST.splitlines()
    part1 = DoHomework(lines)
    assert part1 == 4140
    part2 = FindLargest(lines)
    assert part2 == 3993

    with open("18.txt", "r") as infile:
        lines = infile.read().splitlines()
    part1 = DoHomework(lines)
    print(f"Part 1: {part1}")
    part2 = FindLargest(lines)
    print(f"Part 2: {part2}")
