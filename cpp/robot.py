import math
from turtle import heading, pos
from mesa import Agent
import numpy as np
from cpp.cell import Cell
from cpp.color import Color



class Robot(Agent):
    def __init__(self, id, pos, model, planner, heading=(1,0)):
        super().__init__(id, model)
        print(pos)
        self.x, self.y = pos
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
        return -math.degrees(np.arctan2(self.heading[1], self.heading[0]))

    def step(self):
        destination: Cell = self.planner.next_destination(self)

        if destination != None:
            self.heading = (destination.y - self.pos[1], destination.x - self.pos[0])
            self.model.grid.move_agent(self, destination.pos)
            if not destination.isVisited:
                self.first_visits += 1
            destination.incrementVisitCount()
            

