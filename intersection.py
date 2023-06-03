import random

from car import Car
from direction import MoveDirection
from vector import Vector


class Intersection:
    def __init__(self, id, position, map):
        self.id = id
        self.position = Vector(position[1], position[0])
        self.map = map



    def check_jam(self, cars_v_matrix, cars_object_matrix): #function return position and v (to change v_matrix) of random choice car to solve jam

        def can_go(car:Car, i, j):
            if car.direction == MoveDirection.N:
                if car.will_turn:
                    if car.will_turn_right:
                        return cars_v_matrix[i - 1][j + 1] < 0 and self.map.car_v_map[i - 1][j] < 0
                    if car.will_turn_left:
                        return cars_v_matrix[i - 2][j - 2] < 0 and self.map.car_v_map[i - 2][j - 1] < 0 and self.map.car_v_map[i - 2][j] < 0 and self.map.car_v_map[i - 1][j] < 0
                else:
                    return cars_v_matrix[i - 3][j] < 0 and self.map.car_v_map[i - 1][j] < 0 and self.map.car_v_map[i - 2][j] < 0
            if car.direction == MoveDirection.S:
                if car.will_turn:
                    if car.will_turn_right:
                        return cars_v_matrix[i + 1][j - 1] < 0 and self.map.car_v_map[i + 1][j] < 0
                    if car.will_turn_left:
                        return cars_v_matrix[i + 2][j + 2] < 0 and self.map.car_v_map[i + 2][j + 1] < 0 and self.map.car_v_map[i + 2][j] < 0 and self.map.car_v_map[i + 1][j] < 0
                else:
                    return cars_v_matrix[i + 3][j] < 0 and self.map.car_v_map[i + 1][j] < 0 and self.map.car_v_map[i + 2][j] < 0
            if car.direction == MoveDirection.W:
                if car.will_turn:
                    if car.will_turn_right:
                        return cars_v_matrix[i - 1][j - 1] < 0 and self.map.car_v_map[i][j - 1] < 0
                    if car.will_turn_left:
                        return cars_v_matrix[i + 2][j - 2] < 0 and self.map.car_v_map[i + 1][j - 2] < 0 and self.map.car_v_map[i][j - 2] < 0 and self.map.car_v_map[i][j - 1] < 0
                else:
                    return cars_v_matrix[i][j - 3] < 0 and self.map.car_v_map[i][j - 1] < 0 and self.map.car_v_map[i][j - 2] < 0
            if car.direction == MoveDirection.E:
                if car.will_turn:
                    if car.will_turn_right:
                        return cars_v_matrix[i + 1][j + 1] < 0 and self.map.car_v_map[i][j + 1] < 0
                    if car.will_turn_left:
                        return cars_v_matrix[i - 2][j + 2] < 0 and self.map.car_v_map[i - 1][j + 2] < 0 and self.map.car_v_map[i][j + 2] < 0 and self.map.car_v_map[i][j + 1] < 0
                else:
                    return cars_v_matrix[i][j + 3] < 0 and self.map.car_v_map[i][j + 1] < 0 and self.map.car_v_map[i][j + 2] < 0

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
            if cars_v_matrix[car.position_normal.y][car.position_normal.x] == 0:
                standing_cars.append(False)

        if len(cars) == len(standing_cars) and len(cars) > 0:  # their is a jam
            for _ in range(len(cars)):
                random_car = random.choice(cars)
                i = random_car.position_normal.y
                j = random_car.position_normal.x
                # checking if position after posible turn is free
                if can_go(random_car, i, j):
                    random_car.go = True
                    break
                else:
                    cars.remove(random_car)