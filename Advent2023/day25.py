from collections import defaultdict, deque

TEST = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""


def make_dot(network: dict[str, set[str]]) -> str:
    graph = "graph modules {\n"
    for node, connections in network.items():
        for connection in connections:
            if f"\t{connection} -- {node}" not in graph:
                graph += f"\t{node} -- {connection}\n"
    graph += "}\n"
    return graph


def count_connected(from_node: str, network: dict[str, set[str]]) -> int:
    to_process: deque[str] = deque([from_node])
    connections: set[str] = set()
    while to_process:
        node = to_process.popleft()
        connections.add(node)
        for n in network[node]:
            if n in connections:
                continue
            to_process.append(n)

    return len(connections)


def find_groups(lines: list[str]) -> int:
    network: dict[str, set[str]] = defaultdict(set)
    for line in lines:
        component, components = line.split(": ")
        for connected in components.split():
            network[component].add(connected)
            network[connected].add(component)

    with open("day25.dot", "w") as dot:
        dot.write(make_dot(network))

    # Used neato algorithm in Graphviz to identify connections to remove.
    # gzr/qnz, pgz/hgk, lmj-xgs
    network["gzr"].remove("qnz")
    network["qnz"].remove("gzr")
    network["pgz"].remove("hgk")
    network["hgk"].remove("pgz")
    network["lmj"].remove("xgs")
    network["xgs"].remove("lmj")

    group_1_length = count_connected("gzr", network)
    group_2_length = count_connected("qnz", network)

    return group_1_length * group_2_length


if __name__ == "__main__":
    with open("day25.txt") as infile:
        lines = infile.read().splitlines()

    part1 = find_groups(lines)
    print(f"Part 1: {part1}")
