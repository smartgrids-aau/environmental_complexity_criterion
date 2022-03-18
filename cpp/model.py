from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid

from cpp.cell import Cell
from cpp.robot import Robot


class CoveragePathPlan(Model):

    def __init__(self, width=50, height=50):
        """
        Create a new playing area of (width, height) cells.
        """

        # Set up the grid and schedule.

        self.schedule = BaseScheduler(self)

        self.grid = MultiGrid(width, height, torus=False)

        
        robot_pos = [
            (1,6),
            (10,26),
            (40,6),
            (42,23),
            (42,28),
            (12,6),
            (34,33)
        ]
        for i in range(len(robot_pos)):
            pos = robot_pos[i]
            robot = Robot(i, pos, self)
            self.grid.place_agent(robot, pos)
            self.schedule.add(robot)

        # Place a dead cell at each location.
        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self)
            self.grid.place_agent(cell, (x, y))
            # self.schedule.add(cell)

        self.running = True

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
