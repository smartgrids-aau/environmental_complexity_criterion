from ast import List
from cpp.cell import Cell
from cpp.planner import Planner
from cpp.robot import Robot


class GreedyPlanner(Planner):

    def next_destination(self, robot: Robot, choices: list[Cell]) -> Cell:
        min_value = min(choice.visitCount for choice in choices)
        best_choices = [cell for cell in choices if cell.visitCount == min_value]
        destination = robot.random.choice(best_choices)
        return destination

