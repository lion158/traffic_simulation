import random

from traffic_simulation.map import Map
from traffic_simulation.road import Road
from traffic_simulation.direction import MoveDirection
from traffic_simulation.vector_2d import Vector_2d


class Car:
    def __init__(self, position: Vector_2d, map: Map, road: Road):
        self.position = position
        self.road = road
        self.map = map
        self.direction = self.road.direction
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
        # if len(self.road.cars) > 1:
        next_light = self.road.next_lights(self)
        next_light_distance = self.road.distance(self, next_light)
        # print(f"NEXT_LIGHT_DISTANCE: {next_light_distance}")
        next_car_distance = self.road.distance(self, self.road.car_before(self))
        # print(f"NEXT_CAR_DISTANCE: {next_car_distance}")
        distance = min(next_car_distance,next_light_distance)
        print(f"DISTANCE: {distance}, pręskość: {self.v}, light: {next_light.green}")
        if not next_light.green and self.v > distance:
            self.update_v(distance)
            print("CZERWONE!")
        else:
            self.update_v(min(self.v, next_car_distance))
                # deceleration is not necessary

        # if len(self.road.cars) > 1:
        #     car_before = self.road.car_before(self)
        #     distance = self.road.distance(self, car_before)
        #     if self.v > distance:
        #         self.update_v(distance)
        # else:
        #     pass  # deceleration is not necessary

    def random_events(self):
        if self.v > 0 and random.random() < self.__PROPABILITY:
            self.update_v(self.v - 1)
        else:
            pass  # everything ok

    def move(self):
        self.update_acceleration()
        self.deacceleration()
        # self.random_events()

        # if road direction N
        if self.direction == MoveDirection.N:
            new_position = Vector_2d(self.position.x, self.position.y + self.v)
            if new_position.y <= self.road.lenght:  # to zależy jak będzie lenght (ew + - 1)
                pass  # valid position
            else:
                new_position.y -= self.road.lenght  # to zależy jak będzie lenght (ew + - 1)

        # if road direction S
        elif self.direction == MoveDirection.S:
            new_position = Vector_2d(self.position.x, self.position.y - self.v)
            if new_position.y >= 0:
                pass  # valid position
            else:
                new_position.y += self.road.lenght  # to zależy jak będzie lenght (ew + - 1)

        # if road direction W
        elif self.direction == MoveDirection.W:
            new_position = Vector_2d(self.position.x - self.v, self.position.y)
            if new_position.x >= 0:
                pass  # valid position
            else:
                new_position.x += self.road.lenght  # to zależy jak będzie lenght (ew + - 1)

        # if road direction E
        elif self.direction == MoveDirection.E:
            new_position = Vector_2d(self.position.x + self.v, self.position.y)
            if new_position.x <= self.road.lenght:  # to zależy jak będzie lenght (ew + - 1)
                pass  # valid position
            else:
                new_position.x -= self.road.lenght  # to zależy jak będzie lenght (ew + - 1)

        self.change_position(new_position)
        # print(f"NEW POSITION: {new_position}")

    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction


# map = Map(10, 10)
# road = Road(MoveDirection.S, (0,10), (0, 0), 7)
# car = Car(Vector_2d(0,10), map, road)
# car2 = Car(Vector_2d(0,5), map, road)
# road.add_car(car)
# road.add_car(car2)

#
# road.move_cars()
# road.move_cars()
# road.move_cars()
# road.move_cars()
# road.move_cars()
# road.move_cars()
# road.move_cars()
# road.move_cars()
# road.move_cars()
