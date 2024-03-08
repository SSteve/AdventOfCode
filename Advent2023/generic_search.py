# Adapted from Classic Computer Science Problems in Python
# (https://www.manning.com/books/classic-computer-science-problems-in-python)
# by David Kopec
from __future__ import annotations

from collections import deque
from heapq import heappop, heappush
from typing import Callable, Generic, Iterable, Optional, TypeVar

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: list[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: deque[T] = deque()

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def __repr__(self):
        return f"Node(state={self.state}, cost={self.cost}, heuristic={self.heuristic}"


def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], Iterable[T]]) -> Optional[Node[T]]:
    # frontier is where we've yet to go
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored: set[T] = {initial}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # went through everything and never found goal


def nodeToPath(node: Node[T]) -> list[T]:
    path: list[T] = [node.state]
    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], Iterable[T]]) -> Optional[Node[T]]:
    """
    Perform breadth-first search.

    The bfs search finds the shortest path from an initial state to
    a final goal state. It uses callbacks to identify the final goal
    and successors to the current state.

    This implementation is adapted from "Classic Computer Science
    Problems in Python" by David Kopec.

    Parameters
    ----------
    initial : T
        The initial state. T must be a hashable type. (Note a
        dictionary is not a hashable type.)
    goal_test : Callable[[T], bool]
        A function that takes a state as input and returns True if
        the goal has been reached.
    successors : Callable[[T], Iterable[T]]
        A function that takes a state as input and returns 0 or
        more states that can come after that state.

    Returns
    -------
    Returns a Node object containing the final state or None if no solution
    was found. The entire solution path is obtained by calling `nodeToPath`.
    """
    # frontier is where we've yet to go
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored: set[T] = {initial}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # went through everything and never found goal


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: list[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        return repr(self._container)


def astar(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], Iterable[T]],
          heuristic: Callable[[T], float], cost: Callable[[T, T], float]) -> Optional[Node[T]]:
    """
    Perform an A* search.

    The A* search finds the optimal cost path from an initial state to
    a final goal state. It uses callbacks to identify the final goal,
    successors to the current state, the heuristic (described below),
    and the cost between one state and the next.

    This implementation is adapted from "Classic Computer Science
    Problems in Python" by David Kopec.

    Parameters
    ----------
    initial : T
        The initial state. T must be a hashable type. (Note a
        dictionary is not a hashable type.)
    goal_test : Callable[[T], bool]
        A function that takes a state as input and returns True if
        the goal has been reached.
    successors : Callable[[T], Iterable[T]]
        A function that takes a state as input and returns 0 or
        more states that can come after that state.
    hueristic : Callable[[T], float]
        A function that takes a state as input and returns a best-guess
        cost from there to the goal. It is allowed to be lower than the
        real cost but must never be higher.
    cost : Callable[[T, T], float]
        A function that takes two states as input and returns the
        actual cost to go from the first to the second.

    Returns
    -------
    Returns a Node object containing the final state, the total cost to
    get there, the state's heuristic value, and a pointer to the
    previous Node in the solution. The entire solution path is obtained
    by calling `nodeToPath`.
    """
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # explored is where we've been
    explored: dict[T, float] = {initial: 0.0}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for child in successors(current_state):
            new_cost: float = current_node.cost + cost(current_state, child)

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node,
                              new_cost, heuristic(child)))
    return None  # went through everything and never found goal
