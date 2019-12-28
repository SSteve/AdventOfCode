from intcode import IntCode
from typing import Iterable, List, Tuple

def around(x: int, y: int):
    yield (x, y - 1) # Up
    yield (x + 1, y) # Right
    yield (x, y + 1) # Down
    yield (x - 1, y) # Left

if __name__ == '__main__':
    with open("17.txt") as infile:
        computer = IntCode(infile.readline(), interactive=False)

    computer.run()
    map: List[List[str]] = []
    row_characters: List[str] = []
    for val in computer.output_values:
        if val == 10:
            if len(row_characters) > 1:
                map.append(row_characters)
            row_characters = []
        else:
            row_characters.append(chr(val))
    row_count = len(map)
    row_width = len(map[0])
    alignment_parameters_sum = 0
    for row_number, row in enumerate(map):
        for col, char in enumerate(row):
            scaffold_count = 0
            if char == "#":
                for test_col, test_row in around(col, row_number):
                    if test_row >= 0 and test_row < row_count and test_col >= 0 and test_col < row_width and (map[test_row][test_col] == "#" or map[test_row][test_col] == "O"):
                        scaffold_count += 1
            if scaffold_count > 2:
                alignment_parameters_sum += row_number * col
                map[row_number][col] = "O"

    # for row in map:
    #     print(''.join(row))
    # 20 is wrong
    # 12 is wrong
    # Duh. I'm giving the number of intersections instead of the "alignment parameters"
    print(f"alignment_parameters_sum = {alignment_parameters_sum}")

    assert alignment_parameters_sum == 7816

    # with open("17.txt") as infile:
    #     computer = IntCode(infile.readline(), interactive=False)

    computer.set_memory(0, 2)
    computer.output_values.clear()
    computer.halted = False

    movement_routine = "A,A,B,C,B,C,B,C,B,A\n"
    movement_functions = ["R,10,L,12,R,6\n", "R,6,R,10,R,12,R,6\n", "R,10,L,12,L,12\n"]
    video_feed = "n\n"

    computer.run()
    computer.show_output_message()
    for ch in movement_routine:
        computer.accept_input(ord(ch))
    computer.run()
    for movement_function in movement_functions:
        computer.show_output_message()
        for ch in movement_function:
            computer.accept_input(ord(ch))
        computer.run()
    computer.show_output_message()
    for ch in video_feed:
        computer.accept_input(ord(ch))
    computer.run()

    computer.show_output_message()
    print(f"{computer.output_values[0]} dust collected")
