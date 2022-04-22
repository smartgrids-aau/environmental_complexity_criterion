import queue
from cpp.cell import Cell
from cpp.planner import Planner
from cpp.robot import Robot


class GreedyPlanner(Planner):

    def __init__(self, depth=1):
        self.depth = depth

    def next_destination(self, robot: Robot) -> Cell:
        choices = self.get_empty_neighbors(robot.model.grid, robot.pos)
        next_move = None
        q = queue.SimpleQueue()
        min_visit_count = 999999
        best_choices = []
        seen = {robot.pos:-1}


        for choice in choices:
            q.put({'path': [], 'current':choice, 'cost':0})
            seen[choice.pos] = 0
        
        while not q.empty():
            c = q.get()
            if c['current'].visitCount < min_visit_count:
                min_visit_count = c['current'].visitCount
                best_choices = [c]
            elif c['current'].visitCount == min_visit_count:
                best_choices.append(c)
            if len(c['path']) < self.depth:
                choices = self.get_nonObstacle_neighbors(robot.model.grid, c['current'].pos)
                for choice in choices:
                    if choice.pos not in seen or c['cost'] + c['current'].visitCount < seen[choice.pos]:
                        seen[choice.pos] = c['cost'] + c['current'].visitCount
                        appended_path = c['path'].copy()
                        appended_path.append(c['current'].pos)
                        q.put({'path': appended_path, 'current':choice, 'cost':c['cost']+ c['current'].visitCount})

        if len(best_choices) > 0:
            destination = robot.random.choice(best_choices)
            if len(destination['path']) == 0:
                next_move = robot.model.grid[destination['current'].pos][0]
            else:
                next_move = robot.model.grid[destination['path'][0]][0]
        return next_move

    def get_empty_neighbors(self, grid, pos):
        neighborsContent = grid.get_neighbors(pos, moore=False, include_center=False)
        # straight neighbors
        neighbors = list(filter(lambda content: isinstance(content, Cell) and content.isEmpty, neighborsContent))
        # diagonal neighbors
        for i in [pos[0]-1, pos[0]+1]:
            for j in [pos[1]-1, pos[1]+1]:
                if i in range(0, grid.height) and j in range(0, grid.width) and\
                    grid[i,j][0].isEmpty and grid[i, pos[1]][0].isEmpty and grid[pos[0], j][0].isEmpty:
                    neighbors.append(grid[i,j][0])
        return neighbors

    def get_nonObstacle_neighbors(self, grid, pos):
        neighborsContent = grid.get_neighbors(pos, moore=False, include_center=False)
        # straight neighbors
        neighbors = list(filter(lambda content: isinstance(content, Cell) and not content.isObstacle, neighborsContent))
        # diagonal neighbors
        for i in [pos[0]-1, pos[0]+1]:
            for j in [pos[1]-1, pos[1]+1]:
                if i in range(0, grid.height) and j in range(0, grid.width) and\
                    not grid[i,j][0].isObstacle and not grid[i, pos[1]][0].isObstacle and not grid[pos[0], j][0].isObstacle:
                    neighbors.append(grid[i,j][0])
        return neighbors


