from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from cpp.portrayal import portrayCell
from cpp.model import CoveragePathPlan

width, height = 50, 50

# Make a world that is 50x50, on a 500x500 display.
canvas_element = CanvasGrid(portrayCell, width, height, 500, 500)

server = ModularServer(
    CoveragePathPlan, [canvas_element], "Coverage Path Planning", {"height": height, "width": width}
)
