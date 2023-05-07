import numpy as np

from traffic_simulation.car import Car
from traffic_simulation.intersection import Intersection


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
        self.n = [21, 51, 81]
        self.s = [20, 50, 80]
        self.w = [20, 50, 80]  # zamienielem w i e
        self.e = [21, 51, 81]
        # self.n = [50]
        # self.s = [49]
        # self.w = [49]  # zamienielem w i e
        # self.e = [50]
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
                self.intersections.append(Intersection(id, (pos_i, pos_j), self))
                id += 1

    def car_v_map_update(self, new_v_car_map):
        self.car_v_map = new_v_car_map