TEST = """30373
25512
65332
33549
35390"""


def build_forest(trees: list[str]) -> list[list[int]]:
    forest: list[list[int]] = []
    for tree_line in trees:
        line: list[int] = []
        for tree in tree_line:
            line.append(int(tree))
        forest.append(line)

    return forest


def count_visible_trees(forest: list[list[int]]) -> int:
    # Count all the trees on the outside edge.
    count = len(forest) * 2 + (len(forest[0]) - 2) * 2
    for x in range(1, len(forest[0]) - 1):
        for y in range(1, len(forest) - 1):
            this_tree = forest[y][x]
            is_visible = all(tree < this_tree for tree in forest[y][:x]) or \
                all(tree < this_tree for tree in forest[y][x+1:]) or \
                all(tree < this_tree for tree in (line[x] for line in forest[:y])) or \
                all(tree < this_tree for tree in (
                    line[x] for line in forest[y+1:]))
            if is_visible:
                count += 1
    return count


def find_highest_scenic_score(forest: list[list[int]]) -> int:
    highest_score = 0
    for this_x in range(1, len(forest[0]) - 1):
        for this_y in range(1, len(forest) - 1):
            this_tree = forest[this_y][this_x]
            left_score = 0
            for x in range(this_x - 1, -1, -1):
                left_score += 1
                if forest[this_y][x] >= this_tree:
                    break
            right_score = 0
            for x in range(this_x + 1, len(forest[0])):
                right_score += 1
                if forest[this_y][x] >= this_tree:
                    break
            up_score = 0
            for y in range(this_y - 1, -1, -1):
                up_score += 1
                if forest[y][this_x] >= this_tree:
                    break
            down_score = 0
            for y in range(this_y + 1, len(forest)):
                down_score += 1
                if forest[y][this_x] >= this_tree:
                    break
            highest_score = max(left_score * up_score *
                                down_score * right_score, highest_score)

    return highest_score


if __name__ == "__main__":
    forest = build_forest(TEST.splitlines())
    part1test = count_visible_trees(forest)
    print(f"Part 1 test: {part1test}")
    assert (part1test == 21)

    part2test = find_highest_scenic_score(forest)
    print(f"Part 2 test: {part2test}")
    assert (part2test == 8)

    with open("day8.txt") as infile:
        trees = infile.read().splitlines()
    forest = build_forest(trees)
    part1 = count_visible_trees(forest)
    print(f"Part 1: {part1}")
    assert (part1 == 1794)

    part2 = find_highest_scenic_score(forest)
    print(f"Part 2: {part2}")
    assert (part2 == 199272)
