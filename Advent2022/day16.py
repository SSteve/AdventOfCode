import re
from dataclasses import dataclass
from typing import Callable, Iterable, Optional, TypeVar

from frozendict import frozendict

from generic_search import Node, Queue, nodeToPath

TEST = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

valve_regex = re.compile(
    r"Valve (..) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.+)")


class Valve:
    def __init__(self, input: str) -> None:
        match = valve_regex.match(input)
        if match is None:
            raise ValueError(f"Invalid input: {input}")
        self.name = match[1]
        self.flow_rate = int(match[2])
        self.destinations = match[3].split(", ")

    def __repr__(self) -> str:
        return (f"Valve {self.name}, flow rate: {self.flow_rate}, destinations: {', '.join(self.destinations)}")


@dataclass(frozen=True)
class ValveState:
    name: str
    # True if valve is open
    valve_states: dict[str, bool]
    minute: int


T = TypeVar('T')


def astar_max(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], Iterable[T]],
              cost: Callable[[T, T], float]) -> Optional[Node[T]]:
    """
    Perform an A* search looking for the highest cost.
    """
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None, 0.0))
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
                frontier.push(Node(child, current_node, new_cost))
    return None  # went through everything and never found goal


class Cave:
    def __init__(self, input: list[str]) -> None:
        self.valves: dict[str, Valve] = {}
        for line in input:
            valve = Valve(line)
            self.valves[valve.name] = valve

    def finished(self, state: ValveState):
        return state.minute == self.minutes and all(state.valve_states.values())

    def successors(self, state: ValveState) -> Iterable[ValveState]:
        # If all the valves are open, we don't move.
        if all(state.valve_states.values()):
            yield state
        else:
            # If this valve isn't open and isn't broken, we can spend this round opening the valve.
            if not state.valve_states[state.name] and self.valves[state.name].flow_rate != 0:
                new_valves: dict[str, bool] = {}
                # Set this valve's state to open. Leave other states as-is.
                for valve_state in state.valve_states:
                    new_valves[valve_state] = state.valve_states[valve_state] if valve_state != state.name else True
                yield ValveState(state.name, frozendict(new_valves), state.minute + 1)
            for new_valve in self.valves[state.name].destinations:
                yield ValveState(new_valve, state.valve_states, state.minute + 1)

    def cost(self, state1: ValveState, state2: ValveState):
        if state1.name == state2.name and not state1.valve_states[state1.name] and state2.valve_states[state1.name]:
            return (self.minutes - state1.minute) * self.valves[state1.name].flow_rate
        return 0

    def find_maximum_pressure_release(self, minutes: int) -> int:
        self.minutes = minutes
        valve_states = frozendict(
            (v, self.valves[v].flow_rate == 0) for v in self.valves)
        solution = astar_max(ValveState("AA", valve_states, 1),
                             self.finished,
                             self.successors,
                             self.cost)
        if solution is None:
            raise ValueError("No solution found.")
        # for node in nodeToPath(solution):
        #    print(
        #        f"In {node.name} minute {node.minute} valves: {node.valve_states.values()}.")
        return int(solution.cost)

    def dot_representation(self) -> str:
        dot_text = "graph {\n"
        for valve in self.valves.items():
            for dest_valve in valve[1].destinations:
                dot_text += f"    {valve[0]} -- {dest_valve}\n"
        dot_text += "}\n"
        return dot_text


if __name__ == "__main__":
    cave = Cave(TEST.splitlines())
    print(cave.dot_representation())

    part1test = cave.find_maximum_pressure_release(30)
    print(f"Part 1 test: {part1test}")

    assert (part1test == 1651)

    with open("day16.txt") as infile:
        cave = Cave(infile.read().splitlines())
    part1 = cave.find_maximum_pressure_release(30)
    print(f"Part 1: {part1}")
