from enum import Enum

class WireDirection(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    CORNER = 5
    
    @classmethod
    def from_string(cls, direction_string):
        if direction_string == "U":
            return WireDirection.UP
        if direction_string == "R":
            return WireDirection.RIGHT
        if direction_string == "D":
            return WireDirection.DOWN
        if direction_string == "L":
            return WireDirection.LEFT
        raise ValueError(f"Unknown direction string: {direction_string}")


class WirePoint:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        
    def point_at_direction(self, direction, is_corner):
        if direction == WireDirection.UP:
            return WirePoint(self.x, self.y + 1, WireDirection.CORNER if is_corner else WireDirection.UP)
        if direction == WireDirection.RIGHT:
            return WirePoint(self.x + 1, self.y, WireDirection.CORNER if is_corner else WireDirection.RIGHT)
        if direction == WireDirection.DOWN:
            return WirePoint(self.x, self.y - 1, WireDirection.CORNER if is_corner else WireDirection.DOWN)
        if direction == WireDirection.LEFT:
            return WirePoint(self.x - 1, self.y, WireDirection.CORNER if is_corner else WireDirection.LEFT)
        raise ValueError("Direction wasn't a cardinal direction.")
        
    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)
        
    # Points are equal even if their direction is different
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def __hash__(self):
        return hash((self.x, self.y))
        
    def __repr__(self):
        return f"({self.x}, {self.y}) - {self.direction}"
        
        
class Wire:
    def __init__(self, wire_text):
        self.create_points(wire_text)
        
    def create_points(self, wire_text):
        self.points = []
        paths = wire_text.split(",")
        current_point = WirePoint(0, 0, WireDirection.CORNER)
        for path in paths:
            direction = WireDirection.from_string(path[0])
            distance = int(path[1:])
            for i in range(distance):
                next_point = current_point.point_at_direction(direction, i == distance - 1)
                self.points.append(next_point)
                current_point = next_point
            
    def intersections(self, other_wire):
        return set(self.points).intersection(set(other_wire.points))
        
    # The number of steps it takes to get to the given point
    def steps_to_point(self, point):
        try:
            # We add 1 because the origin isn't included in the list
            return self.points.index(point) + 1
        except:
            return 1e30
        
class FrontPanel:
    def __init__(self, wire1_text, wire2_text):
        self.wire1 = Wire(wire1_text)
        self.wire2 = Wire(wire2_text)
    
    def closest_intersection(self):
        intersections = self.wire1.intersections(self.wire2)
        closest = 1e30
        closest_point = None
        for intersection in intersections:
            this_distance = abs(intersection.x) + abs(intersection.y)
            if this_distance < closest:
                closest = this_distance
                closest_point = intersection
        return closest_point
        
    def shortest_delay(self):
        intersections = self.wire1.intersections(self.wire2)
        closest = 1e30
        for intersection in intersections:
            this_distance = self.wire1.steps_to_point(intersection) + self.wire2.steps_to_point(intersection)
            if this_distance < closest:
                closest = this_distance
        return closest
        
        
if __name__ == "__main__":
    # Tests
    panel = FrontPanel("R8,U5,L5,D3", "U7,R6,D4,L4")
    assert panel.closest_intersection().manhattan_distance() == 6, "Test 1-1 failed"
    assert panel.shortest_delay() == 30, f"Test 1-2 failed. Delay was {panel.shortest_delay()}"
    panel = FrontPanel("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83")
    assert panel.closest_intersection().manhattan_distance() == 159, "Test 2-1 failed"
    assert panel.shortest_delay() == 610, "Test 1-2 failed"
    panel = FrontPanel("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
    assert panel.closest_intersection().manhattan_distance() == 135, "Test 3-1 failed"
    assert panel.shortest_delay() == 410, "Test 1-2 failed"

    # Part 2 tests
    
    with open("3.txt") as infile:
        wire1_text = infile.readline()
        wire2_text = infile.readline()
    panel = FrontPanel(wire1_text, wire2_text)
    print(f"Part one: closest is {panel.closest_intersection().manhattan_distance()}")
    print(f"Part two: closest is {panel.shortest_delay()}")