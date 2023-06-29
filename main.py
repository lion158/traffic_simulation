from simulation.engine import Engine
from simulation.map import Map
from simulation.simulation import Simulation
from simulation.window import Window

def main():
    map = Map(100)
    simulation = Simulation(v_max=6, map=map, cars_number=200, lights=True, lights_time=5, time=1)
    engine = Engine(simulation, map)
    window = Window(engine)
    window.loop()
if __name__ == '__main__':
    main()

