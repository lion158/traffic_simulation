from mesa import Agent

class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        ...


class Road(Agent):
    def __init__(self, unique_id, model, start, end):
        super().__init__(unique_id, model)
        self.start = start
        self.end = end
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def remove_car(self, car):
        self.cars.remove(car)

    def update_cars(self):
        ...



class Intersection(Agent):
    def __init__(self, unique_id, model, position):
        super().__init__(unique_id, model)
        self.position = position
        self.roads = {}

    def add_road(self, road):
        self.roads[road.unique_id] = road

    def remove_road(self, road):
        ...

    de


