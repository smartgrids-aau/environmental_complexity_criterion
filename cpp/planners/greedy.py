import queue
from cpp.cell import Cell
from cpp.planner import Planner
from cpp.robot import Robot


class GreedyPlanner(Planner):

    def __init__(self, depth=1):
        self.depth = depth

    def next_destination(self, robot: Robot) -> Cell:
        min_visit_count = 999999
        best_choices = []
        next_move = None

        current_cell = robot.model.grid[robot.pos][0]
        seen = {robot.pos: -current_cell.visitCount - 1}

        # path: path starting after robot position, INCLUDING last_cell
        # last_cell: last cell in the path
        # cost: sum of visitCount of all cells in path INCLUDING last_cell
        q = queue.SimpleQueue()
        q.put({'path': [], 'last_cell': current_cell, 'cost': 0})

        while not q.empty():
            expanding_path = q.get()

            if len(expanding_path['path']) > 0:
                if expanding_path['last_cell'].visitCount < min_visit_count:
                    min_visit_count = expanding_path['last_cell'].visitCount
                    best_choices = [expanding_path]
                elif expanding_path['last_cell'].visitCount == min_visit_count:
                    best_choices.append(expanding_path)

            if len(expanding_path['path']) <= self.depth:
                choices = self.get_available_neighbors(
                    grid=robot.model.grid,
                    pos=expanding_path['last_cell'].pos,
                    ignoreRobots=len(expanding_path['path']) > 0
                )
                for choice in choices:
                    if choice.pos not in seen or\
                            expanding_path['cost'] + choice.visitCount < seen[choice.pos]:
                        seen[choice.pos] = expanding_path['cost'] + choice.visitCount
                        appended_path = expanding_path['path'].copy()
                        appended_path.append(choice.pos)
                        q.put({
                            'path': appended_path,
                            'last_cell': choice,
                            'cost': expanding_path['cost'] + choice.visitCount
                        })

        if len(best_choices) > 0:
            best_destination = self.choose_best_path(best_choices, robot.random)
            next_move = robot.model.grid[best_destination['path'][0]][0]
        return next_move

    def get_available_neighbors(self, grid, pos, ignoreRobots):
        can_move_to = lambda cell: not cell.isObstacle if ignoreRobots else cell.isEmpty
        neighborsContent = grid.get_neighbors(pos, moore=False, include_center=False)
        # straight neighbors
        neighbors = list(filter(lambda content: isinstance(content, Cell) and
                                can_move_to(content), neighborsContent))
        # diagonal neighbors
        for i in [pos[0]-1, pos[0]+1]:
            for j in [pos[1]-1, pos[1]+1]:
                if i in range(0, grid.height) and j in range(0, grid.width) and\
                        can_move_to(grid[i, j][0]) and\
                        not grid[i, pos[1]][0].isObstacle and not grid[pos[0], j][0].isObstacle:
                    neighbors.append(grid[i, j][0])
        return neighbors

    def choose_best_path(self, best_choices, random):
        min_value = min(
            choice['cost'] - choice['last_cell'].visitCount for choice in best_choices
        )
        min_best_choices = [choice for choice in best_choices if choice['cost'] -
                            choice['last_cell'].visitCount == min_value]
        destination = random.choice(min_best_choices)
        return destination
