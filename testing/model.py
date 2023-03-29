import mesa.time
import mesa.space
from mesa import Model
from traffic_simulation.testing.agent import Car
from traffic_simulation.testing.agent import Road


class Traffic_simulation_model(Model):
    def __init__(self, num_car,):
        self.num_car = num_car
        self.grid = mesa.space.SingleGrid(100, 100, True)
        self.schedule = mesa.time.RandomActivation(self) ##use step function on agents in random order

        #create agents:
        for i in range(self.num_car):
            ## adding car agent
            car = Car(i, self)
            self.schedule.add(car)
            self.grid.place_agent(car, (3,3))

            ##adding road
            road = Road(10, self, (10,3), (0,3))
            self.schedule.add(road)
            self.grid.place_agent(road,(0,0))

            ##adding car to road
            road.add_car(car)



    def step(self) -> None:
        self.schedule.step()





