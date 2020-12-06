import os
import sys
from sys import argv

THIS_YEAR = 2020


def create_readme(year: int):
    print(f"# Advent of Code {year}")
    print()
    print(f"## Solutions to [Advent of Code {year}](https://adventofcode.com/{year}/) puzzles")
    print()
    print("### Jump to")
    for link_year in range(2015, THIS_YEAR + 1):
        if link_year == year:
            continue
        print(f"- [{link_year}](https://github.com/SSteve/AdventOfCode/tree/master/Advent{link_year})")
    print()

    # Include notes for this year
    if os.path.isfile(f"Advent{year}/notes.txt"):
        for notes_line in open(f"Advent{year}/notes.txt"):
            print(notes_line)

    print("### The Puzzles")

    for day in range(1, 26):
        day_string = f"- Dec {day} - [instructions](http://adventofcode.com/{year}/day/{day})"
        if os.path.isfile(f"Advent{year}/{day}.py"):
            day_string += f" - [solution](./{day}.py) (Python)"
        if os.path.isfile(f"Advent{year}/{day}a.py"):
            day_string += f" - [part 1 solution](./{day}a.py) (Python)"
        if os.path.isfile(f"Advent{year}/{day}b.py"):
            day_string += f" - [part 2 solution](./{day}b.py) (Python)"
        if os.path.isfile(f"Advent{year}/{day}.swift"):
            day_string += f" - [solution](./{day}.swift) (Swift)"
        if os.path.isfile(f"Advent{year}/Day{day}/Day{day}/Program.cs"):
            day_string += f" - [solution](./Day{day}/Day{day}/Program.cs) (C#)"
        if os.path.isfile(f"Advent{year}/{day}.S"):
            day_string += f" - [solution](./{day}.S) (ARM64 asm)"
        print(day_string)


if __name__ == "__main__":
    year = THIS_YEAR if len(argv) < 2 else int(argv[1])
    create_readme(year)
