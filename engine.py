import copy

from vector import Vector


class Engine:
    def __init__(self, simulation, map):
        self.simulation = simulation
        self.map = map
        self.ticks = 0
        self.horizontal = False
        self.vertical = True

    def loop(self, time):
        # if self.ticks % 8 == 0:
        #     if self.map.lights_map[11,9] == 1:
        #         self.map.lights_map[11,9] = 0
        #     else:
        #         self.map.lights_map[11, 9] = 1
        if self.ticks % 8 == 0:
            y = self.map.lights_positions_n + self.map.lights_positions_s
            x = self.map.lights_positions_e + self.map.lights_positions_w
            if self.horizontal:
                for pos in y:
                    if self.map.lights_map[pos[0], pos[1]] == 1:
                        self.map.lights_map[pos[0], pos[1]] = 0
                    else:
                        self.map.lights_map[pos[0], pos[1]] = 1
            if self.vertical:
                for pos in x:
                    if self.map.lights_map[pos[0], pos[1]] == 0:
                        self.map.lights_map[pos[0], pos[1]] = 1
                    else:
                        self.map.lights_map[pos[0], pos[1]] = 0
        elif self.ticks % 8 == 5:
            for pos in self.map.lights_positions_n + self.map.lights_positions_s + self.map.lights_positions_e + self.map.lights_positions_w:
                self.map.lights_map[pos[0], pos[1]] = 0
            self.vertical = not self.vertical
            self.horizontal = not self.horizontal

        matrix = copy.deepcopy(self.map.car_v_map)
        new_map = self.simulation.move(matrix, time)
        self.map.car_v_map_update(new_map)
        self.ticks += 1

    def update(self, delta_time, car):
        car.acceleration = Vector(0, 0)  ### to dodałem
        car.position = Vector(car.position.x + car.velocity.x * delta_time
                              + 0.5 * car.acceleration.x * pow(delta_time, 2),
                              car.position.y + car.velocity.y * delta_time
                              + 0.5 * car.acceleration.y * pow(delta_time, 2))
        car.velocity = Vector(car.velocity.x + car.acceleration.x * delta_time,
                              car.velocity.y + car.acceleration.y * delta_time)
        # self.rotate_front()
        if car.position.x >= 700:
            car.position.x = 0
        if car.position.y >= 700:
            car.position.y = 0
        if car.position.x < 0:
            car.position.x = 699
        if car.position.y < 0:
            car.position.y = 699