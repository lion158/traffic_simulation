from traffic_simulation.car import Car
from traffic_simulation.direction import MoveDirection
from traffic_simulation.map import Map
from traffic_simulation.road import Road
from traffic_simulation.vector_2d import Vector_2d
from inits_roads import ROADS


class Simulation:

    def __init__(self):
        self.map = Map(50, 50)
        self.init()

    def __init_roads(self):
        self.map.add_roads(ROADS)
    def __init_cars(self):
        cars1 = [
            Car(Vector_2d(0, 0), self.map, ROADS[0]),
            Car(Vector_2d(20, 0), self.map, ROADS[0])
        ]
        cars2 = [
            Car(Vector_2d(0, 1), self.map, ROADS[1]),
            Car(Vector_2d(20, 1), self.map, ROADS[1])
        ]

        self.map.add_cars(cars1)
        self.map.add_cars(cars2)
        # for road in ROADS:
        #     road.add_car()
        for car in cars1:
            ROADS[0].add_car(car)

        for car in cars2:
            ROADS[1].add_car(car)
    def init(self):
        self.__init_roads()
        self.__init_cars()


    def update(self):
        self.map.move_cars()


