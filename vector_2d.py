class Vector_2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def add(self, vector_2d):
        return Vector_2d(self.x + vector_2d.x, self.y + vector_2d.y)

    def remove(self, vector_2d):
        return Vector_2d(self.x - vector_2d.x, self.y - vector_2d.y)