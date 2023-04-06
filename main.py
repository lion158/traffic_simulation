from traffic_simulation.simulation import Simulation
from traffic_simulation.window import Window


def main():
    simulation = Simulation()
    window = Window(simulation)
    window.loop()

if __name__ == '__main__':
    main()