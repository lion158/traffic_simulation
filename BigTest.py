import numpy as np


class Map:
    def __init__(self, N):
        self.N = N
        self.map = np.full((self.N, self.N), None)  # must be int value (to proper acceleration)
        self.n = [3, 11]
        self.s = [2, 10]
        self.w = [3, 11]
        self.e = [2, 10]

    def print_map(self):
        print(self.map)

    def temp_map(self):
        return np.full((self.N, self.N), None)

    def add_car(self, x, y):
        self.map[x][y] = 0

    def update_map(self, temp):
        self.map = temp.map

    def road(self):
        x_list = self.w + self.e
        y_list = self.n + self.s
        self.map[x_list, :] = -10
        self.map[:, y_list] = -10


class Simulation:
    def __init__(self, v_max, map):
        self.v_max = v_max
        self.map = map

    def acceleration(self, matrix):
        condition = np.logical_and(matrix >= 0, matrix < self.v_max)
        matrix[condition] += 1
        return matrix

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
                return 0 # distance 0
            else:
                return None # no other cars on the street
        else:
            return distance

        ################ sprawdź czy nie zmienia oryginalnej macierzy

    def next_lights_distance(self, matrix, index):
        self.next_car_distance(matrix, index)

    def next_lights_bool(self, matrix, index, distance): # index of car, distance to lights
        return matrix[index + distance + 1]

    def deacceleration(self, matrix_car, matrix_lights):
        new_matrix = np.full((self.map.N, self.map.N), None) # integer values


        for i, v in enumerate(matrix_car):  # i=index, v=value
            if v >= 0:
                next_car = self.next_car_distance(matrix_car, i)
                next_lights = self.next_lights_distance(matrix_lights, i)
                next_lights_bool = self.next_lights_bool(matrix_lights, i, next_lights) # True = green, False = red

                if not next_lights_bool and v > min(next_car, next_lights): # if red and v > distance to next object
                    v = min(next_car, next_lights)
                else:
                    v = min(v, next_car)







test = Simulation(5)
x = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [-1, -2, -10, False]])
x = test.acceleration(x)
print(x)

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
