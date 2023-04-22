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
        self.n = [3, 11]
        self.s = [2, 10]
        self.w = [2, 10]  # zamienielem w i e
        self.e = [3, 11]
        self.__PROPABILITY = 0.2
        self.lights_positions_n = [(4, 3), (4, 11), (12, 3), (12, 11)]
        self.lights_positions_s = [(1, 2), (1, 10), (9, 2), (9, 10)]
        self.lights_positions_w = [(2, 4), (2, 12), (10, 4), (10, 12)]
        self.lights_positions_e = [(3, 1), (3, 9), (11, 1), (11, 9)]
        self.road()
        self.lights()
        self.intersections()

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

    def intersections(self):
        for pos_i in self.e + self.w:
            for pos_j in self.n + self.s:
                self.intersections_map[pos_i][pos_j] = 0

    def car_v_map_update(self, new_v_car_map):
        self.car_v_map = new_v_car_map


class Car:
    def __init__(self, direction, position):
        self.direction = direction
        self.position = Vector(position[1] * 7, position[0] * 7)  # grid size 5
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.old_v = 0  ## helping variable to move function in simulation


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

        ################ sprawdź czy nie zmienia oryginalnej macierzy

    def next_lights_distance(self, matrix, index):
        return self.next_car_distance(matrix, index)

    def next_intersection_distance(self, matrix, index):
        return self.next_car_distance(matrix, index)

    def next_lights_bool(self, matrix, index, distance):  # index of car, distance to lights
        return matrix[(index + distance + 1) % len(matrix)]  # dodałem modulo

    def deacceleration(self, matrix_car, matrix_v_car, matrix_lights, matrix_intersections, direction):
        # new_matrix = np.full((self.map.N, self.map.N), None)  # integer values
        def sprawdzam():
            if matrix_car[i].direction == MoveDirection.N:
                position_x = int(matrix_car[i].position.x / 7)  ######## grid size
                position_y = int(matrix_car[i].position.y / 7)  ######## grid size
                l = []
                for z in range(6): #na sztywno (max prędkość)
                    # print("SPRAWDZAM")
                    # print(self.map.car_v_map[(position_y + z + 1) % self.N][position_x])
                    # print(self.map.car_map[(position_y + z + 1) % self.N][position_x].direction)
                    if (self.map.car_v_map[(position_y - z - 1) % self.N][position_x] >= 0 and \
                        self.map.car_map[(position_y - z - 1) % self.N][position_x].direction == MoveDirection.E) or \
                            (self.map.car_v_map[(position_y - z - 1) % self.N][position_x] >= 0 and \
                             self.map.car_map[(position_y - z - 1) % self.N][
                                 position_x].direction == MoveDirection.W) or \
                            (self.map.car_v_map[(position_y - z - 1) % self.N][position_x - 1] >= 0 and \
                             self.map.car_map[(position_y - z - 1) % self.N][
                                 position_x - 1].direction == MoveDirection.E) or \
                            (self.map.car_v_map[(position_y - z - 1) % self.N][position_x - 1] >= 0 and \
                             self.map.car_map[(position_y - z - 1) % self.N][
                                 position_x - 1].direction == MoveDirection.W):
                        l.append(True)
                    else:
                        l.append(False)
                if any(l):
                    return True
                else:
                    return False
            elif matrix_car[i].direction == MoveDirection.S:
                position_x = int(matrix_car[i].position.x / 7)  ######## grid size
                position_y = int(matrix_car[i].position.y / 7)  ######## grid size
                l = []
                for z in range(6): #na sztywno (max prędkość)
                    # print("SPRAWDZAM")
                    # print(self.map.car_v_map[(position_y + z + 1) % self.N][position_x])
                    # print(self.map.car_map[(position_y + z + 1) % self.N][position_x].direction)
                    if (self.map.car_v_map[(position_y + z + 1) % self.N][position_x] >= 0 and \
                        self.map.car_map[(position_y + z + 1) % self.N][position_x].direction == MoveDirection.E) or \
                            (self.map.car_v_map[(position_y + z + 1) % self.N][position_x] >= 0 and \
                             self.map.car_map[(position_y + z + 1) % self.N][
                                 position_x].direction == MoveDirection.W) or \
                            (self.map.car_v_map[(position_y + z + 1) % self.N][position_x + 1] >= 0 and \
                             self.map.car_map[(position_y + z + 1) % self.N][
                                 position_x - 1].direction == MoveDirection.E) or \
                            (self.map.car_v_map[(position_y + z + 1) % self.N][position_x + 1] >= 0 and \
                             self.map.car_map[(position_y + z + 1) % self.N][position_x + 1].direction == MoveDirection.W):
                        l.append(True)
                    else:
                        l.append(False)
                if any(l):
                    return True
                else:
                    return False
            elif matrix_car[i].direction == MoveDirection.E:
                position_x = int(matrix_car[i].position.x / 7)  ######## grid size
                position_y = int(matrix_car[i].position.y / 7)  ######## grid size
                l = []
                for z in range(6): #na sztywno (max prędkość)
                    # print("SPRAWDZAM")
                    # print(self.map.car_v_map[(position_y + z + 1) % self.N][position_x])
                    # print(self.map.car_map[(position_y + z + 1) % self.N][position_x].direction)
                    if (self.map.car_v_map[(position_y) % self.N][(position_x + z + 1) % self.N] >= 0 and \
                        self.map.car_map[(position_y) % self.N][(position_x + z + 1) % self.N].direction == MoveDirection.N) or \
                            (self.map.car_v_map[(position_y) % self.N][(position_x + z + 1) % self.N] >= 0 and \
                             self.map.car_map[(position_y) % self.N][
                             (position_x + z + 1) % self.N].direction == MoveDirection.S) or \
                            (self.map.car_v_map[(position_y - 1) % self.N][(position_x + z + 1) % self.N] >= 0 and \
                             self.map.car_map[(position_y - 1) % self.N][
                             (position_x + z + 1) % self.N].direction == MoveDirection.N) or \
                            (self.map.car_v_map[(position_y - 1) % self.N][(position_x + z + 1) % self.N] >= 0 and \
                             self.map.car_map[(position_y - 1) % self.N][(position_x + z + 1) % self.N].direction == MoveDirection.S):
                        l.append(True)
                    else:
                        l.append(False)
                if any(l):
                    return True
                else:
                    return False
            elif matrix_car[i].direction == MoveDirection.W:
                position_x = int(matrix_car[i].position.x / 7)  ######## grid size
                position_y = int(matrix_car[i].position.y / 7)  ######## grid size
                l = []
                for z in range(6): #na sztywno (max prędkość)
                    # print("SPRAWDZAM")
                    # print(self.map.car_v_map[(position_y + z + 1) % self.N][position_x])
                    # print(self.map.car_map[(position_y + z + 1) % self.N][position_x].direction)
                    if (self.map.car_v_map[(position_y) % self.N][(position_x - z - 1) % self.N] >= 0 and \
                        self.map.car_map[(position_y) % self.N][(position_x - z - 1) % self.N].direction == MoveDirection.N) or \
                        (self.map.car_v_map[(position_y) % self.N][(position_x - z - 1) % self.N] >= 0 and \
                         self.map.car_map[(position_y) % self.N][(position_x - z - 1) % self.N].direction == MoveDirection.S) or \
                        (self.map.car_v_map[(position_y + 1) % self.N][(position_x - z - 1) % self.N] >= 0 and \
                         self.map.car_map[(position_y + 1) % self.N][(position_x - z - 1) % self.N].direction == MoveDirection.N) or \
                        (self.map.car_v_map[(position_y + 1) % self.N][(position_x - z - 1) % self.N] >= 0 and \
                         self.map.car_map[(position_y + 1) % self.N][(position_x - z - 1) % self.N].direction == MoveDirection.S):
                        l.append(True)
                    else:
                        l.append(False)
                if any(l):
                    return True
                else:
                    return False

        for i, v in enumerate(matrix_v_car):  # i=index, v=value
            if v >= 0 and matrix_car[i].direction == direction:  # tu zmieniłem na == z !=
                next_car = self.next_car_distance(matrix_v_car, i)
                next_lights = self.next_lights_distance(matrix_lights, i)
                next_intersection = self.next_intersection_distance(matrix_intersections, i)
                next_lights_bool = self.next_lights_bool(matrix_lights, i, next_lights)  # True = green, False = red

                if (next_lights_bool == 0) and v > min(next_car, next_lights):  # if red and v > distance to next object
                    v = min(next_car, next_lights)
                    matrix_v_car[i] = v
                elif (next_lights_bool == 1) and v > min(next_car, next_lights) and sprawdzam():
                    v = min(next_car, next_lights, v)
                    matrix_v_car[i] = v
                # dodaje
                # if matrix_car[i].direction == MoveDirection.N:
                #     position_x = int(matrix_car[i].position.x / 7)  ######## grid size
                #     position_y = int(matrix_car[i].position.y / 7)  ######## grid size
                #     # for z in range(1, v):
                #     #     if self.map.car_v_map[position_x][(position_y + z) % self.N] >= 0 and \
                #     #             self.map.car_map[position_x][(position_y + z) % self.N].direction == MoveDirection.E or \
                #     #             self.map.car_v_map[position_x][(position_y + z) % self.N] >= 0 and \
                #     #             self.map.car_map[position_x][(position_y + z) % self.N].direction == MoveDirection.W or \
                #     #             self.map.car_v_map[position_x - 1][(position_y + z) % self.N] >= 0 and \
                #     #             self.map.car_map[position_x - 1][(position_y + z) % self.N].direction == MoveDirection.E or \
                #     #             self.map.car_v_map[position_x - 2][(position_y + z) % self.N] >= 0 and \
                #     #             self.map.car_map[position_x - 2][
                #     #                 (position_y + z) % self.N].direction == MoveDirection.W:
                #     #         v = next_intersection  # TODO next_intersection
                #     #         matrix_v_car[i] = v
                #
                #     # for z in range(1, v):
                #     #     if (self.map.car_v_map[(position_y + z) % self.N][position_x] >= 0 and \
                #     #             self.map.car_map[(position_y + z) % self.N][position_x].direction == MoveDirection.E) or \
                #     #             (self.map.car_v_map[(position_y + z) % self.N][position_x] >= 0 and \
                #     #             self.map.car_map[(position_y + z) % self.N][position_x].direction == MoveDirection.W) or \
                #     #             (self.map.car_v_map[(position_y + z) % self.N][position_x - 1] >= 0 and \
                #     #             self.map.car_map[(position_y + z) % self.N][position_x - 1].direction == MoveDirection.E) or \
                #     #             (self.map.car_v_map[(position_y + z) % self.N][position_x - 1] >= 0 and \
                #     #             self.map.car_map[(position_y + z) % self.N][position_x - 1].direction == MoveDirection.W):
                #     #         v = next_intersection  # TODO next_intersection
                #     #         matrix_v_car[i] = v
                #
                #     for z in range(v):
                #         # print("SPRAWDZAM")
                #         # print(self.map.car_v_map[(position_y + z + 1) % self.N][position_x])
                #         # print(self.map.car_map[(position_y + z + 1) % self.N][position_x].direction)
                #         if (self.map.car_v_map[(position_y - z - 1) % self.N][position_x] >= 0 and \
                #             self.map.car_map[(position_y - z - 1) % self.N][position_x].direction == MoveDirection.E) or \
                #                 (self.map.car_v_map[(position_y - z - 1) % self.N][position_x] >= 0 and \
                #                  self.map.car_map[(position_y - z - 1) % self.N][position_x].direction == MoveDirection.W) or \
                #                 (self.map.car_v_map[(position_y - z - 1) % self.N][position_x - 1] >= 0 and \
                #                  self.map.car_map[(position_y - z - 1) % self.N][
                #                      position_x - 1].direction == MoveDirection.E) or \
                #                 (self.map.car_v_map[(position_y - z - 1) % self.N][position_x - 1] >= 0 and \
                #                  self.map.car_map[(position_y - z - 1) % self.N][position_x - 1].direction == MoveDirection.W):
                #             v = next_intersection
                #             print(v) # TODO coś z prędkością (za dużo czasami (pewnie odległość do następnego skrztzowania))
                #             matrix_v_car[i] = v
                else:
                    ######test
                    # if v > min(next_lights, next_car) and sprawdzam():
                    #     print("SPRAWDZAM:")
                    #     print(sprawdzam())
                    #     v = min(next_lights, next_car, v)
                    #     matrix_v_car[i] = v
                    # else: ##można usunąć
                    ######test

                    v = min(v, next_car)
                    matrix_v_car[i] = v
            else:
                pass  # velocity can't be negative or car is driving another direction

        # TODO special condition if cars on the crossroad
        # jeżeli droga zajęta i jadą w e lub w to stój


    def random_events(self, matrix_car, matrix_v_car, direction):
        for i, v in enumerate(matrix_v_car):
            if v > 0 and random.random() < self.__PROPABILITY and matrix_car[
                i].direction == direction:  # tu zmieniłem na ==
                v -= 1
                matrix_v_car[i] = v
            else:
                pass  # everything ok

    def move(self, matrix):

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

            intersections_matrix = self.map.intersections_map[:, n]
            intersections_matrix = intersections_matrix[::-1]

            # self.acceleration(car_matrix)
            self.deacceleration(car_matrix, car_v_matrix, lights_matrix, intersections_matrix, MoveDirection.N)
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
                if new_car_map[i][n] == None:  # dodałęm tą linie
                    new_car_map[i][n] = new_car_object_matrix[i]

            new_map[:, n] = new_car_matrix

        # roads with South move direction
        for s in self.map.s:
            car_matrix = [row[s] for row in self.map.car_map]

            car_v_matrix = matrix[:, s]

            lights_matrix = self.map.lights_map[:, s]

            intersections_matrix = self.map.intersections_map[:, s]

            # self.acceleration(car_matrix)
            self.deacceleration(car_matrix, car_v_matrix, lights_matrix, intersections_matrix, MoveDirection.S)
            self.random_events(car_matrix, car_v_matrix, MoveDirection.S)

            # new_car_matrix = np.full((self.map.N), -99)  # should be integer
            new_car_matrix = new_map[:, s]

            ###########################################
            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.S:
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

            intersections_matrix = self.map.intersections_map[:, e]

            # self.acceleration(car_matrix)
            self.deacceleration(car_matrix, car_v_matrix, lights_matrix, intersections_matrix, MoveDirection.E)
            self.random_events(car_matrix, car_v_matrix, MoveDirection.E)

            # new_car_matrix = np.full((self.map.N), -99)  # should be integer
            new_car_matrix = new_map[e]

            ###########################################
            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.E:
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

            intersections_matrix = self.map.intersections_map[:, w]
            intersections_matrix = intersections_matrix[::-1]

            # self.acceleration(car_matrix)
            self.deacceleration(car_matrix, car_v_matrix, lights_matrix, intersections_matrix, MoveDirection.W)
            self.random_events(car_matrix, car_v_matrix, MoveDirection.W)

            # new_car_matrix = np.full((self.map.N), -99)  # should be integer
            new_car_matrix = new_map[w]
            new_car_matrix = new_car_matrix[::-1]  # tą linie dodałem

            ###########################################
            new_car_object_matrix = [None] * self.N

            for i, v in enumerate(car_v_matrix):
                if v >= 0 and car_matrix[i].direction == MoveDirection.W:
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

        # update cars objects velocity:
        for i in range(self.N):
            for j in range(self.N):
                object = new_car_map[j][i]
                if object != None:
                    direction = object.direction
                    a = 2 * (new_map[j][i] - object.old_v * self.time) / self.time ** 2  # 2(vk - vp*t)/t^2
                    a = a * 7  ## GRID size

                    value = (new_map[j][i] * 7) / self.time

                    if direction == MoveDirection.N:
                        object.velocity = Vector(0, value)
                    if direction == MoveDirection.S:
                        object.velocity = Vector(0, -value)
                    if direction == MoveDirection.W:
                        object.velocity = Vector(-value, 0)
                    if direction == MoveDirection.E:
                        object.velocity = Vector(value, 0)

                    object.old_v = new_map[j][i]

        self.map.car_map = new_car_map
        return new_map


class Engine:
    def __init__(self, simulation, map):
        self.simulation = simulation
        self.map = map
        self.ticks = 0

    def loop(self):
        # if self.ticks % 8 == 0:
        #     if self.map.lights_map[11,9] == 1:
        #         self.map.lights_map[11,9] = 0
        #     else:
        #         self.map.lights_map[11, 9] = 1

        if self.ticks % 6 == 0:
            y = self.map.lights_positions_n + self.map.lights_positions_s
            x = self.map.lights_positions_e + self.map.lights_positions_w
            for pos in y:
                if self.map.lights_map[pos[0], pos[1]] == 1:
                    self.map.lights_map[pos[0], pos[1]] = 0
                else:
                    self.map.lights_map[pos[0], pos[1]] = 1
            for pos in x:
                if self.map.lights_map[pos[0], pos[1]] == 0:
                    self.map.lights_map[pos[0], pos[1]] = 1
                else:
                    self.map.lights_map[pos[0], pos[1]] = 0

        matrix = copy.deepcopy(self.map.car_v_map)
        new_map = self.simulation.move(matrix)
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


class Window:
    def __init__(self, engine):
        self.engine = engine
        # Ustawienia okna
        self.WINDOW_WIDTH = 700
        self.WINDOW_HEIGHT = 700
        self.FPS = 60
        self.tick = 0

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
            pygame.draw.rect(self.screen, (255, 0, 0), rect)

    def loop(self):
        # Główna pętla gry
        clock = pygame.time.Clock()
        while True:
            # Obsługa zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            delta_time = clock.tick(self.FPS) / 1000.0

            # Wypełnienie tła
            self.screen.fill((0, 0, 0))

            # Rysowanie kratki na mapie
            self.draw_grid()

            # Rysowanie obiektów
            # object_positions = [(1, 0), (0, 15), (50, 0)] # Przykładowe pozycje obiektów
            # for pos in object_positions:
            #     rect = pygame.Rect(pos[0], pos[1], self.OBJECT_SIZE, self.OBJECT_SIZE)
            #     pygame.draw.rect(self.screen, (255, 0, 0), rect)

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

            # self.draw_cars(delta_time)

            # Aktualizacja ekranu
            pygame.display.update()
            self.clock.tick(self.FPS)

            if self.tick % 60 == 0:
                self.engine.loop()

            self.tick += 1


cars = []
map = Map(100)
car = map.add_car(11, 0, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 1, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 2, MoveDirection.E)
cars.append(car)
car = map.add_car(10,2, MoveDirection.W)
cars.append(car)
car = map.add_car(10,7, MoveDirection.W)
cars.append(car)
car = map.add_car(13, 3, MoveDirection.N)
cars.append(car)

car = map.add_car(11, 3, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 4, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 5, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 6, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 7, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 8, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 9, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 10, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 11, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 12, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 13, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 14, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 15, MoveDirection.E)
cars.append(car)
car = map.add_car(11, 16, MoveDirection.E)
cars.append(car)



car = map.add_car(14, 3, MoveDirection.N)
cars.append(car)
car = map.add_car(15, 3, MoveDirection.N)
cars.append(car)
car = map.add_car(16, 3, MoveDirection.N)
cars.append(car)
car = map.add_car(17, 3, MoveDirection.N)
cars.append(car)
car = map.add_car(18, 3, MoveDirection.N)
cars.append(car)
car = map.add_car(19, 3, MoveDirection.N)
cars.append(car)


car = map.add_car(5, 3, MoveDirection.N)
cars.append(car)
car = map.add_car(6, 3, MoveDirection.N)
cars.append(car)

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
