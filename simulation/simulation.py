import random

import numpy as np
from simulation.car import Car
from simulation.direction import MoveDirection
from simulation.vector import Vector



class Simulation:
    def __init__(self, v_max, map, cars_number,lights, lights_time, time):
        self.__PROPABILITY = 0.2
        self.v_max = v_max
        self.map = map
        self.N = map.N
        self.lights = lights
        self.lights_time = lights_time
        if lights and lights_time < 5:
            raise Exception("Lights time must be greater then 4")
        if not lights:
            self.map.reset_lights_map()
        self.time = time
        self.cars = []
        self.cars_number = cars_number
        self.generate_cars()

    def generate_cars(self):
        invalid_positions = []
        valid_positions = []

        #creating invalid positions list (intersections)
        for pos_i in self.map.e + self.map.w:
            for pos_j in self.map.n + self.map.s:
                invalid_positions.append((pos_i, pos_j))

        #creating valid positions list:
        # horizontal roads
        for i in self.map.e + self.map.w:
            for j in range(self.map.N):
                pos = (i, j)
                if pos in invalid_positions:
                    pass # this position is invalid
                else:
                    valid_positions.append(pos) # this position is valid (add to the valid list)
        # vertical roads
        for j in self.map.s + self.map.n:
            for i in range(self.map.N):
                pos = (i, j)
                if pos in invalid_positions:
                    pass  # this position is invalid
                else:
                    valid_positions.append(pos)  # this position is valid (add to the valid list)

        # generating cars on the map
        for i in range(self.cars_number):
            pos = random.choice(valid_positions)
            valid_positions.remove(pos)

            # checking proper move direction
            if pos[0] in self.map.e:
                direction = MoveDirection.E
            elif pos[0] in self.map.w:
                direction = MoveDirection.W
            elif pos[1] in self.map.n:
                direction = MoveDirection.N
            else:
                direction = MoveDirection.S

            # generating car object
            car = self.map.add_car(pos[0], pos[1], direction)
            self.cars.append(car)


    def acceleration(self, matrix):
        condition = np.logical_and(matrix >= 0, matrix < self.v_max)
        matrix[condition] += 1
        # return matrix

    def next_car_distance(self, matrix, index):
        matrix = np.roll(matrix, -index)  # roll to start_index as first
        # mask of positive and negative value
        positive_mask = matrix >= 0
        negative_mask = matrix < 0

        # finding first positive value index from the index
        positive_index = (positive_mask[0 + 1:] == True).argmax()

        # counting distance between positive values
        distance = np.count_nonzero(negative_mask[positive_index:0:-1])

        if distance == 0:
            if matrix[1] >= 0:
                return 0  # distance 0
            else:
                return len(matrix)  # no other cars on the street
        else:
            return distance

    def next_lights_distance(self, matrix, index):
        return self.next_car_distance(matrix, index)

    def next_intersection_distance(self, matrix, index):
        return self.next_car_distance(matrix, index)

    def next_right_distnace(self, matrix, index):
        return self.next_car_distance(matrix, index)

    def next_left_distance(self, matrix, index):
        return self.next_car_distance(matrix, index)

    def next_lights_bool(self, matrix, index, distance):  # index of car, distance to lights
        return matrix[(index + distance + 1) % len(matrix)]  # dodałem modulo

    def deacceleration(self, matrix_car, matrix_v_car, matrix_lights, matrix_intersections, matrix_left_turn,
                       matrix_right_turn, direction):
        def can_go(car: Car):  # true if can go, false othervise

            # heliping functions

            def can_go_right():
                if car.direction == MoveDirection.N:
                    if self.map.car_v_map[i - 1][j + 1] < 0 and self.map.car_v_map[i - 1][j] < 0:
                        return True
                elif car.direction == MoveDirection.S:
                    if self.map.car_v_map[i + 1][j - 1] < 0 and self.map.car_v_map[i + 1][j] < 0:
                        return True
                elif car.direction == MoveDirection.W:
                    if self.map.car_v_map[i - 1][j - 1] < 0 and self.map.car_v_map[i][j - 1] < 0:
                        return True
                elif car.direction == MoveDirection.E:
                    if self.map.car_v_map[i + 1][j + 1] < 0 and self.map.car_v_map[i][j + 1] < 0:
                        return True
                else:
                    return False
            def can_go_streight():
                if car.direction == MoveDirection.N:
                    if self.map.car_v_map[i - 3][j] < 0 and self.map.car_v_map[i - 2][j + 1] < 0 and self.map.car_v_map[i - 1][j] < 0 and self.map.car_v_map[i - 2][j] < 0:
                        return True
                elif car.direction == MoveDirection.S:
                    if self.map.car_v_map[i + 3][j] < 0 and self.map.car_v_map[i + 2][j - 1] < 0 and self.map.car_v_map[i + 1][j] < 0 and self.map.car_v_map[i + 2][j] < 0:
                        return True
                elif car.direction == MoveDirection.W:
                    if self.map.car_v_map[i][j - 3] < 0 and self.map.car_v_map[i - 1][j - 2] < 0 and self.map.car_v_map[i][j - 1] < 0 and self.map.car_v_map[i][j - 2] < 0:
                        return True
                elif car.direction == MoveDirection.E:
                    if self.map.car_v_map[i][j + 3] < 0 and self.map.car_v_map[i + 1][j + 2] < 0 and self.map.car_v_map[i][j + 1] < 0 and self.map.car_v_map[i][j + 2] < 0:
                        return True
                else:
                    return False

            def left_check():
                if car.direction == MoveDirection.N:
                    if self.map.car_v_map[i - 3][j - 1] < 0 and self.map.car_v_map[i - 2][j - 2] < 0 and self.map.car_v_map[i - 2][j - 1] < 0:
                        return True
                elif car.direction == MoveDirection.S:
                    if self.map.car_v_map[i + 3][j + 1] < 0 and self.map.car_v_map[i + 2][j + 2] < 0 and self.map.car_v_map[i + 2][j + 1] < 0:
                        return True
                elif car.direction == MoveDirection.W:
                    if self.map.car_v_map[i + 1][j - 3] < 0 and self.map.car_v_map[i + 2][j - 2] < 0 and self.map.car_v_map[i + 1][j - 2] < 0:
                        return True
                elif car.direction == MoveDirection.E:
                    if self.map.car_v_map[i - 1][j + 3] < 0 and self.map.car_v_map[i - 2][j + 2] < 0 and self.map.car_v_map[i - 1][j + 2] < 0:
                        return True
                else:
                    return False

            # main function
            i = car.position_normal.y
            j = car.position_normal.x

            # #drawing next turn
            car.draw_next_turn()

            if car.will_turn:
                if car.will_turn_right:
                    return can_go_right()
                if car.will_turn_left:
                    return can_go_streight() and left_check()
            else:
                return can_go_streight()

        for i, v in enumerate(matrix_v_car):  # i=index, v=value
            if v >= 0 and matrix_car[i].direction == direction:
                car = matrix_car[i]
                next_car = self.next_car_distance(matrix_v_car, i)
                next_lights = self.next_lights_distance(matrix_lights, i)
                next_intersection = self.next_intersection_distance(matrix_intersections, i)
                next_lights_bool = self.next_lights_bool(matrix_lights, i, next_lights)  # True = green, False = red

                if next_intersection == 0:
                    car.can_change_direction = True
                    car.can_draw_turn = True
                    if can_go(car):
                        if car.will_turn:
                            if car.will_turn_right:
                                v = 1
                                matrix_v_car[i] = v
                                car.go = False
                            if car.will_turn_left:
                                v = 2
                                matrix_v_car[i] = v
                                car.go = False
                        else:  # go straight
                            v = 2
                            matrix_v_car[i] = v
                            car.go = False
                    else:
                        v = 0
                        matrix_v_car[i] = v
                else:
                    if next_lights_bool == False:
                        v = min(v, next_intersection, next_car, next_lights)
                        matrix_v_car[i] = v
                    else:
                        v = min(v, next_intersection, next_car)
                        matrix_v_car[i] = v

    def random_events(self, matrix_car, matrix_v_car, direction):
        for i, v in enumerate(
                matrix_v_car):  ## changed from 0 to 2 (I assume that at low speed the driver does not make mistakes, needed for intersections)
            if v > 2 and random.random() < self.__PROPABILITY and matrix_car[
                i].direction == direction:
                v -= 1
                matrix_v_car[i] = v
            else:
                pass  # everything ok

    def move(self, matrix, time):
        new_map = self.map.temp_map()
        new_car_map = [[None] * self.N for _ in range(self.N)]

        self.acceleration(matrix)

        # roads with North move direction
        for n in self.map.n:
            car_matrix = [row[n] for row in self.map.car_map]
            car_matrix = car_matrix[::-1]

            car_v_matrix = matrix[:, n]
            car_v_matrix = car_v_matrix[::-1]

            lights_matrix = self.map.lights_map[:, n]
            lights_matrix = lights_matrix[::-1]

            intersections_matrix = self.map.intersections_map_n[:, n]
            intersections_matrix = intersections_matrix[::-1]

            left_turn_matrix = self.map.left_map_n[:, n]
            left_turn_matrix = left_turn_matrix[::-1]

            right_turn_matrix = self.map.right_map_n[:, n]
            right_turn_matrix = right_turn_matrix[::-1]

            # self.acceleration(car_matrix)
            self.deacceleration(car_matrix, car_v_matrix, lights_matrix, intersections_matrix, left_turn_matrix,
                                right_turn_matrix, MoveDirection.N)
            self.random_events(car_matrix, car_v_matrix, MoveDirection.N)

            new_car_matrix = new_map[:, n]
            new_car_matrix = new_car_matrix[::-1]

            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.N:
                    new_car_matrix[(i + v) % len(car_v_matrix)] = v
                    car = car_matrix[i]
                    new_car_object_matrix[(i + v) % len(car_v_matrix)] = car

            new_car_matrix = new_car_matrix[::-1]

            new_car_object_matrix = new_car_object_matrix[::-1]
            for i in range(len(new_car_map)):
                if new_car_map[i][n] == None:
                    new_car_map[i][n] = new_car_object_matrix[i]

            new_map[:, n] = new_car_matrix

        # roads with South move direction
        for s in self.map.s:
            car_matrix = [row[s] for row in self.map.car_map]

            car_v_matrix = matrix[:, s]

            lights_matrix = self.map.lights_map[:, s]

            intersections_matrix = self.map.intersections_map_s[:, s]

            left_turn_matrix = self.map.left_map_s[:, s]

            right_turn_matrix = self.map.right_map_s[:, s]

            self.deacceleration(car_matrix, car_v_matrix, lights_matrix, intersections_matrix, left_turn_matrix,
                                right_turn_matrix, MoveDirection.S)
            self.random_events(car_matrix, car_v_matrix, MoveDirection.S)

            new_car_matrix = new_map[:, s]

            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.S:
                    new_car_matrix[(i + v) % len(car_v_matrix)] = v
                    car = car_matrix[i]
                    new_car_object_matrix[(i + v) % len(car_v_matrix)] = car

            for i in range(len(new_car_map)):
                if new_car_map[i][s] == None:
                    new_car_map[i][s] = new_car_object_matrix[i]

            new_map[:, s] = new_car_matrix

        # roads with East directions
        for e in self.map.e:
            car_matrix = self.map.car_map[e]
            car_v_matrix = matrix[e]

            lights_matrix = self.map.lights_map[e]

            intersections_matrix = self.map.intersections_map_e[e]

            left_turn_matrix = self.map.left_map_e[e]
            right_turn_matrix = self.map.right_map_e[e]

            # self.acceleration(car_matrix)
            self.deacceleration(car_matrix, car_v_matrix, lights_matrix, intersections_matrix, left_turn_matrix,
                                right_turn_matrix, MoveDirection.E)
            self.random_events(car_matrix, car_v_matrix, MoveDirection.E)

            new_car_matrix = new_map[e]

            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.E:
                    new_car_matrix[(i + v) % len(car_matrix)] = v
                    car = car_matrix[i]
                    new_car_object_matrix[(i + v) % len(car_v_matrix)] = car

            new_car_matrix = new_car_matrix
            new_car_object_matrix = new_car_object_matrix
            for i in range(len(new_car_map)):
                if new_car_map[e][i] == None:
                    new_car_map[e][i] = new_car_object_matrix[i]

            new_map[e] = new_car_matrix

        # roads with West move directions
        for w in self.map.w:

            car_matrix = self.map.car_map[w]
            car_matrix = car_matrix[::-1]

            car_v_matrix = matrix[w]
            car_v_matrix = car_v_matrix[::-1]

            lights_matrix = self.map.lights_map[w]
            lights_matrix = lights_matrix[::-1]

            intersections_matrix = self.map.intersections_map_w[w]
            intersections_matrix = intersections_matrix[::-1]

            left_turn_matrix = self.map.left_map_w[w]
            left_turn_matrix = left_turn_matrix[::-1]

            right_turn_matrix = self.map.right_map_w[w]
            right_turn_matrix = right_turn_matrix[::-1]

            # self.acceleration(car_matrix)
            self.deacceleration(car_matrix, car_v_matrix, lights_matrix, intersections_matrix, left_turn_matrix,
                                right_turn_matrix, MoveDirection.W)
            self.random_events(car_matrix, car_v_matrix, MoveDirection.W)

            new_car_matrix = new_map[w]
            new_car_matrix = new_car_matrix[::-1]

            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.W:
                    new_car_matrix[(i + v) % len(car_matrix)] = v
                    car = car_matrix[i]
                    new_car_object_matrix[(i + v) % len(car_v_matrix)] = car

            new_car_matrix = new_car_matrix[::-1]
            new_car_object_matrix = new_car_object_matrix[::-1]
            for i in range(len(new_car_map)):
                if new_car_map[w][i] == None:
                    new_car_map[w][i] = new_car_object_matrix[i]

            new_map[w] = new_car_matrix

        # #handling possible intersections jam
        # for intersection in self.map.intersections:
        #     intersection.check_jam(cars_v_matrix=new_map, cars_object_matrix=new_car_map)

        # update cars objects velocity:
        for i in range(self.N):
            for j in range(self.N):
                object = new_car_map[j][i]
                if object != None:
                    object.position_normal.x = i
                    object.position_normal.y = j
                    direction = object.direction

                    value = (new_map[j][i] * 7) / time

                    if direction == MoveDirection.N:
                        object.velocity = Vector(0, -value)
                    if direction == MoveDirection.S:
                        object.velocity = Vector(0, value)
                    if direction == MoveDirection.W:
                        object.velocity = Vector(-value, 0)
                    if direction == MoveDirection.E:
                        object.velocity = Vector(value, 0)

                    object.old_v = new_map[j][i]

                    # update odometer
                    object.odometer += object.old_v

        # update direction for cars which turning
        for pos_i in self.map.e + self.map.w:
            for pos_j in self.map.n + self.map.s:

                object = new_car_map[pos_i][pos_j]
                if object != None:
                    if object.can_change_direction:
                        if object.will_turn:
                            direction = object.direction

                            if object.will_turn_right:
                                if direction == MoveDirection.N and pos_i in self.map.e:
                                    object.direction = MoveDirection.E
                                    object.can_change_direction = False
                                elif direction == MoveDirection.S and pos_i in self.map.w:
                                    object.direction = MoveDirection.W
                                    object.can_change_direction = False
                                elif direction == MoveDirection.W and pos_j in self.map.n:
                                    object.direction = MoveDirection.N
                                    object.can_change_direction = False
                                elif direction == MoveDirection.E and pos_j in self.map.s:
                                    object.direction = MoveDirection.S
                                    object.can_change_direction = False

                            if object.will_turn_left:
                                if direction == MoveDirection.N and pos_i in self.map.w:
                                    object.direction = MoveDirection.W
                                    object.can_change_direction = False
                                elif direction == MoveDirection.S and pos_i in self.map.e:
                                    object.direction = MoveDirection.E
                                    object.can_change_direction = False
                                elif direction == MoveDirection.W and pos_j in self.map.s:
                                    object.direction = MoveDirection.S
                                    object.can_change_direction = False
                                elif direction == MoveDirection.E and pos_j in self.map.n:
                                    object.direction = MoveDirection.N
                                    object.can_change_direction = False
                    object.can_change_direction = False

        self.map.car_map = new_car_map
        return new_map