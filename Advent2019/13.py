from intcode import IntCode
from math import inf
from typing import Dict, List, NamedTuple

class Point(NamedTuple):
    x: int
    y: int

class GameState(NamedTuple):
    paddle: Point
    ball: Point
    blocks: int

TILES: Dict[int, str] = {0: " ", 1: "#", 2: "X", 3: "—", 4: "o"}

def show_screen(values: List[int], x_range: int, y_range: int) -> int:
    score = -1
    index = 0
    blocks = 0
    paddle: Point = Point(0, 0)
    ball: Point = Point(0, 0)
    pixels: Dict[Point, int] = {}
    while index < len(values):
        if values[index] == -1 and values[index + 1] == 0:
            score = values[index + 2]
        else:
            point = Point(values[index], values[index + 1])
            tile = values[index + 2]
            pixels[point] = tile
            if tile == 3:
                paddle = point
            elif tile == 4:
                ball = point
        index += 3
    for y in range(y_range):
        for x in range(x_range):
            print(TILES[pixels[Point(x, y)]], end='')
            if pixels[Point(x, y)] == 2:
                blocks += 1
        print()
    print(f"Score: {score}")
    return GameState(paddle, ball, blocks)

if __name__ == '__main__':
    with open("13.txt") as infile:
        computer: IntCode = IntCode(infile.readline(), interactive=False)
    computer.run()

    pixels: Dict[Point, int] = {}
    index: int = 0
    min_x: int = inf
    max_x: int = -inf
    min_y: int = inf
    max_y: int = -inf
    while index < len(computer.output_values):
        point = Point(computer.output_values[index], computer.output_values[index + 1])
        pixels[point] = computer.output_values[index + 2]
        index += 3
        min_x = min(min_x, point.x)
        max_x = max(max_x, point.x)
        min_y = min(min_y, point.y)
        max_y = max(max_y, point.y)
    game_state: GameState = show_screen(computer.output_values, max_x + 1, max_y + 1)
    print(f"{game_state.blocks} blocks")

    with open("13.txt") as infile:
        computer: IntCode = IntCode(infile.readline(), interactive=False)
    computer.memory[0] = 2
    previous_ball_state = game_state.ball
    next_input = 0
    while game_state.blocks > 0 and game_state.ball.y < game_state.paddle.y:
        computer.accept_input(next_input)
        computer.run()
        game_state: GameState = show_screen(computer.output_values, max_x + 1, max_y + 1)
        if game_state.ball.x > game_state.paddle.x:
            next_input = 1
        elif game_state.ball.x < game_state.paddle.x:
            next_input = -1
        else:
            next_input = 0
    previous_ball_state = game_state.ball

    
