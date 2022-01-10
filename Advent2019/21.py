from intcode import IntCode


def RunSpringScript(program: str, script: str) -> int:
    inputValues = list(map(ord, script))
    springDroid = IntCode(program, inputValues, False)
    springDroid.run()
    for c in springDroid.output_values:
        if c < 128:
            print(chr(c), end="")
        else:
            return c
    return -1


if __name__ == '__main__':
    springScript = """\
NOT A J
NOT J J
AND B J
AND C J
NOT J J
AND D J
WALK
"""
    springScript2 = """\
NOT C J
AND H J
NOT B T
OR T J
NOT A T
OR T J
AND D J
RUN
"""
    with open('21.txt', 'r') as infile:
        program = infile.read().strip()
    part1 = RunSpringScript(program, springScript)
    print(f"Part 1: {part1}")

    part2 = RunSpringScript(program, springScript2)
    print(f"Part 2: {part2}")
