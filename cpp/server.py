from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from cpp.planners.greedy import GreedyPlanner
from cpp.portrayal import portrayCell
from cpp.model import CoveragePathPlan
from modules.CanvasGridVisualization import CanvasGridWithAngle
from modules.ColorfullBarChartVisualization import ColorfullBarChartModule
from PIL import Image

width, height = 25, 25
path_to_map = 'cpp\maps\star.png'
if path_to_map is not None:
    img = Image.open(path_to_map)
    width, height = img.size


model_params = {
    "width": None,
    "height": None,
    "robot_count": UserSettableParameter(
        "slider", "Robots Count", 8, 1, 50
    ),
    "map": path_to_map,
    # "map": """{
    #     rect 4 5, rect 10 5 , rect 2 6, L -5 2 -7 2, L -14 2 -12 2,
    #     L 4 1 -5 1, L -6 1 6 2, rect 1 1, rect 3 4, rect 2 2, rect 2 2, rect 1 1, rect 2 4
    #  }""",
    'depth': UserSettableParameter(
        "number", "Greedy planner depth", 3
    ),
    'seed': 7
}

canvas_element = CanvasGridWithAngle(portrayCell, width, height, 500*width/height, 500)

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
    model_cls= CoveragePathPlan,
    visualization_elements= [canvas_element, chart_element, agent_bar],
    name= "Coverage Path Planning",
    model_params= model_params
)
