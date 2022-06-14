import os
from mesa.batchrunner import batch_run
import pandas as pd
from mesa.datacollection import DataCollector
from cpp.model import CoveragePathPlan
import os
import glob
import numpy as np
def get_max_visited_cell(model):
    max = 0
    for contents in model.grid.__iter__():
        if not contents[0].isObstacle and contents[0].visitCount > max:
            max = contents[0].visitCount
    return max

def get_cells_state(model):
    visits = [str(cell[0][0].visitCount).zfill(3) for cell in list(model.grid.coord_iter())]
    return visits

def check_final_result(model):
    for contents in model.grid.__iter__():
        cell = contents[0]
        if not cell.isObstacle and not cell.isVisited:
            return False
    return True
def get_wvisits(model):
    return np.sum([robot.wvisits for robot in model.schedule.agents])
class BatchCoveragePathPlan(CoveragePathPlan):

    def __init__(self, width=40, height=40, robot_count = 8, map = '', depth= 1, seed = None):
        super().__init__(width, height, robot_count, map, depth, seed)

        self.datacollector = DataCollector(
            model_reporters={
                "Max visited": get_max_visited_cell,
                "Solved": check_final_result,
                "wstep": get_wvisits
            },
            # agent_reporters={"first visits": lambda x: {'value': x.first_visits, 'color': x.color}},
            # agent_reporters={"first visits": lambda x: x.first_visits},
        )
    
maps = list(glob.glob(os.path.dirname(os.path.realpath(__file__)) + '\\cpp\\maps\\Ex\\maps\\s\\medium2.png'))
print(len(maps),'maps')
# parameter lists for each parameter to be tested in batch run
br_params = {
    # "width": 25,
    # "height": 25,
    "robot_count": [10],
    "map": maps,
    'depth': [15],
}

if __name__ == "__main__":
    data = batch_run(
        BatchCoveragePathPlan,
        br_params,
        iterations=10000,
        max_steps=10000,
        number_processes= None
    )
    br_df = pd.DataFrame(data)
    if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + "\\results"):
        os.makedirs(os.path.dirname(os.path.realpath(__file__)) + '\\results')
    br_df.to_csv(os.path.dirname(os.path.realpath(__file__)) + '\\results\\batch__dist.csv')
