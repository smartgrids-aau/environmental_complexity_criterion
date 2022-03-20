from typing import NamedTuple
from cpp.cell import Cell
from cpp.color import Color, compute_alpha

def portrayCell(agent):
    """
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the cell in its current state.
    :param cell:  the cell in the simulation
    :return: the portrayal dictionary.
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
                    else Color(0,117,0).with_alpha(compute_alpha(agent.visitCount)) if agent.isVisited 
                    else 'white',
            "text": str(agent.visitCount) if not agent.isObstacle else '',
            "text_color": "white"
        }
    else:
        return {
            "Shape": "circle",
            "r": 0.8,
            "Filled": "true",
            "Layer": 1,
            "x": agent.x,
            "y": agent.y,
            "Color": agent.color,
            "text": agent.unique_id,
            "text_color": "white"
        }


