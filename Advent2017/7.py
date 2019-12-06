import re
from collections import defaultdict

infoRegex = re.compile(r"(\w*) \((\d+)\)( -> )?(.*)")

class TowerProgram:
    def __init__(self, name, weight, children, parentName):
        self.name = name
        self.weight = weight
        self.children = children
        self.parentName = parentName
        self.childWeights = defaultdict(int)

    def __repr__(self):
        return f"{self.name}, parent: {self.parentName}, weight: {self.weight}, children: {self.children}"

    def calcChildWeights(self, tower):
        for childName in self.children:
            child = tower[childName]
            self.childWeights[childName] = child.weight + child.calcChildWeights(tower)
        return sum(self.childWeights.values())

    def unbalancedChild(self, progs):
        weights = defaultdict(list)
        for childName in self.children:
            child = progs[childName]
            grandchildrenWeight = sum([x for x in child.childWeights.values()])
            weights[child.weight + grandchildrenWeight].append(child)
        for value in weights.values():
            if len(value) == 1:
                return value[0]
        return None
    
    def findUnbalancedChildCorrectWeight(self, progs):
        prog = self
        badProg = None
        while badProg == None:
            unbalancedChild = prog.unbalancedChild(progs)
            if unbalancedChild is None:
                badProg = prog
            prog = unbalancedChild

        parent = progs[badProg.parentName]
        balancedChildName = parent.children[0] if parent.children[0] != badProg.name else parent.children[1]
        balancedChild = progs[balancedChildName]
        adjustment = balancedChild.weight + sum(balancedChild.childWeights.values()) - \
            (badProg.weight + sum(badProg.childWeights.values()))
        return badProg.weight + adjustment


def day7a(fileName):
    bottomProgram = "placeholder"
    progs = {}
    with open(fileName) as infile:
        for line in infile:
            match = infoRegex.match(line)
            if match:
                name = match[1]
                weight = int(match[2])
                children = match[4].split(", ") if len(match[4]) > 0 else []
                if name in progs:
                    prog = progs[name]
                    prog.weight = weight
                    prog.children = children
                else:
                    progs[name] = TowerProgram(name, weight, children, "")
                for childName in children:
                    if childName in progs:
                        prog = progs[childName]
                        prog.parentName = name
                    else:
                        progs[childName] = TowerProgram(childName, None, [], name)
    
    with open("7.dot", "w") as outfile:
        print("graph Towers {", file=outfile)
        for prog in progs.values():
            if len(prog.parentName) == 0:
                bottomProgram = prog
            for child in prog.children:
                print(f"{prog.name} -- {child};", file=outfile)
        print("}", file=outfile)

        progs[bottomProgram.name].calcChildWeights(progs)

    return progs, bottomProgram


def day7b(progs, bottomProgram):
    correctWeight = bottomProgram.findUnbalancedChildCorrectWeight(progs)
    return correctWeight


if __name__ == "__main__":
    progs, bottomProgram = day7a("7.txt")
    print(f"Bottom: {bottomProgram.name}")
    correctWeight = day7b(progs, bottomProgram)
    print(f"Correct weight: {correctWeight}")
