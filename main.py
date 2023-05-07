from traffic_simulation.engine import Engine
from traffic_simulation.map import Map
from traffic_simulation.simulation import Simulation
from traffic_simulation.window import Window

#TODO INTERSECTIONS JAMS COŚ  JEST NIE TAK (MIAŁO TEGO NIE BYĆ) SPRAWDŹ
def main():
    map = Map(100)
    simulation = Simulation(v_max=6, map=map, cars_number=200, time=1)
    engine = Engine(simulation, map)
    window = Window(engine)
    window.loop()
if __name__ == '__main__':
    main()

