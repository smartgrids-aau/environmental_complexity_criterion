"""
Modular Canvas Rendering
========================

Module for visualizing model objects in grid cells.

"""
from collections import defaultdict
from mesa.visualization.modules import CanvasGrid


class CanvasGridWithAngle(CanvasGrid):
    package_includes = ["CanvasModule.js", "InteractionHandler.js"]
    local_includes = ["modules/js/GridDraw.js"]

    def __init__(
        self,
        portrayal_method,
        grid_width,
        grid_height,
        canvas_width=500,
        canvas_height=500,
    ):
        super().__init__(portrayal_method,grid_width,grid_height,canvas_width,canvas_height)
