import random
import numpy as np
import copy
import sys

import pygame

from traffic_simulation.direction import MoveDirection


#TODO drawing_next_turn
cars = []
map = Map(100)

# car = map.add_car(11, 1, MoveDirection.E)
# cars.append(car)
# car = map.add_car(10, 4, MoveDirection.W)
# cars.append(car)
# car = map.add_car(12, 3, MoveDirection.N)
# cars.append(car)
# car = map.add_car(9, 2, MoveDirection.S)
# cars.append(car)

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

simulation = Simulation(v_max=6, map=map, cars_number=200, time=1)
engine = Engine(simulation, map)
window = Window(engine)
window.loop()


# simulation = Simulation(v_max=6, map=map, cars_number=200, time=1)
# engine = Engine(simulation, map)
# for _ in range(1000):
#     engine.loop(0)

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
