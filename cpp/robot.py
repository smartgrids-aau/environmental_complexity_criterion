from typing import Set
from mesa import Agent
from cpp.cell import Cell

from operator import attrgetter


class Robot(Agent):
    def __init__(self, id, pos, model):
        super().__init__(id, model)
        print(pos)
        self.x, self.y = pos
        self.color = "#"+''.join([self.random.choice('0123456789ABCDEF') for j in range(6)])

    @property
    def neighborhood(self):
        return self.model.grid.get_neighborhood(self.pos, False, False)

    @property
    def empty_neighbor_cells(self):
        neighborsContent = self.model.grid.get_neighbors(self.pos, False, False)
        return list(filter(lambda grid: isinstance(grid, Cell) and grid.isEmpty, neighborsContent))

    def get_cell(self, grid):
        # print(type(grid))
        if grid is Set:
            for content in grid:
                if content is Cell:
                    return content 
        else:
            return grid

    @property
    def cell(self):
        return self.model.grid[self.pos][0]

    def step(self):
        # destination = self.get_cell(self.random.choice(self.neighbors))
        choices = self.empty_neighbor_cells
        if len(choices) > 0:
            min_value = min(choice.visitCount for choice in choices)
            destination = self.random.choice([cell for cell in choices if cell.visitCount == min_value])

            self.model.grid.move_agent(self, destination.pos)
            destination.incrementVisitCount()
            

