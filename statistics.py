import matplotlib.pyplot as plt
import numpy as np
from engine import Engine
from map import Map
from simulation import Simulation


class Statistics:
    def mean_v(self, v_map, car_number):
        mask = (v_map >= 0)
        return np.sum(v_map[mask]) / car_number

    def cars_stop_ratio(self, v_map, car_number):
        mask = (v_map == 0)
        return np.sum(v_map[mask]) / car_number

    def cars_move_ratio(self, v_map, car_number):
        mask = (v_map > 0)
        return np.sum(v_map[mask]) / car_number

    def min_value(self, vector):
        return min(vector)

    def max_value(self, vector):
        return max(vector)

    def mean_value(self, vector):
        return np.mean(vector)

    def standard_deviation(self, vector):
        return np.std(vector)

s = Statistics()
map = Map(100)
simulation = Simulation(v_max=6, map=map, cars_number=200, time=1)
engine = Engine(simulation, map)

mean_vs = []
stop_cars_number = []
for i in range(500):
    engine.loop(time=1) # no need time here
    mean_vs.append(s.mean_v(engine.map.car_v_map, 200))
    stop_cars_number.append(s.cars_stop_ratio(engine.map.car_v_map, 200))

mean_value = s.mean_value(mean_vs)
plt.plot(mean_vs, label='mean velocity')
plt.axhline(mean_value, color='red', linestyle='--', label='mean')
plt.legend()
plt.show()

mean_value = s.mean_value(stop_cars_number)
plt.plot(stop_cars_number, label='stop cars ratio')
plt.legend()
plt.show()

plt.boxplot(mean_vs)
plt.title('mean velocity boxplot')
plt.show()

#TODO te funkcje powyżej jeszcze do przepatarzenia