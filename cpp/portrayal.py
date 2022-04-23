from typing import NamedTuple
from cpp.cell import Cell
from cpp.color import Color, compute_alpha

def portrayCell(agent):
    """
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the cell in its current state.
    """
    assert agent is not None
    if type(agent) is Cell:
        return {
            "Shape": "rect",
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Layer": 0,
            "x": agent.x,
            "y": agent.y,
            "Color": "black" if agent.isObstacle 
                    else Color(0,117,0).with_alpha(compute_alpha(agent.visitCount)) if agent.isVisited and agent.model_steps > 0
                    else 'white',
            "text": str(agent.visitCount) if not agent.isObstacle else '',
            "text_color": "white"
        }
    else:
        return {
            "Shape": "arrowHead",
            "scale": 1,
            "rotate": agent.angle,
            "Filled": "true",
            "Layer": 1,
            "x": agent.x,
            "y": agent.y,
            "Color": agent.color,
            "text": agent.unique_id,
            "text_color": "white"
        }


