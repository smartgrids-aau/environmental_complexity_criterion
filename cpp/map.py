
import numpy as np
from PIL import Image
import re
from cpp.constants import AREA, OBS
from cpp.shape import Shape

def generate_map_from_png(path, shape):
    img = Image.open(path)
    img = img.rotate(-90)
    img = img.resize(shape, Image.NEAREST)
    map = np.array(img)
    non_obs = np.array(map).mean(axis=2) != 0
    map = np.int8(np.zeros(non_obs.shape))
    map[non_obs] = AREA
    map[~non_obs] = OBS
    return map

def generate_map_by_pattern(pattern, shape, random):     
    map = np.ones(shape)
    obs = pattern[1:-1].split(',')
    shapes = [Shape.get_shape(re.sub(' +', ' ', ob).strip(), random) for ob in obs]
    for shape in shapes:
        shape.draw(map)
    return map
