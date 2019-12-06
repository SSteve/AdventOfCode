import os

THIS_YEAR = 2019

def create_readme(year):
	print(f"# Advent of Code {year}")
	print()
	print(f"## Solutions to [Advent of Code {year}](https://adventofcode.com/{year}/) puzzles")
	print()
	print("### Jump to")
	for link_year in range(2015, THIS_YEAR + 1):
		if link_year == year:
			continue;
		print(f"- [{link_year}](https://github.com/SSteve/AdventOfCode/tree/master/Advent{link_year})")
	print()
	
	# Include notes for this year
	try:
		for notes_line in open(f"Advent{year}/notes.txt"):
			print(notes_line)
	except:
		# Don't do anything if notes.txt doesn't exist
		pass
		
	print("### The Puzzles")
	
	for day in range(1, 26):
		if os.path.isfile(f"Advent{year}/{day}.py"):
			print(f"- Dec {day}. - [instructions](http://adventofcode.com/{year}/day/{day}) + [solution](./{day}.py)")
		elif os.path.isfile(f"Advent{year}/{day}a.py"):
			if os.path.isfile(f"Advent{year}/{day}b.py"):
				print(f"- Dec {day}. - [instructions](http://adventofcode.com/{year}/day/{day}) + solutions: [day 1](./{day}a.py), [day 2](./{day}b.py)")
			else:
				print(f"- Dec {day}. - [instructions](http://adventofcode.com/{year}/day/{day}) + solutions: [day 1](./{day}a.py)")
		else:
			print(f"- Dec {day}. - [instructions](http://adventofcode.com/{year}/day/{day})")

if __name__ == "__main__":
	create_readme(2019)