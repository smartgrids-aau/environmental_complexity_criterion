from importlib.resources import contents
import re
from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from cpp.cell import Cell
from cpp.constants import OBS
from cpp.map import generate_map_by_pattern, generate_map_from_png
from cpp.planners.greedy import GreedyPlanner
from cpp.robot import Robot
from mesa.datacollection import DataCollector

STOCK_THRESHOLD = 100

def get_num_empty_cells(model):
    empty_cells = [content[0] for content in model.grid if (not content[0].isVisited and not content[0].isObstacle)]
    return len(empty_cells)


class CoveragePathPlan(Model):

    def __init__(self, width=40, height=40, robot_count = 8, map = '', depth = 1, seed = None):
        super().__init__()

        self._seed = seed
        self.schedule = BaseScheduler(self)
        self.grid = MultiGrid(width, height, torus=False)
        self.planner = GreedyPlanner(depth)
        self.stock_step_counts = 0
        self.stock = True

        if map!='':
            if re.match('^{((.|\n)*)}$', map):
                map = generate_map_by_pattern(map, (self.grid.height, self.grid.width), self.random)
            else:
                map = generate_map_from_png(map, (self.grid.height, self.grid.width))

        for (_, x, y) in self.grid.coord_iter():
            if map == '':
                cell = Cell((x, y), self.random.getrandbits(5) == 0, self)
            else:
                cell = Cell((x, y), map[y, x] == OBS, self)
            self.grid.place_agent(cell, (x, y))

        robot_pos = self.gen_coordinates(width, height, robot_count, map)
        for pos in robot_pos:
            robot = Robot(self.next_id(), pos, self, self.planner)
            self.grid.place_agent(robot, pos)
            self.schedule.add(robot)
            self.grid[pos][0].incrementVisitCount()
            robot.first_visits += 1

        self.datacollector = DataCollector(
            model_reporters={
                "Uncovered Cells": get_num_empty_cells
            },
            agent_reporters={"first visits": lambda x: {'value': x.first_visits, 'color': x.color}},
            # agent_reporters={"first visits": lambda x: x.first_visits},
        )

        self.datacollector.collect(self)
        self.running = True


    def step(self):
        prev_positions = [robot.pos for robot in self.schedule.agents]

        self.schedule.step()
        self.datacollector.collect(self)
        
        self.running = False
        for contents in self.grid.__iter__():
            cell = contents[0]
            if not cell.isObstacle and not cell.isVisited:
                self.running = True
                break
    
        cur_positions = [robot.pos for robot in self.schedule.agents]
        if prev_positions == cur_positions:
            self.stock_step_counts += 1
            if self.stock_step_counts == STOCK_THRESHOLD:
                self.stock = True
                self.running = False
        else:
            self.stock_step_counts = 0

        


    def gen_coordinates(self, width, height, count, map):
        seen = set()

        for _ in range(count):
            x = self.random.randint(0, width-1)
            y = self.random.randint(0, height-1)
            while (x, y) in seen or map[y, x] == OBS:
                x = self.random.randint(0, width-1)
                y = self.random.randint(0, height-1)
            seen.add((x, y))
        return seen
            