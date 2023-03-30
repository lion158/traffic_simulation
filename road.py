
class Road:
    def __init__(self, direction, start, end, v_max, map):
        self.start = start
        self.end = end
        self.direction = direction
        self.__v_max = v_max
        self.lenght = ... ###
        self.cars = []


    def get_v_max(self):
        return self.__v_max

    def distance(self, object, object_before):
        distance = object_before.position - object.position
        if distance >= 0:
            return distance - 1
        else:
            return distance + self.lenght - 1

    def car_before(self, car):
        try:
            car_index = self.cars.index(car)
            return self.cars[car_index + 1]
        except IndexError:
            return self.cars[0]
