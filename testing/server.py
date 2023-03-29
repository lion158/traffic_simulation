# from model import Traffic_simulation_model
#
# empty_model = Traffic_simulation_model(1)
#
# empty_model.step()
# empty_model.step()
# empty_model.step()
# empty_model.step()
# empty_model.step()

from traffic_simulation.testing.model import Traffic_simulation_model
import mesa


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    return portrayal

space = mesa.visualization.CanvasGrid(agent_portrayal,100,100,400,400)
server = mesa.visualization.ModularServer(
    Traffic_simulation_model, [space], "Money Model", {"num_car": 1,}
)
server =  mesa.visualization.ModularServer(Traffic_simulation_model,
                       [space],
                       "Traffic_simulation_model",
                       {"num_car": 1},
                       )
server.port = 8521 # The default
server.launch()