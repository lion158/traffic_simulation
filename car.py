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

    def update_position(self, position):
        self.position = position

    def update_v(self, v):
        self.v = v

    def update_acceleration(self):
        if self.v < self.road.get_v_max():
            self.update_v(self.v + self.__ACCELERATION)
        else:
            pass

    def deacceleration(self, car_before: Car): ## car befor from street (create function)
        #obliczanie odległości (chyva w klasie street)
        ...


    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction
