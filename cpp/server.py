from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from cpp.portrayal import portrayCell
from cpp.model import CoveragePathPlan

width, height = 40, 40

# Make a world that is 50x50, on a 500x500 display.
canvas_element = CanvasGrid(portrayCell, width, height, 400, 400)

model_params = {
    "width": 40,
    "height": 40,
    "robot_count": UserSettableParameter(
        "slider",
        "Robots Count",
        8,
        1,
        100
    ),
}

server = ModularServer(
    CoveragePathPlan, [canvas_element], "Coverage Path Planning", model_params
)
