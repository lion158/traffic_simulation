from scipy.spatial import distance as d
from traffic_simulation.direction import MoveDirection
class Road:
    def __init__(self, direction, start, end, v_max):
        self.start = start
        self.end = end
        self.direction = direction
        self.__v_max = v_max
        self.lenght = 200 ###
        self.cars = []

    def get_v_max(self):
        return self.__v_max

    def distance(self, object, object_before):
        # distance = object_before.position.distance(object.position)
        if self.direction == MoveDirection.N:
            distance = object_before.position.y - object.position.y
        elif self.direction == MoveDirection.S:
            distance = object.position.y - object_before.position.y
        elif self.direction == MoveDirection.E:
            distance = object_before.position.x - object.position.x
        elif self.direction == MoveDirection.W:
            distance = object.position.x - object_before.position.x

        if distance >= 0:
            return distance #- 1    #zastanów się nad tymi - 1
        else:
            return distance + self.lenght #- 1

    def car_before(self, car):
        try:
            car_index = self.cars.index(car)
            return self.cars[car_index + 1]
        except IndexError:
            return self.cars[0]

    def add_car(self, car):
        self.cars.append(car)

    def move_cars(self):
        if len(self.cars) > 0:
            for car in self.cars:
                car.move()
        else:
            pass  # no cars on road

