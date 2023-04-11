import random
import numpy as np


class Map:
    def __init__(self, N):
        self.nothing_cell = -100
        self.road_cell = -99
        self.N = N
        self.car_map = np.full((self.N, self.N), self.nothing_cell)  # must be int value (to proper acceleration)
        self.road_map = np.full((self.N, self.N), self.nothing_cell)  # must be int value (to proper acceleration)
        self.lights_map = np.full((self.N, self.N), self.nothing_cell)  # must be int value (to proper acceleration)
        self.n = [3, 11]
        self.s = [2, 10]
        self.w = [3, 11]
        self.e = [2, 10]
        self.__PROPABILITY = 0.2
        self.road()
        self.lights()

    # def print_map(self):
    #     print(self.map)

    def temp_map(self):
        return np.full((self.N, self.N), self.nothing_cell)  # should be integers

    def add_car(self, x, y):
        self.car_map[x][y] = 0

    def update_map(self, temp):
        self.car_map = temp.map

    def road(self):
        x_list = self.w + self.e
        y_list = self.n + self.s
        self.road_map[x_list, :] = self.road_cell
        self.road_map[:, y_list] = self.road_cell

    def lights(self):
        positions_n = [(4,3), (4,11), (12,3), (12,11)]
        positions_s = [(1,2), (1,10), (9,2), (9,10)]
        positions_w = [(2,4), (2,12), (10,4), (10,12)]
        positions_e = [(3,1), (3,9), (11,1), (11,9)]
        for pos in positions_s + positions_n + positions_w + positions_e:
            self.lights_map[pos[0], pos[1]] = 1

    def car_map_update(self, new_car_map):
        self.car_map = new_car_map

class Simulation:
    def __init__(self, v_max, map):
        self.__PROPABILITY = 0.2
        self.v_max = v_max
        self.map = map

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

    def next_lights_bool(self, matrix, index, distance):  # index of car, distance to lights
        return matrix[index + distance + 1]

    def deacceleration(self, matrix_car, matrix_lights):
        # new_matrix = np.full((self.map.N, self.map.N), None)  # integer values

        for i, v in enumerate(matrix_car):  # i=index, v=value
            if v >= 0:
                next_car = self.next_car_distance(matrix_car, i)
                next_lights = self.next_lights_distance(matrix_lights, i)
                next_lights_bool = self.next_lights_bool(matrix_lights, i, next_lights)  # True = green, False = red

                if not next_lights_bool and v > min(next_car, next_lights):  # if red and v > distance to next object
                    v = min(next_car, next_lights)
                else:
                    v = min(v, next_car)
            else:
                pass  # velocity can't be negative

        # TODO special condition if cars on the crossroad
        # to v zmiemieniaj do nowej listy ?

    def random_events(self, matrix):
        for i, v in enumerate(matrix):
            if v > 0 and random.random() < self.__PROPABILITY:
                v -= 1
            else:
                pass  # everything ok

    def move(self, map:Map):
        new_map = map.temp_map()

        # roads with North move direction
        for n in map.n:
            car_matrix = map.car_map[:, n]
            car_matrix = car_matrix[::-1]

            lights_matrix = map.lights_map[:, n]
            lights_matrix = lights_matrix[::-1]
        
            self.acceleration(car_matrix)
            self.deacceleration(car_matrix, lights_matrix)
            self.random_events(car_matrix)

            new_car_matrix = np.full((self.map.N), -99)

            for i, v in enumerate(car_matrix):
                if v >= 0:
                    new_car_matrix[(i + v) % len(car_matrix)] = v

            new_car_matrix = new_car_matrix[::-1]

            new_map[:, n] = new_car_matrix

        # roads with South move direction
        for s in map.s:
            car_matrix = map.car_map[:, s]

            lights_matrix = map.lights_map[:, s]

            self.acceleration(car_matrix)
            self.deacceleration(car_matrix, lights_matrix)
            self.random_events(car_matrix)

            new_car_matrix = np.full((self.map.N), -99)  # should be integer

            for i, v in enumerate(car_matrix):
                if v >= 0:
                    new_car_matrix[(i + v) % len(car_matrix)] = v

            new_car_matrix = new_car_matrix[::-1]

            new_map[:, s] = new_car_matrix

        # roads with East directions
        for e in map.e:
            car_matrix = map.car_map[e]

            lights_matrix = map.lights_map[e]

            self.acceleration(car_matrix)
            self.deacceleration(car_matrix, lights_matrix)
            self.random_events(car_matrix)

            new_car_matrix = np.full((self.map.N), -99)  # should be integer

            for i, v in enumerate(car_matrix):
                if v >= 0:
                    new_car_matrix[(i + v) % len(car_matrix)] = v

            new_car_matrix = new_car_matrix[::-1]

            new_map[e] = new_car_matrix

        # roads with West move directions
        for w in map.w:
            car_matrix = map.car_map[w]
            car_matrix = car_matrix[::-1]

            lights_matrix = map.lights_map[w]
            lights_matrix = lights_matrix[::-1]

            self.acceleration(car_matrix)
            self.deacceleration(car_matrix, lights_matrix)
            self.random_events(car_matrix)

            new_car_matrix = np.full((self.map.N), -99)  # should be integer

            for i, v in enumerate(car_matrix):
                if v >= 0:
                    new_car_matrix[(i + v) % len(car_matrix)] = v

            new_car_matrix = new_car_matrix[::-1]

            new_map[w] = new_car_matrix

        return new_map





map = Map(15)
map.add_car(14,3)
simulation = Simulation(6, map)
new_map = simulation.move(map)
map.car_map_update(new_map)
print(new_map)
print('')
print('')
print(map.car_map)
print('')
print('')
new_map = simulation.move(map)
map.car_map_update(new_map)
print(map.car_map)
print('')
print('')



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
#     # Print the state of the road
#     print(''.join('.' if x==0 else str(int(x)) for x in road))
