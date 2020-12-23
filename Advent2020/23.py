class Node:
    def __init__(self, prev: int, next: int):
        self.prev = prev
        self.next = next
        self.up = False
        
def MakeNodes(data: str):
    values = [int(ch) - 1 for ch in data]
    nodes = []
    for value in range(len(values)):
        index = values.index(value)
        prev = values[(index - 1) % len(values)]
        next = values[(index + 1) % len(values)]
        nodes.append(Node(prev, next))
    return nodes, values[0]
    
def MakeNodes2(data: str):
    nodes, current = MakeNodes(data)
    nodes[nodes[current].prev].next = len(nodes)
    firstNewNode = len(nodes)
    for value in range(len(nodes), 1_000_000):
        nodes.append(Node(value - 1, value + 1))
    
    nodes[999_999].next = current
    nodes[firstNewNode].prev = nodes[current].prev
    nodes[current].prev = 999_999
    return nodes, current
    
def Turn(current: int, nodes):
    up = nodes[current].next
    firstUp = up
    for _ in range(3):
        nodes[up].up = True
        up = nodes[up].next
    lastUp = nodes[up].prev
    destination = (current - 1) % len(nodes)
    while nodes[destination].up:
        destination = (destination - 1) % len(nodes)
    nodes[current].next = nodes[lastUp].next
    nodes[nodes[lastUp].next].prev = current
    nodes[lastUp].next = nodes[destination].next
    nodes[firstUp].prev = destination
    nodes[nodes[destination].next].prev = lastUp
    nodes[destination].next = firstUp
    up = firstUp
    for _ in range(3):
        nodes[up].up = False
        up = nodes[up].next
    return nodes[current].next
    
def PrintNodes(current: int, nodes):
    print(f"({current + 1})", end='')
    index = nodes[current].next
    for _ in range(min(len(nodes) - 1, 20)):
        print(f" {index + 1}", end='')
        index = nodes[index].next
    print()
    for _ in range(min(len(nodes) - 1, 20)):
        print(f" {index + 1}", end='')
        index = nodes[index].prev
    print()
        
def Answer(nodes):
    answer = ''
    node = nodes[0].next
    for _ in range(len(nodes) - 1):
        answer += str(node + 1)
        node = nodes[node].next
    return answer
    
def Answer2(nodes):
    cup1 = nodes[0].next
    cup2 = nodes[cup1].next
    return (cup1 + 1) * (cup2 + 1)
    
    
TEST = "389125467"

DATA = "487912365"

testNodes, current = MakeNodes(TEST)
for _ in range(100):
    current = Turn(current, testNodes)
assert Answer(testNodes) == '67384529'

nodes, current = MakeNodes(DATA)
for _ in range(100):
    current = Turn(current, nodes)
print(Answer(nodes))
assert Answer(nodes) == '89573246'

testNodes, current = MakeNodes2(TEST)
for _ in range(10_000_000):
    current = Turn(current, testNodes)
assert Answer2(testNodes) == 149245887792

nodes, current = MakeNodes2(DATA)
for _ in range(10_000_000):
    current = Turn(current, nodes)
print(Answer2(nodes))
