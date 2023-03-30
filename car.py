import random

from traffic_simulation.map import Map
from traffic_simulation.road import Road
from traffic_simulation.direction import MoveDirection
from traffic_simulation.car import Car
from traffic_simulation.vector_2d import Vector_2d


class Car:
    def __init__(self, position: Vector_2d, direction: MoveDirection, map: Map, road: Road):
        self.position = position
        self.direction = direction
        self.road = road
        self.map = map
        self.v = 0
        self.__ACCELERATION = 1
        self.__PROPABILITY = 0.2

    def change_position(self, position):
        self.position = position

    def update_v(self, v):
        self.v = v

    def update_acceleration(self):
        if self.v < self.road.get_v_max():
            self.update_v(self.v + self.__ACCELERATION)
        else:
            pass  # car can't drive faster ;)

    def deacceleration(self):
        car_before = self.road.car_before(self)
        distance = self.road.distance(self, car_before)

        if self.v > distance:
            self.update_v(distance)
        else:
            pass  # deceleration is not necessary

    def random_events(self):
        if self.v > 0 and random.random() < self.__PROPABILITY:
            self.update_v(self.v - 1)
        else:
            pass  # everything ok

    def move(self):
        self.update_acceleration()
        self.deacceleration()
        self.random_events()

        if self.direction == MoveDirection.N:
            new_position = Vector_2d(self.position.x, self.position.y + s) ## oblicz nową pozycję (zastanów się nad wyjściem poza mapę)


        self.change_position(self.position.x + self.v)

    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction
