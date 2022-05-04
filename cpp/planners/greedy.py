import queue
from turtle import width
import numpy as np
from cpp.cell import Cell
from cpp.planner import Planner
from cpp.robot import Robot
from cpp.utils import MAX_INT


class GreedyPlanner(Planner):

    def __init__(self, depth=1):
        self.depth = depth

    def next_destination(self, robot: Robot) -> Cell:
        grid = robot.model.grid
        
        neighborsContent = grid.get_neighbors(robot.pos, moore=True, include_center=False)
        neighbors = list(filter(lambda content: isinstance(content, Cell), neighborsContent))

        min_direction_cost = MAX_INT
        best_choices = []
        for i in range(len(neighbors)):
            destination = neighbors[i]
            direction = np.subtract(destination.pos, robot.pos)
            d = 1
            total_cost = 0
            min_cost = 99999
            while d <= self.depth:
                total_cost += destination.visitCount
                cost = total_cost / d
                if cost < min_cost:
                    min_cost = cost
                next_destination_pos = np.add(destination.pos, direction)
                if next_destination_pos[0] in range(0,grid.width) and next_destination_pos[1] in range(0,grid.height):
                    destination = grid[next_destination_pos][0]
                    d += 1
                else:
                    break
    
            if min_cost < min_direction_cost:
                min_direction_cost = min_cost
                best_choices = [neighbors[i]]
            elif min_cost == min_direction_cost:
                best_choices.append(neighbors[i])

        best_destination = robot.random.choice(best_choices)
        return best_destination