from dbm import dumb
from importlib.resources import contents
from itertools import combinations, combinations_with_replacement
from timeit import repeat
from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
import numpy as np
from PIL import Image
from cpp.cell import Cell
from cpp.robot import Robot


class CoveragePathPlan(Model):

    def __init__(self, width=40, height=40, robot_count = 8, path_to_map = ''):
        """
        Create a new playing area of (width, height) cells.
        """

        # Set up the grid and schedule.

        self.schedule = BaseScheduler(self)

        self.grid = MultiGrid(width, height, torus=False)

        if path_to_map!='':
            map = self.get_area_map(path_to_map)
            print(map.shape)

        # Place a dead cell at each location.
        for (contents, x, y) in self.grid.coord_iter():
            if path_to_map == '':
                cell = Cell((x, y), self.random.getrandbits(5) == 0, self)
            else:
                cell = Cell((x, y), not bool(map[x,y]), self)
            self.grid.place_agent(cell, (x, y))
            # self.schedule.add(cell)

        
        # robot_pos = [
        #     (1,6),
        #     (9,1),
        #     (30,6),
        #     (32,23),
        #     (32,28),
        #     (5,6),
        #     (2,6),
        #     (14,33),
        #     # (49,49),
        #     (34,20)
        # ]
        robot_pos = self.gen_coordinates(width, height, robot_count)
        i = 0
        for pos in robot_pos:
            robot = Robot(i, pos, self)
            self.grid.place_agent(robot, pos)
            self.schedule.add(robot)
            i+=1

        self.running = True

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
        
        self.running = False
        for (contents, x, y) in self.grid.coord_iter():
            cell = contents[0] if isinstance(contents[0], Cell) else contents[1]
            if not cell.isBarrier and not cell.isVisited:
                self.running = True
                break

    def gen_coordinates(self, width, height, count):
        seen = set()

        for _ in range(count):
            x = self.random.randint(0, width-1)
            y = self.random.randint(0, height-1)
            while (x, y) in seen:
                x = self.random.randint(0, width-1)
                y = self.random.randint(0, height-1)
            seen.add((x, y))
        return seen
            

    def get_area_map(self, path, area=1, obs=0):
        """
        Creates an array from a given png-image(path).
        :param path: path to the png-image
        :param area: non-obstacles tiles
        :param obs: obstacle tiles value
        :return: an array of area(0) and obstacle(-1) tiles
        """
        img = Image.open(path)
        img = img.rotate(-90)
        img = img.resize((self.grid.width, self.grid.height), Image.NEAREST)
        map = np.array(img)
        non_obs = np.array(map).mean(axis=2) != 0
        map = np.int8(np.zeros(non_obs.shape))
        map[non_obs] = area
        map[~non_obs] = obs
        return map
