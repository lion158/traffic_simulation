from engine import Engine
from map import Map
from simulation import Simulation
from window import Window

#TODO INTERSECTIONS JAMS COŚ  JEST NIE TAK (MIAŁO TEGO NIE BYĆ) SPRAWDŹ
def main():
    map = Map(100)
    simulation = Simulation(v_max=6, map=map, cars_number=200, time=1)
    engine = Engine(simulation, map)
    window = Window(engine)
    window.loop()
if __name__ == '__main__':
    main()

