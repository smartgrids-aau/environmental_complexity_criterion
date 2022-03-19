from cpp.cell import Cell
from cpp.planner import Planner
from cpp.robot import Robot


class GreedyPlanner(Planner):

    def next_destination(self, robot: Robot) -> Cell:
        choices = self.get_empty_neighbor_cells(robot)
        if len(choices) > 0:
            min_value = min(choice.visitCount for choice in choices)
            destination = robot.random.choice([cell for cell in choices if cell.visitCount == min_value])
            return destination
        return None

    def get_empty_neighbor_cells(self, robot):
        neighborsContent = robot.model.grid.get_neighbors(robot.pos, False, False)
        return list(filter(lambda grid: isinstance(grid, Cell) and grid.isEmpty, neighborsContent))