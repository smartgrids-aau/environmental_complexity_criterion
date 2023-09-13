# Run "python batch_run.py -h" for help
# Sample command:
# > python batch_run.py --path <PATH_TO_PNGs_DIR> -r 9 12 15 -d 3 6 9 -i 10 -s 1000
#             *******all arguments are optional*******

import os
import argparse
import pandas as pd
from mesa.datacollection import DataCollector
from cpp.batchrunner import batch_run_with_rngs
from cpp.model import CoveragePathPlan
import os
import glob
import numpy as np
from itertools import groupby

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

def merge(groupby_df):
    o = groupby_df.loc[groupby_df['obstacle_free'] == False].iloc[0]
    of = groupby_df.loc[groupby_df['obstacle_free'] == True].iloc[0]
    df = pd.DataFrame(
        {
        "steps" : [o['Step']],
        "steps_of":[of['Step']],
        "A_o/A_of":[float(o['area'])/of['area']],
        "Complexity":[1 - ((float(of['Step']) / of['area']) / (float(o['Step']) / o['area'])) ]
        }
    )
    df.set_index('steps', inplace=True) # just to remove index column
    return df

class BatchCoveragePathPlan(CoveragePathPlan):

    def __init__(self, width=40, height=40, robot_count = 8, map = '', obstacle_free = False, depth= 1, position_seed = None, model_seed = None, map_seed = None):
        super().__init__(width, height, robot_count, map, obstacle_free, depth, position_seed, model_seed, map_seed)

        self.datacollector = DataCollector(
            model_reporters={
                "Max visited": get_max_visited_cell,
                "Solved": check_final_result,
                "wstep": get_wvisits,
                "area": 'area'
            },
            # agent_reporters={"first visits": lambda x: {'value': x.first_visits, 'color': x.color}},
            # agent_reporters={"first visits": lambda x: x.first_visits},
        )


if __name__ == "__main__":
    
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    robot_count = [3,6,9,12]
    depths = [1,2,3]
    iterations = 3
    max_steps = 10000
    expriment_name = 'final7'
    maps_folder = 'final7'
    

    def dir_path(string):
        if os.path.isdir(string):
            return string
        else:
            raise NotADirectoryError(string)
    
    parser = argparse.ArgumentParser(
        prog="Batch run",
        description="This program executes batch run with the given argumens."
    )
    parser.add_argument("--path", type=dir_path)
    parser.add_argument("-r", "--Robots", nargs='+', type=int, help="List of number of robots.")
    parser.add_argument("-d", "--Depths", nargs='+', type=int, help="List of depth of view of the robots.")
    parser.add_argument("-i", "--Iterations", type=int, help="Number of interations each parameters set is executed.")
    parser.add_argument("-s", "--Max_Steps", type=int, help="halts the simulation if steps passes this number")
    args = parser.parse_args()

    if args.Robots:
        robot_count = args.Robots
    if args.Depths:
        depths = args.Depths
    if args.Iterations:
        iterations = args.Iterations
    if args.Max_Steps:
        max_steps = args.Max_Steps
    if args.path:
        path = args.path

    maps = list(glob.glob(f'maps\\{maps_folder}\\*.png'))

    br_params = {
        "robot_count": robot_count,
        "map": maps,
        'depth': depths,
    }
    data = batch_run_with_rngs(
            BatchCoveragePathPlan,
            br_params,
            max_steps=max_steps,
            iterations=iterations,
            display_progress=True
        )
    br_df = pd.DataFrame(data)
    br_df = br_df.groupby(['robot_count','map','depth', 'iteration']).apply(merge) 

    if not os.path.exists('results'):
        os.mkdir('results')
    br_df.to_csv(f'results\\{expriment_name}.csv')
    print('find results at: ', f'{expriment_name}.csv')
