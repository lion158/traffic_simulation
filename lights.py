from traffic_simulation.vector_2d import Vector_2d


class Lights:
    def __init__(self, position: Vector_2d):
        self.position = position
        self.green = True

    def change_lights(self):
        self.green = not self.green
        print("Lights Change")
        print(f"Green: {self.green}")
