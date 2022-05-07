import os
from mesa.batchrunner import batch_run
import pandas as pd
from mesa.datacollection import DataCollector
from cpp.model import CoveragePathPlan

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

class BatchCoveragePathPlan(CoveragePathPlan):

    def __init__(self, width=40, height=40, robot_count = 8, map = '', depth= 1, seed = None):
        super().__init__(width, height, robot_count, map, depth, seed)

        self.datacollector = DataCollector(
            model_reporters={
                "width": "width",
                "height": "height",
                "Max visited": get_max_visited_cell,
                "final state": get_cells_state,
                "Solved": check_final_result
            },
            # agent_reporters={"first visits": lambda x: {'value': x.first_visits, 'color': x.color}},
            # agent_reporters={"first visits": lambda x: x.first_visits},
        )
    

# parameter lists for each parameter to be tested in batch run
br_params = {
    # "width": 25,
    # "height": 25,
    "robot_count": [3, 20],
    "map": ["cpp\maps\star.png", "{rect 8 4, L 7 2 -8 3, rect 6 6}", "{L 20 3 15 3, rect 4 4, rect 2 9}"],
    'depth': [1, 5, 9],
}

if __name__ == "__main__":
    data = batch_run(
        BatchCoveragePathPlan,
        br_params,
        iterations=2,
        max_steps=3000
    )
    br_df = pd.DataFrame(data)
    if not os.path.exists('results'):
        os.makedirs('results')
    br_df.to_csv('results/batch_run.csv')
