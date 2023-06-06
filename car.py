import random

from vector import Vector


class Car:
    def __init__(self, direction, position):
        self.direction = direction
        self.position = Vector(position[1] * 7, position[0] * 7)  # grid size 5
        self.position_normal = Vector(position[1], position[0])
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.old_v = 0  ## helping variable to move function in simulation
        self.odometer = 0 # measuring the distance traveled by an object
        self.will_turn = False
        self.will_turn_right = False
        self.will_turn_left = False
        self.go = False
        self.can_draw_turn = False
        self.WILL_TURN_PROPABILITY = 0.5
        self.WILL_TURN_RIGHT_PROPABILITY = 0.7
        self.draw_next_turn()
        self.can_change_direction = False
        color_r = random.randint(50, 200)
        color_g = random.randint(50, 200)
        color_b = random.randint(50, 200)
        self.color = (color_r, color_g, color_b)

    def draw_next_turn(self):
        # first setting to start values
        self.will_turn = False
        self.will_turn_right = False
        self.will_turn_left = False

        r = random.random()
        if r < self.WILL_TURN_PROPABILITY:
            self.will_turn = True
            r = random.random()
            if r < self.WILL_TURN_RIGHT_PROPABILITY:
                self.will_turn_right = True
            else:
                self.will_turn_left = True
        else:
            self.will_turn = False
            self.will_turn_right = False
            self.will_turn_left = False