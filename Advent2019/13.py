from intcode import IntCode
from math import inf
from time import sleep
from typing import Dict, List, NamedTuple

class Point(NamedTuple):
    x: int
    y: int

class GameState(NamedTuple):
    paddle: Point
    ball: Point
    blocks: int

TILES: Dict[int, str] = {0: " ", 1: "#", 2: "X", 3: "—", 4: "o"}

def show_screen(values: List[int], pixels: Dict[Point, int]) -> int:
    score = -1
    index = 0
    blocks = 0
    paddle: Point = Point(0, 0)
    ball: Point = Point(0, 0)
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
            print(f"\033[{values[index + 1] + 10};{values[index] + 10}H{TILES[values[index + 2]]}", end='')
        index += 3

    blocks = sum(1 for pixel in pixels.values() if pixel == 2)
    if score > 0:
        print(f"\033[5;0HScore: {score}", end='')
    print(f"\033[6;0HBlocks: {blocks}  ", end='')
    # Print a line with a carriage return to flush output buffer
    print(f"\033[35;0H ")
    return GameState(paddle, ball, blocks)

if __name__ == '__main__':
    with open("13.txt") as infile:
        computer: IntCode = IntCode(infile.readline(), interactive=False)
    computer.run()

    pixels: Dict[Point, int] = {}
    game_state: GameState = show_screen(computer.output_values, pixels)
    # print(f"{game_state.blocks} blocks")

    with open("13.txt") as infile:
        computer: IntCode = IntCode(infile.readline(), interactive=False)
    computer.memory[0] = 2
    previous_ball_state = game_state.ball
    next_input = 0
    while game_state.blocks > 0 and game_state.ball.y < game_state.paddle.y:
        computer.accept_input(next_input)
        computer.run()
        game_state: GameState = show_screen(computer.output_values, pixels)
        sleep(0.02)
        computer.output_values.clear()
        if game_state.ball.x > game_state.paddle.x:
            next_input = 1
        elif game_state.ball.x < game_state.paddle.x:
            next_input = -1
        else:
            next_input = 0
    previous_ball_state = game_state.ball

    
