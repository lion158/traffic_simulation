from mesa import Model
from agent import Car

class Traffic_simulation_model(Model):
    def __init__(self, N, width, height):
        self.num_car = N
