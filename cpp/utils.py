import math
import numpy as np

MAX_INT = 99999

def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return int(math.degrees(
        np.arccos(
            np.clip(
                np.dot(v1_u, v2_u), -1.0, 1.0
            )
        )
    ))