from cpp.planners.greedy import GreedyPlanner
from cpp.utils import angle_between

class LgreedyPlanner(GreedyPlanner):

    def __init__(self, depth=1):
        super().__init__(depth)

    def get_available_neighbors(self, grid, current_pos, prev_pos, ignoreRobots):
        all_moves = super().get_available_neighbors(grid, current_pos, prev_pos, ignoreRobots)
        possible_moves = [cell for cell in all_moves if self.less_than_90_degree(prev_pos, current_pos, cell)]
        return possible_moves

    def less_than_90_degree(self, prev_pos, current_pos, destination):
        current_heading = (current_pos[0] - prev_pos[0], current_pos[1] - prev_pos[1])
        new_heading = (destination.x - current_pos[0], destination.y - current_pos[1])
        turn_angle = angle_between(current_heading, new_heading)
        return turn_angle < 90
