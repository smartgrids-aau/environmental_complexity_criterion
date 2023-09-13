
import numpy as np
from PIL import Image
import re
from cpp.constants import AREA, OBS
from cpp.shape import Shape

def generate_map_from_png(path):
    img = Image.open(path).convert('L')
    obstacle_map = np.array(img)
    non_obs = obstacle_map > 128
    obstacle_map = np.int8(np.zeros(non_obs.shape))
    obstacle_map[non_obs] = AREA
    obstacle_map[~non_obs] = OBS
    obstacle_map = np.flip(obstacle_map, axis=0)
    return obstacle_map, img.width, img.height

def generate_map_by_pattern(pattern, obstacle_map_shape, random): 
    attemps = 0
    while True:
        try:
            attemps += 1
            obstacle_map = np.ones(obstacle_map_shape)
            obs = pattern[1:-1].split(',')
            shapes = [Shape.get_shape(re.sub(' +', ' ', ob).strip(), random) for ob in obs]
            for shape in shapes:
                shape.draw(obstacle_map)
            return obstacle_map
        except Exception as err:
            print("error while generating the obstacle_map: {0}".format(err))
            if attemps > 100:
                raise Exception(err)
