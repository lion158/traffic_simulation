from mesa import Agent


class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    # def step(self):
    #     print("Hi, I am agent " + str(self.unique_id) + "." + 'my poition: ')
    #     print(self.pos)
    #     self.model.space.move_agent(self, (10,10))
    def move(self):
        position = self.pos
        print("Hi, I am agent " + str(self.unique_id) + "." + 'my poition: ')
        print(self.pos)
        return (position[0] - 1, position[1])


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

    def step(self,):
        for car in self.cars:
            position = car.move()
            self.model.grid.move_agent(car, position)



class Intersection(Agent):
    def __init__(self, unique_id, model, position):
        super().__init__(unique_id, model)
        self.position = position
        self.roads = {}

    def add_road(self, road):
        self.roads[road.unique_id] = road

    def remove_road(self, road):
        ...


