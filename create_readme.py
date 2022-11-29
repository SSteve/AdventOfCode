import os
from datetime import datetime, timedelta


def create_readme(year: int, this_year: int, base_path: str):
    """
    year: The year whose README we're building.
    this_year: The most recent year of Advent of Code.
    base_path: The base path for the solution files.
    """
    print(f"# Advent of Code {year}")
    print()
    print(
        f"## Solutions to [Advent of Code {year}](https://adventofcode.com/{year}/) puzzles")
    print()
    print("### Jump to")
    for link_year in range(2015, this_year + 1):
        if link_year == year:
            continue
        print(
            f"- [{link_year}](https://github.com/SSteve/AdventOfCode/tree/master/Advent{link_year})")
    print()

    # Include notes for this year
    if os.path.isfile(f"{base_path}/notes.txt"):
        for notes_line in open(f"{base_path}/notes.txt"):
            print(notes_line)

    print("### The Puzzles")

    end_of_advent = datetime(this_year, 12, 25)
    # Convert local time to EST.
    today = datetime.now() + timedelta(hours=3)
    if today > end_of_advent:
        last_day = 25
    else:
        last_day = today.day

    for day in range(1, last_day + 1):
        day_string = f"- Dec {day} - [instructions](http://adventofcode.com/{year}/day/{day})"
        if os.path.isfile(f"{base_path}/day{day}.py"):
            day_string += f" - [solution](./day{day}.py) (Python)"
        if os.path.isfile(f"{base_path}/{day}.py"):
            day_string += f" - [solution](./{day}.py) (Python)"
        if os.path.isfile(f"{base_path}/{day}a.py"):
            day_string += f" - [part 1 solution](./{day}a.py) (Python)"
        if os.path.isfile(f"{base_path}/{day}b.py"):
            day_string += f" - [part 2 solution](./{day}b.py) (Python)"
        if os.path.isfile(f"{base_path}/{day}.swift"):
            day_string += f" - [solution](./{day}.swift) (Swift)"
        if os.path.isfile(f"{base_path}/Day{day}/Day{day}/Program.cs"):
            day_string += f" - [solution](./Day{day}/Day{day}/Program.cs) (C#)"
        if os.path.isfile(f"{base_path}/{day}.S"):
            day_string += f" - [solution](./{day}.S) (ARM64 asm)"
        if os.path.isfile(f"{base_path}/day{day}/src/main.rs"):
            day_string += f" - [solution](./day{day}/src/main.rs) (Rust)"
        print(day_string)


if __name__ == "__main__":
    now = datetime.now()
    this_year = now.year
    if now.month < 12:
        this_year -= 1

    # Get the last four characters of the current directory.
    directory_year = os.getcwd()[-4:]
    if directory_year.isnumeric():
        # If we're in the directory for a year, this is the year we're building.
        year = int(directory_year)
        # Set the base path to the current directory.
        base_path = '.'
    else:
        # If we're in the root AoC directory, build the read me for the current year.
        year = this_year
        # Set the base path to the child directory for this year.
        base_path = f"Advent{year}"

    create_readme(year, this_year, base_path)
