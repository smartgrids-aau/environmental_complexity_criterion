from importlib.resources import contents
import random
import re
from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
import numpy as np
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
    
    """Parameters
    ----------
    width, height : int
        The map width and height. if map is path to a png file width and height will be determined by png file 
        and these 2 parameters are ignored
    map : str
        map can be a path to a png file or a pattern for generating maps randomly containing given shapes.
        Currently, rectangle and L shapes are available. The pattern includes a list of shapes separated 
        with commas and surrounded between { }.
        To add rectangle to the map use rect keyword followed by its height and width separated with spaces.
        To add L shape to the map use L keyword followed by 4 numbers:
            1. Lenght of the vertical bar of L. if a negative number is given, L shape will be flipped vertically
            2. Thickness of vertical bar
            3. Lenght of the horizontal bar of L. if a negative number is given, L shape will be flipped horizontally
            4. Thickness of horizontal bar
        example:
            {
                rect 4 5, rect 10 5 , rect 2 6, L -5 2 -7 2, L -14 2 -12 2,
                L 4 1 -5 1, L -6 1 6 2, rect 1 1, rect 3 4, rect 2 2, rect 2 2, rect 1 1, rect 2 4
            }
    depth : int
        the depth greedy planner searches in each direction for best destination
    position_seed : int
        Random seed used for placing robots in map
    model_seed : int
        Random seed used in robot movements and planner algorithms
    map_seed : int
        Random seed used for generating map using pattern
    """
    def __init__(
        self,
        width=40, height=40,
        robot_count = 8,
        map = '',
        depth = 1,
        position_seed = None, model_seed = None, map_seed = None
    ):
        super().__init__()
        self._seed = model_seed
        self.schedule = BaseScheduler(self)
        
        map_is_empty = False
        if map:
            if re.match('^{((.|\n)*)}$', map): # map is pattern-based
                map_random = random.Random(map_seed)
                map = generate_map_by_pattern(map, (height, width), map_random)
            else: # map is path to png file
                map, width, height = generate_map_from_png(map)
        else:
            map_is_empty = True
            map = np.ones((height, width), np.int8)

        self.width, self.height = width, height
        self.grid = MultiGrid(width, height, torus=False)

        self.planner = GreedyPlanner(depth)
        self.stock_step_counts = 0
        self.stock = True

        for (_, x, y) in self.grid.coord_iter():
            if map_is_empty:
                # cell = Cell((x, y), map_random.getrandbits(5) == 0, self) 
                cell = Cell((x, y), False, self)
            else:
                cell = Cell((x, y), map[y, x] == OBS, self)
            self.grid.place_agent(cell, (x, y))

        position_random = random.Random(position_seed)
        robot_pos = self.gen_coordinates(width, height, robot_count, map, position_random)
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
        


    def gen_coordinates(self, width, height, count, map, random):
        seen = set()

        for _ in range(count):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            while (x, y) in seen or map[y, x] == OBS:
                x = random.randint(0, width-1)
                y = random.randint(0, height-1)
            seen.add((x, y))
        return seen
            