import random
import numpy as np
import copy
import sys

import pygame

from traffic_simulation.direction import MoveDirection


class Map:
    def __init__(self, N):
        self.nothing_cell = -100
        self.road_cell = -99
        self.N = N
        self.car_v_map = np.full((self.N, self.N), self.nothing_cell)  # must be int value (to proper acceleration)
        self.car_map = [[None] * self.N for _ in range(self.N)]
        self.road_map = np.full((self.N, self.N), self.nothing_cell)  # must be int value (to proper acceleration)
        self.lights_map = np.full((self.N, self.N), self.nothing_cell)  # must be int value (to proper acceleration)
        self.intersections_map = np.full((self.N, self.N), self.nothing_cell)
        self.left_map_n = np.full((self.N, self.N), self.nothing_cell)
        self.right_map_n = np.full((self.N, self.N), self.nothing_cell)
        self.left_map_s = np.full((self.N, self.N), self.nothing_cell)
        self.right_map_s = np.full((self.N, self.N), self.nothing_cell)
        self.left_map_w = np.full((self.N, self.N), self.nothing_cell)
        self.right_map_w = np.full((self.N, self.N), self.nothing_cell)
        self.left_map_e = np.full((self.N, self.N), self.nothing_cell)
        self.right_map_e = np.full((self.N, self.N), self.nothing_cell)
        self.n = [3, 11]
        self.s = [2, 10]
        self.w = [2, 10]  # zamienielem w i e
        self.e = [3, 11]
        self.__PROPABILITY = 0.2
        self.lights_positions_n = [(4, 3), (4, 11), (12, 3), (12, 11)]
        self.lights_positions_s = [(1, 2), (1, 10), (9, 2), (9, 10)]
        self.lights_positions_w = [(2, 4), (2, 12), (10, 4), (10, 12)]
        self.lights_positions_e = [(3, 1), (3, 9), (11, 1), (11, 9)]
        self.intersections = []
        self.intersections_map_n = np.full((self.N, self.N), self.nothing_cell)
        self.intersections_map_s = np.full((self.N, self.N), self.nothing_cell)
        self.intersections_map_w = np.full((self.N, self.N), self.nothing_cell)
        self.intersections_map_e = np.full((self.N, self.N), self.nothing_cell)
        self.road()
        self.lights()
        self.intersections_maps()
        self.intersections_objects()
        self.turns()

    def temp_map(self):
        x_list = self.w + self.e
        y_list = self.n + self.s
        temp = np.full((self.N, self.N), self.nothing_cell)  # should be integers
        temp[x_list, :] = self.road_cell
        temp[:, y_list] = self.road_cell
        return temp

    def add_car(self, x, y, direction):
        car = Car(direction, (x, y))
        self.car_map[x][y] = car
        self.car_v_map[x][y] = 0
        return car

    def update_map(self, temp):
        self.car_map = temp.map

    def road(self):
        x_list = self.w + self.e
        y_list = self.n + self.s
        self.road_map[x_list, :] = self.road_cell
        self.road_map[:, y_list] = self.road_cell

    def turns(self):
        # for n directions
        left_n = self.w
        left_n = [x - 1 for x in left_n]
        right_n = self.e
        right_n = [x - 1 for x in right_n]
        self.left_map_n[left_n, :] = 0
        self.right_map_n[right_n, :] = 0

        # for s directions
        left_s = self.e
        left_s = [x + 1 for x in left_s]
        right_s = self.w
        right_s = [x + 1 for x in right_s]
        self.left_map_s[left_s, :] = 0
        self.right_map_s[right_s, :] = 0

        # for e directions
        left_e = self.n
        left_e = [x + 1 for x in left_e]
        right_e = self.s
        right_e = [x + 1 for x in right_e]
        self.left_map_e[:, left_e] = 0
        self.right_map_e[:, right_e] = 0

        # for w directions
        left_w = self.s
        left_w = [x - 1 for x in left_w]
        right_w = self.n
        right_w = [x - 1 for x in right_w]
        self.left_map_w[:, left_w] = 0
        self.right_map_w[:, right_w] = 0

    def lights(self):
        # lights_positions_n = [(4,3), (4,11), (12,3), (12,11)]
        # lights_positions_s = [(1,2), (1,10), (9,2), (9,10)]
        # lights_positions_w = [(2,4), (2,12), (10,4), (10,12)]
        # lights_positions_e = [(3,1), (3,9), (11,1), (11,9)]
        for pos in self.lights_positions_s + self.lights_positions_n:
            self.lights_map[pos[0], pos[1]] = 0

        for pos in self.lights_positions_w + self.lights_positions_e:
            self.lights_map[pos[0], pos[1]] = 1

        # self.lights_map[11, 99] = 0

    def intersections_maps(self):
        # for pos_i in self.e + self.w:
        #     for pos_j in self.n + self.s:
        #         self.intersections_map[pos_i][pos_j] = 0
        # for n directions roads
        for pos_i in self.e:
            for pos_j in self.n:
                self.intersections_map_n[pos_i][pos_j] = 0
        # for s directions roads
        for pos_i in self.w:
            for pos_j in self.s:
                self.intersections_map_s[pos_i][pos_j] = 0
        # for e directions roads
        for pos_i in self.e:
            for pos_j in self.s:
                self.intersections_map_w[pos_j][pos_i] = 0
        # for w directions roads
        for pos_i in self.w:
            for pos_j in self.n:
                self.intersections_map_e[pos_j][pos_i] = 0

    def intersections_objects(self):
        id = 1
        for pos_i in self.e:
            for pos_j in self.s:
                self.intersections.append(Intersection(id, (pos_i, pos_j)))
                id += 1

    def car_v_map_update(self, new_v_car_map):
        self.car_v_map = new_v_car_map


class Intersection:
    def __init__(self, id, position):
        self.id = id
        self.position = Vector(position[1], position[0])



    def check_jam(self, cars_v_matrix, cars_object_matrix): #function return position and v (to change v_matrix) of random choice car to solve jam
        print("HELLO")
        cars = []
        standing_cars = []

        i = self.position.y
        j = self.position.x

        print(i, j)

        car1 = cars_object_matrix[i][j - 1]
        if car1 != None:
            cars.append(car1)
        car2 = cars_object_matrix[i + 1][j + 1]
        if car2 != None:
            cars.append(car2)
        car3 = cars_object_matrix[i - 1][j + 2]
        if car3 != None:
            cars.append(car3)
        car4 = cars_object_matrix[i - 2][j]
        if car4 != None:
            cars.append(car4)

        for car in cars:
            print("XD")
            if cars_v_matrix[car.position_normal.y][car.position_normal.x] == 0:
                print("Działa")
                standing_cars.append(False)

        if len(cars) == len(standing_cars) and len(cars) > 0:  # their is a jam
            print(len(cars))
            print(len(standing_cars))
            random_car = random.choice(cars)
            random_car.go = True
            # v = 0
            # if random_car.will_turn:
            #     if random_car.will_turn_right:
            #         v = 1
            #     elif random_car.will_turn_left:
            #         v = 2
            # else:
            #     v = 2



class Car:
    def __init__(self, direction, position):
        self.direction = direction
        self.position = Vector(position[1] * 7, position[0] * 7)  # grid size 5
        self.position_normal = Vector(position[1], position[0])
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.old_v = 0  ## helping variable to move function in simulation
        self.will_turn = False
        self.will_turn_right = False
        self.will_turn_left = False
        self.go = False
        self.WILL_TURN_PROPABILITY = 0.5
        self.WILL_TURN_RIGHT_PROPABILITY = 0.7
        self.draw_next_turn()
        color_r = random.randint(50, 200)
        color_g = random.randint(50, 200)
        color_b = random.randint(50, 200)
        self.color = (color_r, color_g, color_b)

    def draw_next_turn(self):
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
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Simulation:
    def __init__(self, v_max, map, cars, time):
        self.__PROPABILITY = 0.2
        self.v_max = v_max
        self.map = map
        self.N = map.N
        self.time = time
        self.cars = cars

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

            # heliping finctions
            def can_go_streight():
                if car.direction == MoveDirection.N:
                    if map.car_v_map[i - 3][j] < 0 and map.car_v_map[i - 2][j + 1] < 0:
                        print(map.car_v_map[i - 3][j])
                        print(map.car_v_map[i - 2][j + 1])
                        return True
                elif car.direction == MoveDirection.S:
                    if map.car_v_map[i + 3][j] < 0 and map.car_v_map[i + 2][j - 1] < 0:
                        return True
                elif car.direction == MoveDirection.W:
                    if map.car_v_map[i][j - 3] < 0 and map.car_v_map[i - 1][j - 2] < 0:
                        return True
                elif car.direction == MoveDirection.E:
                    if map.car_v_map[i][j + 3] < 0 and map.car_v_map[i + 1][j + 2] < 0:
                        return True
                else:
                    return False

            def left_check():  # i - wiersze, j-kolumny
                if car.direction == MoveDirection.N:
                    if map.car_v_map[i - 3][j - 1] < 0 and map.car_v_map[i - 2][j - 2] < 0:
                        return True
                elif car.direction == MoveDirection.S:
                    if map.car_v_map[i + 3][j + 1] < 0 and map.car_v_map[i + 2][j + 2] < 0:
                        return True
                elif car.direction == MoveDirection.W:
                    if map.car_v_map[i + 1][j - 3] < 0 and map.car_v_map[i + 2][j - 2] < 0:
                        return True
                elif car.direction == MoveDirection.E:
                    if map.car_v_map[i - 1][j + 3] < 0 and map.car_v_map[i - 2][j + 2] < 0:
                        return True
                else:
                    return False

            # main function
            i = car.position_normal.y
            j = car.position_normal.x

            print(f"i={i}, j={j}")

            if car.will_turn:
                if car.will_turn_right:
                    return True
                if car.will_turn_left:
                    return can_go_streight() and left_check()

            else:
                return can_go_streight()

        for i, v in enumerate(matrix_v_car):  # i=index, v=value
            if v >= 0 and matrix_car[i].direction == direction:  # tu zmieniłem na == z !=
                car = matrix_car[i]
                next_car = self.next_car_distance(matrix_v_car, i)
                next_lights = self.next_lights_distance(matrix_lights, i)
                next_intersection = self.next_intersection_distance(matrix_intersections, i)
                next_lights_bool = self.next_lights_bool(matrix_lights, i, next_lights)  # True = green, False = red
                next_right = self.next_right_distnace(matrix_right_turn, i)
                next_left = self.next_left_distance(matrix_left_turn, i)

                if next_intersection == 0:
                    if can_go(car) or car.go:
                        print("CO KOLWIEK")
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
                matrix_v_car):  ## zmieniłem z 0 na 2 (zakładam że przy niskiej prędkości kierowca nie popełnia błędów, potrzebne do skrzyżowań)
            if v > 2 and random.random() < self.__PROPABILITY and matrix_car[
                i].direction == direction:  # tu zmieniłem na ==
                v -= 1
                matrix_v_car[i] = v
            else:
                pass  # everything ok



    def move(self, matrix, time):
        print(f"PRZED: {len(matrix[matrix >= 0])}")
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

            # new_car_matrix = np.full((self.map.N), -99)
            new_car_matrix = new_map[:, n]
            new_car_matrix = new_car_matrix[::-1]

            ###########################################
            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.N:
                    new_car_matrix[(i + v) % len(car_v_matrix)] = v
                    #########################################
                    car = car_matrix[i]
                    new_car_object_matrix[(i + v) % len(car_v_matrix)] = car

            new_car_matrix = new_car_matrix[::-1]

            #############################################
            new_car_object_matrix = new_car_object_matrix[::-1]
            for i in range(len(new_car_map)):
                if new_car_map[i][n] == None:  # dodałem tą linie
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

            # self.acceleration(car_matrix)
            self.deacceleration(car_matrix, car_v_matrix, lights_matrix, intersections_matrix, left_turn_matrix,
                                right_turn_matrix, MoveDirection.S)
            self.random_events(car_matrix, car_v_matrix, MoveDirection.S)

            # new_car_matrix = np.full((self.map.N), -99)  # should be integer
            new_car_matrix = new_map[:, s]

            ###########################################
            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.S:
                    if new_car_matrix[(i + v) % len(car_matrix)] >= 0:
                        print(
                            f"OLD Car position: {car_matrix[i].position_normal.y, car_matrix[i].position_normal.x}, {car_matrix[i].direction}")
                        print(
                            f"NEW CAr position: {new_car_object_matrix[i].position_normal.y, new_car_object_matrix[i].position_normal.x}, {new_car_object_matrix[i].direction}")
                        print("S")
                        print(i)
                        print(f"V: {v}")
                        print("KOLIZJA")
                    new_car_matrix[(i + v) % len(car_v_matrix)] = v
                    #########################################
                    car = car_matrix[i]
                    new_car_object_matrix[(i + v) % len(car_v_matrix)] = car

            #############################################
            for i in range(len(new_car_map)):
                if new_car_map[i][s] == None:  # dodałęm tą linie
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

            # new_car_matrix = np.full((self.map.N), -99)  # should be integer
            new_car_matrix = new_map[e]

            ###########################################
            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.E:
                    if new_car_matrix[(i + v) % len(car_matrix)] >= 0:
                        print(
                            f"OLD Car position: {car_matrix[i].position_normal.y, car_matrix[i].position_normal.x}, {car_matrix[i].direction}")
                        print(
                            f"NEW CAr position: {new_car_object_matrix[i].position_normal.y, new_car_object_matrix[i].position_normal.x}, {new_car_object_matrix[i].direction}")
                        print("E")
                        print(i)
                        print(f"V: {v}")
                        print("KOLIZJA")
                    new_car_matrix[(i + v) % len(car_matrix)] = v
                    #########################################
                    car = car_matrix[i]
                    new_car_object_matrix[(i + v) % len(car_v_matrix)] = car

            new_car_matrix = new_car_matrix  # tu usunąłem reverse
            #############################################
            new_car_object_matrix = new_car_object_matrix
            for i in range(len(new_car_map)):
                if new_car_map[e][i] == None:  # dodałęm tą linie
                    new_car_map[e][i] = new_car_object_matrix[i]  # zamieniłem e i

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

            # new_car_matrix = np.full((self.map.N), -99)  # should be integer
            new_car_matrix = new_map[w]
            new_car_matrix = new_car_matrix[::-1]  # tą linie dodałem

            ###########################################
            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.W:
                    if new_car_matrix[(i + v) % len(car_matrix)] >= 0:
                        print(
                            f"OLD Car position: {car_matrix[i].position_normal.y, car_matrix[i].position_normal.x}, {car_matrix[i].direction}")
                        print(
                            f"NEW CAr position: {new_car_object_matrix[i].position_normal.y, new_car_object_matrix[i].position_normal.x}, {new_car_object_matrix[i].direction}")
                        print("W")
                        print(i)
                        print(f"V: {v}")
                        print("KOLIZJA")
                    new_car_matrix[(i + v) % len(car_matrix)] = v
                    #########################################
                    car = car_matrix[i]
                    new_car_object_matrix[(i + v) % len(car_v_matrix)] = car

            new_car_matrix = new_car_matrix[::-1]
            #############################################
            new_car_object_matrix = new_car_object_matrix[::-1]
            for i in range(len(new_car_map)):
                if new_car_map[w][i] == None:  # dodałęm tą linie
                    new_car_map[w][i] = new_car_object_matrix[i]  # zamieniełem w i

            new_map[w] = new_car_matrix

        #handling posible intersections jam
        for intersection in self.map.intersections:
            intersection.check_jam(cars_v_matrix=new_map, cars_object_matrix=new_car_map)

        # update cars objects velocity:
        for i in range(self.N):
            for j in range(self.N):
                object = new_car_map[j][i]
                if object != None:
                    object.position_normal.x = i
                    object.position_normal.y = j
                    direction = object.direction
                    # a = 2 * (new_map[j][i] - object.old_v * self.time) / self.time ** 2  # 2(vk - vp*t)/t^2
                    # a = a * 7  ## GRID size

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

        # update direction for cars which turning
        for pos_i in self.map.e + self.map.w:
            for pos_j in self.map.n + self.map.s:
                # self.intersections_map[pos_i][pos_j] = 0

                object = new_car_map[pos_i][pos_j]
                if object != None:
                    if object.will_turn:
                        direction = object.direction

                        if object.will_turn_right:
                            if direction == MoveDirection.N and pos_i in self.map.e:
                                object.direction = MoveDirection.E
                            elif direction == MoveDirection.S and pos_i in self.map.w:
                                object.direction = MoveDirection.W
                            elif direction == MoveDirection.W and pos_j in self.map.n:
                                object.direction = MoveDirection.N
                            elif direction == MoveDirection.E and pos_j in self.map.s:
                                object.direction = MoveDirection.S

                        if object.will_turn_left:
                            if direction == MoveDirection.N and pos_i in self.map.w:
                                object.direction = MoveDirection.W
                            elif direction == MoveDirection.S and pos_i in self.map.e:
                                object.direction = MoveDirection.E
                            elif direction == MoveDirection.W and pos_j in self.map.s:
                                object.direction = MoveDirection.S
                            elif direction == MoveDirection.E and pos_j in self.map.n:
                                object.direction = MoveDirection.N
                    #drawing next turn for a car
                    object.draw_next_turn()

        self.map.car_map = new_car_map
        print(f"PO: {len(new_map[new_map >= 0])}")
        return new_map


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
        # print("##################################################################")
        # print("NEW TICK")
        # print(len(self.simulation.cars))
        # for car in self.simulation.cars:
        #     print(f"({car.position.x / 7}, {car.position.y / 7})")

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


class Window:
    def __init__(self, engine):
        self.engine = engine
        # Ustawienia okna
        self.WINDOW_WIDTH = 700
        self.WINDOW_HEIGHT = 700
        self.FPS = 60
        self.tick = 0
        self.update_time = 0

        # Ustawienia mapy
        self.GRID_SIZE = 7
        self.GRID_WIDTH = 100  ##WINDOW_WIDTH // GRID_SIZE
        self.GRID_HEIGHT = 100  ##WINDOW_HEIGHT // GRID_SIZE

        # Ustawienia obiektów
        self.OBJECT_SIZE = 5

        # Inicjalizacja Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

    # Funkcja rysująca kratki na mapie
    def draw_grid(self):
        for x in range(0, self.WINDOW_WIDTH, self.GRID_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, self.WINDOW_HEIGHT))
        for y in range(0, self.WINDOW_HEIGHT, self.GRID_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255), (0, y), (self.WINDOW_WIDTH, y))

    def draw_cars(self, delta_time):
        cars = self.engine.simulation.cars

        for car in cars:
            self.engine.update(delta_time, car)
            rect = pygame.Rect(car.position.x, car.position.y, self.OBJECT_SIZE, self.OBJECT_SIZE)  ##*10
            pygame.draw.rect(self.screen, car.color, rect)

    def draw_roads(self):
        for i in range(self.engine.map.N):
            for j in range(self.engine.map.N):
                if self.engine.map.road_map[i][j] == -99:
                    rect = pygame.Rect(j * 7, i * 7, 7, 7)  ##*10
                    pygame.draw.rect(self.screen, (200, 200, 200), rect)
                if self.engine.map.lights_map[i][j] == 1:
                    rect = pygame.Rect(j * 7, i * 7, 7, 7)  ##*10
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)
                if self.engine.map.lights_map[i][j] == 0:
                    rect = pygame.Rect(j * 7, i * 7, 7, 7)  ##*10
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)
                if self.engine.map.car_v_map[i][j] >= 0:
                    rect = pygame.Rect(j * 7, i * 7, 7, 7)  ##*10
                    pygame.draw.rect(self.screen, (0, 0, 255), rect)

    def loop(self):
        # Główna pętla gry
        clock = pygame.time.Clock()
        while True:
            self.tick += 1
            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            delta_time = clock.tick(self.FPS) / 1000.0

            # Wypełnienie tła
            self.screen.fill((0, 0, 0))

            # Rysowanie kratki na mapie

            # self.draw_grid()
            # Rysowanie obiektów
            # object_positions = [(1, 0), (0, 15), (50, 0)] # Przykładowe pozycje obiektów
            # for pos in object_positions:
            #     rect = pygame.Rect(pos[0], pos[1], self.OBJECT_SIZE, self.OBJECT_SIZE)
            #     pygame.draw.rect(self.screen, (255, 0, 0), rect)

            self.draw_roads()

            self.draw_cars(delta_time)

            # Aktualizacja ekranu
            pygame.display.update()
            self.clock.tick(self.FPS)
            self.update_time += delta_time

            if self.tick % 60 == 0:
                self.engine.loop(self.update_time)
                self.update_time = 0


cars = []
map = Map(100)
car = map.add_car(11, 1, MoveDirection.E)
cars.append(car)
car = map.add_car(10, 4, MoveDirection.W)
cars.append(car)
car = map.add_car(12, 3, MoveDirection.N)
cars.append(car)
car = map.add_car(9, 2, MoveDirection.S)
cars.append(car)

# car = map.add_car(13, 3, MoveDirection.N)
# cars.append(car)
# car = map.add_car(14, 3, MoveDirection.N)
# cars.append(car)
# car = map.add_car(15, 3, MoveDirection.N)
# cars.append(car)

# car = map.add_car(11, 1, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 2, MoveDirection.E)
# cars.append(car)
# car = map.add_car(10, 2, MoveDirection.W)
# cars.append(car)
# car = map.add_car(11, 6, MoveDirection.W)
# cars.append(car)
# car = map.add_car(13, 5, MoveDirection.N)
# cars.append(car)
# #
# car = map.add_car(11, 3, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 4, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 5, MoveDirection.E)
# cars.append(car)
#
# car = map.add_car(11, 6, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 7, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 8, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 9, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 10, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 11, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 12, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 13, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 14, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 15, MoveDirection.E)
# cars.append(car)
# car = map.add_car(11, 16, MoveDirection.E)
# cars.append(car)
#
# car = map.add_car(14, 3, MoveDirection.N)
# cars.append(car)
# car = map.add_car(15, 3, MoveDirection.N)
# cars.append(car)
# car = map.add_car(16, 3, MoveDirection.N)
# cars.append(car)
# car = map.add_car(17, 3, MoveDirection.N)
# cars.append(car)
# car = map.add_car(18, 3, MoveDirection.N)
# cars.append(car)
# car = map.add_car(19, 3, MoveDirection.N)
# cars.append(car)
#
# car = map.add_car(5, 3, MoveDirection.N)
# cars.append(car)

# TODO car position nie jest aktualizowane ( niektóre funkcje się na tym opierają ) najlepiej ctr+f positon.x, position.y
# TODO zmiana kierunków popraw

simulation = Simulation(6, map, cars, 1)
engine = Engine(simulation, map)
window = Window(engine)
window.loop()

# simulation = Simulation(6, map, cars, 1)
# engine = Engine(simulation, map)
# engine.loop()
# engine.loop()
# engine.loop()
# engine.loop()
# engine.loop()
# engine.loop()
# engine.loop()
# engine.loop()
# engine.loop()
# engine.loop()
# engine.loop()
# engine.loop()
# engine.loop()


# matrix = copy.deepcopy(map.car_v_map)
# new_map = simulation.move(matrix)
# map.car_v_map_update(new_map)
# print(new_map)
# print("")
# print("")
# print(map.car_map)
# # print('')
# # print('')
# # print(map.car_v_map)
# # print('')
# # print('')
#
#
# matrix = copy.deepcopy(map.car_v_map)
# # print(map.car_map)
# new_map = simulation.move(matrix)
# map.car_v_map_update(new_map)
# print(new_map)
# print("")
# print("")
#
# matrix = copy.deepcopy(map.car_v_map)
# # print(map.car_map)
# new_map = simulation.move(matrix)
# map.car_v_map_update(new_map)
# print(new_map)
# print("")
# print("")
#
# matrix = copy.deepcopy(map.car_v_map)
# # print(map.car_map)
# new_map = simulation.move(matrix)
# map.car_v_map_update(new_map)
# print(new_map)
# print("")
# print("")
#
# matrix = copy.deepcopy(map.car_v_map)
# # print(map.car_map)
# new_map = simulation.move(matrix)
# map.car_v_map_update(new_map)
# print(new_map)
# print("")
# print("")
#
# matrix = copy.deepcopy(map.car_v_map)
# # print(map.car_map)
# new_map = simulation.move(matrix)
# map.car_v_map_update(new_map)
# print(new_map)
# print("")
# print("")
#
# matrix = copy.deepcopy(map.car_v_map)
# # print(map.car_map)
# new_map = simulation.move(matrix)
# map.car_v_map_update(new_map)
# print(new_map)
# print("")
# print("")
#
# matrix = copy.deepcopy(map.car_v_map)
# # print(map.car_map)
# new_map = simulation.move(matrix)
# map.car_v_map_update(new_map)
# print(new_map)
# print("")
# print("")


# test = Simulation(5)
# x = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [-1, -2, -10, False]])
# # x = test.acceleration(x)
# print(x)
# print(x[1])
# # print(x[:,2][::-1])
# # y = np.full((10), None)
# # y[10] = 3
#
# print(12 % 12)


#
# map = Map(15)
# map.road()
# map.print_map()
# x = map.map[:, 2]
# x[:] = "ZMIANA"
# map.map[:, 2] = x
# map.print_map()
# temp = Map(10)
# map.print_map()
# temp.add_car(0,0)
# map.print_map()
# temp.print_map()
# map.update_map(temp)
# map.print_map()


# # Set up the road
# n = 100 # Number of cells
# m = 10 # Number of vehicles
# road = np.zeros(n)
# road[20] = 1 # Add a vehicle at cell 20
#
# # Set the model parameters
# vmax = 5 # Maximum speed
# p = 0.3 # Randomization probability
# L = 5 # Length of sight
#
# # Run the simulation for t time steps
# t = 100
# for k in range(t):
#     # Add a new vehicle after 50 time steps
#     if k == 50:
#         road[30] = 1
#
#     # Acceleration, deceleration, randomization, and movement rules go here
#
