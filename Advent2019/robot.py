# This is the robot from day 11. I'm using it to test the IntCode computer

from __future__ import annotations
from collections import defaultdict
from enum import IntEnum
from math import inf
from typing import Dict, List, NamedTuple

from intcode import IntCode

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def turn(current_direction: Direction, turn_code: int) -> Direction:
        if turn_code == 0:
            return (current_direction - 1) % 4
        return (current_direction + 1) % 4

    @staticmethod
    def move_directions():
        # Values to add to a Point to move up, right, down, and left
        return [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]

class Point(NamedTuple):
    x: int = 0
    y: int = 0

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

class Robot:
    def __init__(self, int_code_program: str, starting_value: int):
        self.location: Point = Point(0, 0)
        self.painted_panels: Dict[Point, int] = defaultdict(int)
        self.heading: Direction = Direction.UP
        self.computer = IntCode(int_code_program, input_queue=[starting_value], interactive=False)

    def run(self):
        self.computer.run()
        while not self.computer.halted:
            new_color = self.computer.output_values.pop(0)
            new_direction = self.computer.output_values.pop(0)
            self.painted_panels[self.location] = new_color
            self.heading = Direction.turn(self.heading, new_direction)
            self.location = self.location + Direction.move_directions()[self.heading]
            self.computer.accept_input(0 if not self.location in self.painted_panels else self.painted_panels[self.location])
            self.computer.run()

    def get_message(self):
        min_x = inf
        max_x = -inf
        min_y = inf
        max_y = -inf
        for location in self.painted_panels.keys():
            min_x = min(location.x, min_x)
            max_x = max(location.x, max_x)
            min_y = min(location.y, min_y)
            max_y = max(location.y, max_y)
        rows: List[str] = []
        for y in range(min_y, max_y + 1):
            row: List[str] = []
            for x in range(min_x, max_x + 1):
                row.append(" " if self.painted_panels[Point(x, y)] == 0 else "*")
            rows.append(''.join(row))
        return '\n'.join(rows)
