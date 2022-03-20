from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from cpp.portrayal import portrayCell
from cpp.model import CoveragePathPlan
from modules.ColorfullBarChartVisualization import ColorfullBarChartModule

width, height = 25,25
# cell_size = 12

# Make a world that is 50x50, on a 500x500 display.
canvas_element = CanvasGrid(portrayCell, width, height, 500, 500)

model_params = {
    "width": width,
    "height": height,
    "robot_count": UserSettableParameter(
        "slider",
        "Robots Count",
        8,
        1,
        100
    ),
    "path_to_map": 'cpp\maps\map1.png'
}

chart_element = ChartModule(
    [
        {"Label": "Uncovered Cells", "Color": "#3349FF"}
    ]
)

agent_bar = ColorfullBarChartModule(
    [{"Label": "first visits"}],
    scope="agent",
    sorting="ascending",
    sort_by='unique_id',
    canvas_width=700,
    canvas_height=350
)

server = ModularServer(
    CoveragePathPlan, [canvas_element, chart_element, agent_bar], "Coverage Path Planning", model_params
)
