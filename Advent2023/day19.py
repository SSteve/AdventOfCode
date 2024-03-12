from math import prod

TEST = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


class WorkflowStep:
    category: str | None
    op_is_gt: bool
    compare_value: int
    result: str

    def __init__(self, step_string: str):
        if ":" in step_string:
            self.category = step_string[0]
            self.op_is_gt = step_string[1] == ">"
            value_string, self.result = step_string[2:].split(":")
            self.compare_value = int(value_string)
        else:
            self.category = None
            self.result = step_string

    def process_part(self, part: dict[str, int]) -> str | None:
        if self.category is None:
            return self.result
        if self.op_is_gt:
            return self.result if part[self.category] > self.compare_value else None
        else:
            return self.result if part[self.category] < self.compare_value else None

    def part_with_filter(self, part: dict[str, set[int]]) -> dict[str, set[int]]:
        # Return the resultant part after applying this step's filter to the given part.
        if self.category is None:
            raise ValueError("Can't apply a filter to a workflow step with no category.")

        new_part: dict[str, set[int]] = {}
        values_to_remove = set(range(self.compare_value + 1)) if self.op_is_gt else set(range(self.compare_value, 4001))
        for category in ("x", "m", "a", "s"):
            if category == self.category:
                new_part[category] = part[category] - values_to_remove
            else:
                new_part[category] = set(part[category])
        return new_part

    def remove_filtered_values(self, part: dict[str, set[int]]) -> None:
        # Remove the values that do not pass this step's filter from the given part.
        if self.category is None:
            raise ValueError("Can't apply a filter to a workflow step with no category.")
        values_to_remove = set(range(self.compare_value + 1, 4001)) if self.op_is_gt else set(range(self.compare_value))
        part[self.category] = part[self.category] - values_to_remove

    def __repr__(self):
        if self.category:
            return f"{self.category}{'>' if self.op_is_gt else '<'}{self.compare_value}:{self.result}"
        return self.result


class Workflow:
    steps: list[WorkflowStep]

    def __init__(self, line: str):
        self.steps = []
        for step in line.split(","):
            self.steps.append(WorkflowStep(step))

    def process_part(self, part: dict[str, int]):
        for step in self.steps:
            if result := step.process_part(part):
                return result

    def __str__(self):
        return ",".join(self.steps)


def part_from_string(part_string: str) -> dict[str, int]:
    part: dict[str, int] = {}
    for category in part_string.split(","):
        part[category[0]] = int(category[2:])
    return part


def process_part(part: dict[str, int], workflows: dict[str, Workflow]) -> int:
    # Use the given workflows to process the part. If the part is accepted,
    # return the sum of its category values. If not, return 0.

    workflow_result = "in"
    while workflow_result not in ["A", "R"]:
        workflow = workflows[workflow_result]
        workflow_result = workflow.process_part(part)

    if workflow_result == "R":
        return 0

    return sum(part.values())


def process_parts(lines: list[str]) -> int:
    workflows: dict[str, Workflow] = {}
    parts: list[dict[str, int]] = []

    reading_workflows = True
    for line in lines:
        if len(line) == 0:
            reading_workflows = False
            continue
        if reading_workflows:
            brace_position = line.index("{")
            workflows[line[:brace_position]] = Workflow(line[brace_position + 1 : -1])
        else:
            parts.append(part_from_string(line[1:-1]))
    return sum(process_part(part, workflows) for part in parts)


def combinations_for_workflow(name: str, part: dict[str, set[int]], workflows: dict[str, Workflow]) -> int:
    # Count the number of combinations of parts that pass through this workflow.
    combinations = 0

    if name == "R":
        return 0

    if name == "A":
        return prod(len(v) for v in part.values())

    workflow = workflows[name]
    for step in workflow.steps:
        if step.category is None:
            # We've reached the last step in this workflow.
            if step.result == "A":
                # This part is accepted so add the total number of combinations left in the part.
                combinations += prod(len(v) for v in part.values())
            elif step.result != "R":
                # If the remainder of the part is going to another workflow, add the nubmer of
                # combinations from that workflow. (If the part is rejected, the number of combinations
                # won't be affected.)
                combinations += combinations_for_workflow(step.result, part, workflows)
        else:
            new_part = step.part_with_filter(part)
            combinations += combinations_for_workflow(step.result, new_part, workflows)
            step.remove_filtered_values(part)

    return combinations


def count_ratings_combinations(lines: list[str]) -> int:
    workflows: dict[str, Workflow] = {}

    for line in lines:
        if len(line) == 0:
            break
        brace_position = line.index("{")
        workflows[line[:brace_position]] = Workflow(line[brace_position + 1 : -1])

    part: dict[str, set[int]] = {
        "x": set(range(1, 4001)),
        "m": set(range(1, 4001)),
        "a": set(range(1, 4001)),
        "s": set(range(1, 4001)),
    }

    return combinations_for_workflow("in", part, workflows)


if __name__ == "__main__":
    part1test = process_parts(TEST.splitlines())
    print(f"Part 1 test: {part1test}")
    assert part1test == 19114

    part2test = count_ratings_combinations(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 167_409_079_868_000

    with open("day19.txt") as infile:
        lines = infile.read().splitlines()

    part1 = process_parts(lines)
    print(f"Part 1: {part1}")
    assert part1 == 374873

    part2 = count_ratings_combinations(lines)
    print(f"Part 2: {part2}")
    assert part2 == 122_112_157_518_711
