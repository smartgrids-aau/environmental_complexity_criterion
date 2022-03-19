from mesa import Agent


class Cell(Agent):
    """Represents a single cell in the simulation."""

    def __init__(self, pos, isObstacle, model):
        """
        Create a cell, in the given state, at the given x, y position.
        """
        super().__init__(pos, model)
        self.x, self.y = pos
        self.visitCount = 0
        self.isObstacle = isObstacle
        self._nextState = None
        self.isConsidered = False

    @property
    def isVisited(self):
        return self.visitCount > 0

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y))

    @property
    def content(self):
        return self.model.grid.get_cell_list_contents((self.x, self.y))

    @property
    def isEmpty(self):
        return (not self.isObstacle) and (len(self.content) == 1)

    def step(self):
        pass

    def incrementVisitCount(self):
        self.visitCount += 1
                    