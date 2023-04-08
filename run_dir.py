# Sample command:
# > python run_dir.py --path <PATH_TO_PNGs_DIR> -r 9 12 15 -d 3 6 9 -i 10 -s 1000
#             *******all arguments are optional*******

import argparse
import glob
import os
import pandas as pd
from batch_run import BatchCoveragePathPlan, merge
from cpp.batchrunner import batch_run_with_rngs
from itertools import groupby

if __name__ == "__main__":
    
    path = os.path.dirname(os.path.realpath(__file__))
    robot_count = [9, 12, 15]
    depths = [3,6,9]
    iterations = 3
    max_steps = 10000

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

    maps = list(glob.glob(path + '\\*.png'))

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

    br_df.to_csv(path + '\\result.csv')
