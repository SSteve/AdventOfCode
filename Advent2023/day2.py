from math import prod

TEST = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


def analyze_games(games: list[str], cubes: dict[str, int]) -> int:
    sum = 0
    for game in games:
        game, reveals = game.split(": ")
        # Set the value for this game to the game id. If the game is invalid, it will be set to zero.
        value_for_game = int(game.split()[1])
        for reveal in reveals.split("; "):
            for color_count in reveal.split(", "):
                count, color = color_count.split()
                if int(count) > cubes[color]:
                    value_for_game = 0
                    break
            if value_for_game == 0:
                break
        sum += value_for_game

    return sum


def find_least(games: list[str]) -> int:
    power_sum = 0
    for game in games:
        minimums = {"blue": 0, "red": 0, "green": 0}
        game, reveals = game.split(": ")
        # Set the value for this game to the game id. If the game is invalid, it will be set to zero.
        for reveal in reveals.split("; "):
            for color_count in reveal.split(", "):
                count, color = color_count.split()
                if int(count) > minimums[color]:
                    minimums[color] = int(count)
        game_value = prod(minimums.values())
        power_sum += game_value

    return power_sum


if __name__ == "__main__":
    part1test = analyze_games(TEST.splitlines(), {"blue": 14, "green": 13, "red": 12})
    print(f"Part 1 test: {part1test}")
    assert part1test == 8

    part2test = find_least(TEST.splitlines())
    print(f"Part 2 test: {part2test}")
    assert part2test == 2286

    with open("day2.txt") as infile:
        games = infile.read().splitlines()

    part1 = analyze_games(games, {"blue": 14, "green": 13, "red": 12})
    print(f"Part 1: {part1}")

    part2 = find_least(games)
    print(f"Part 2: {part2}")
