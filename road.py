
class Road:
    def __init__(self, direction, start, end, v_max, map):
        self.start = start
        self.end = end
        self.direction = direction
        self.__v_max = v_max
        cars = []


    def get_v_max(self):
        return self.__v_max