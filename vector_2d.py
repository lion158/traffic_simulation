from scipy.spatial import distance as d

class Vector_2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return self.x - other.x, self.y - other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __le__(self, other):
        return self.age <= other.age
    def add(self, vector_2d):
        return Vector_2d(self.x + vector_2d.x, self.y + vector_2d.y)

    def remove(self, vector_2d):
        return Vector_2d(self.x - vector_2d.x, self.y - vector_2d.y)

    def distance(self, other):
        x = (self.x, self.y)
        y = (other.x, other.y)
        return d.euclidean(x, y)