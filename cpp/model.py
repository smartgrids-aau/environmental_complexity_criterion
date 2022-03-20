from importlib.resources import contents
from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
import numpy as np
from PIL import Image
from cpp.cell import Cell
from cpp.planners.greedy import GreedyPlanner
from cpp.robot import Robot
from mesa.datacollection import DataCollector

def get_num_empty_cells(model):
    all = list(model.grid.__iter__())
    empty_cells = [content[0] for content in model.grid if (not content[0].isVisited and not content[0].isObstacle)]
    print(len(empty_cells), len(all))
    return len(empty_cells)


class CoveragePathPlan(Model):
    AREA, OBS = 1 , 0

    def __init__(self, width=40, height=40, robot_count = 8, path_to_map = '', planner= GreedyPlanner(), seed = None):

        self._seed = seed
        self.schedule = BaseScheduler(self)
        self.grid = MultiGrid(width, height, torus=False)
        self.planner = planner

        if path_to_map!='':
            map = self.get_area_map(path_to_map)
            print(map.shape)

        for (contents, x, y) in self.grid.coord_iter():
            if path_to_map == '':
                cell = Cell((x, y), self.random.getrandbits(5) == 0, self)
            else:
                cell = Cell((x, y), map[x,y] == self.OBS, self)
            self.grid.place_agent(cell, (x, y))

        # robot_pos = [
        #     (1,6),
        #     (9,1),
        #     (30,6),
        #     (32,23),
        #     (32,28),
        #     (5,6),
        #     (2,6),
        #     (14,33),
        #     (49,49),
        #     (34,20)
        # ]
        robot_pos = self.gen_coordinates(width, height, robot_count, map)
        i = 0
        for pos in robot_pos:
            robot = Robot(i, pos, self, planner)
            self.grid.place_agent(robot, pos)
            self.schedule.add(robot)
            i+=1

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
        self.schedule.step()
        self.datacollector.collect(self)
        
        self.running = False
        for (contents, x, y) in self.grid.coord_iter():
            cell = contents[0] if isinstance(contents[0], Cell) else contents[1]
            if not cell.isObstacle and not cell.isVisited:
                self.running = True
                break


    def gen_coordinates(self, width, height, count, map):
        seen = set()

        for _ in range(count):
            x = self.random.randint(0, width-1)
            y = self.random.randint(0, height-1)
            while (x, y) in seen or map[x,y] == self.OBS:
                x = self.random.randint(0, width-1)
                y = self.random.randint(0, height-1)
            seen.add((x, y))
        return seen
            

    def get_area_map(self, path):
        img = Image.open(path)
        img = img.rotate(-90)
        img = img.resize((self.grid.width, self.grid.height), Image.NEAREST)
        map = np.array(img)
        non_obs = np.array(map).mean(axis=2) != 0
        map = np.int8(np.zeros(non_obs.shape))
        map[non_obs] = self.AREA
        map[~non_obs] = self.OBS
        return map
