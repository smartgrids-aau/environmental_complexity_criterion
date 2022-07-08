
import numpy as np
from PIL import Image
import re
from cpp.constants import AREA, OBS
from cpp.shape import Shape

def generate_map_from_png(path, only_ground):
    img = Image.open(path)
    if only_ground:
        map = np.ones((img.height, img.width), np.int8)
        return map, img.width, img.height
    map = np.array(img)
    non_obs = np.array(map).mean(axis=2) != 0
    map = np.int8(np.zeros(non_obs.shape))
    map[non_obs] = AREA
    map[~non_obs] = OBS
    map = np.flip(map, axis=0)
    return map, img.width, img.height

def generate_map_by_pattern(pattern, map_shape, random): 
    attemps = 0
    while True:
        try:
            attemps += 1
            map = np.ones(map_shape)
            obs = pattern[1:-1].split(',')
            shapes = [Shape.get_shape(re.sub(' +', ' ', ob).strip(), random) for ob in obs]
            for shape in shapes:
                shape.draw(map)
            return map
        except Exception as err:
            print("error while generating map: {0}".format(err))
            if attemps > 100:
                raise Exception(err)
