from cpp.cell import Cell
from cpp.planner import Planner
from cpp.robot import Robot


class GreedyPlanner(Planner):

    def next_destination(self, robot: Robot) -> Cell:
        choices = self.get_empty_neighbors(robot.model.grid, robot.pos)
        destination = None
        if len(choices) > 0:
            min_value = min(choice.visitCount for choice in choices)
            best_choices = [cell for cell in choices if cell.visitCount == min_value]
            destination = robot.random.choice(best_choices)
        return destination

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


