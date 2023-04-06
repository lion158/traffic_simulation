# from traffic_simulation.car import Car
# from traffic_simulation.road import Road


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = []
        self.roads = []
        self.cars = []

    def add_road(self, road):
        self.roads.append(road)

    def add_car(self, car):
        self.cars.append(car)

    def add_roads(self, roads):
        for road in roads:
            self.add_road(road)

    def add_cars(self, cars):
        for car in cars:
            self.add_car(car)
    def move_cars(self):
        for road in self.roads:
            road.move_cars()