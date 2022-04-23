import math
from turtle import heading, pos
from mesa import Agent
import numpy as np
from cpp.cell import Cell
from cpp.color import Color



class Robot(Agent):
    def __init__(self, id, pos, model, planner, heading=(0,1)):
        super().__init__(id, model)
        print(pos)
        self.first_visits = 0
        self.planner = planner
        self.color = Color.random(self.random)
        self.heading = heading

    @property
    def cell(self):
        return self.model.grid[self.pos][0]

    @property
    def empty_neighbor_cells(self):
        neighborsContent = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        return list(filter(lambda content: isinstance(content, Cell) and content.isEmpty, neighborsContent))

    @property
    def angle(self):
        return -math.degrees(np.arctan2(*self.heading))

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def prev_pos(self):
        return (self.x - self.heading[0], self.y - self.heading[1])

    def step(self):
        destination: Cell = self.planner.next_destination(self)

        if destination != None:
            self.heading = (destination.x - self.x, destination.y - self.y)
            self.model.grid.move_agent(self, destination.pos)
            if not destination.isVisited:
                self.first_visits += 1
            destination.incrementVisitCount()
            

