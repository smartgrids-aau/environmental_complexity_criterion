from tabnanny import check
from typing import List
from xmlrpc.client import Boolean
from numpy import ndarray

from cpp.constants import OBS

RECT = 'rect'

class Shape:

    def __init__(self, random):
        self.random = random

    @staticmethod
    def get_shape(pattern, random):
        parts = pattern.split(' ')
        name = parts[0]
        if name == RECT:
            return Rect(int(parts[1]), int(parts[2]), random)


    def draw(self, map):
        positions = self.get_random_area(map)
        for y, x in positions:
            map[x, y] = OBS

    def get_random_area(self, map: ndarray):
        found = False
        while not found:
            anchor = (self.random.randint(0, map.shape[0]), self.random.randint(0, map.shape[1]))
            coors = self.get_draw_coors(anchor)
            found = self.check_fit_in_map(anchor, map.shape) and not self.check_collision(map, coors)
        return coors

    def check_fit_in_map(self, anchor, map_shape)->Boolean:
        pass

    def get_draw_coors(self, anchor)->List:
        pass

    def check_collision(self, map, shape_coors):
        for coor in shape_coors:
            if any(neighbor == OBS for neighbor in self.get_neightbors(coor, map.shape)):
                return True
        return False

    def get_neightbors(self, map_shape, coor):
        neighbors = [
            (coor[0] - 1, coor[1]),
            (coor[0] + 1, coor[1]),
            (coor[0], coor[1] - 1),
            (coor[0], coor[1] + 1)
        ]
        return list(filter(lambda n: n[0] in range(0, map_shape[0]) and n[1] in range(0, map_shape[1]), neighbors))



class Rect(Shape):

    def __init__(self, width, height, random):
        super().__init__(random)
        self.width = width
        self.height = height

    def check_fit_in_map(self, anchor, map_shape)->Boolean:
        return anchor[0] + self.height < map_shape[0] and anchor[1] + self.width < map_shape[1]

    def get_draw_coors(self, anchor)->ndarray:
        coors = []
        for i in range(anchor[0], anchor[0]+self.height):
            for j in range(anchor[1], anchor[1]+self.width):
                coors.append((i,j))
        return coors
    