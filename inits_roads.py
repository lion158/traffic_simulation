from traffic_simulation.direction import MoveDirection
from traffic_simulation.road import Road
from traffic_simulation.vector_2d import Vector_2d

ROADS = [
    Road(MoveDirection.E, Vector_2d(0, 0), Vector_2d(0, 50), 6),
    Road(MoveDirection.W, Vector_2d(0, 0), Vector_2d(0, 50), 6)
]
