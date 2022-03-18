from mesa import Agent


class Robot(Agent):
    def __init__(self, id, pos, model):
        super().__init__(id, model)
        print(pos)
        self.x, self.y = pos
        self.color = "#"+''.join([self.random.choice('0123456789ABCDEF') for j in range(6)])

    @property
    def neighborhood(self):
        return self.model.grid.get_neighborhood(self.pos, False, False)

    @property
    def neighbors(self):
        return list(filter(lambda grid: self.get_cell(grid).isEmpty, self.model.grid.get_neighbors(self.pos, False, False)))

    def get_cell(self, grid):
        if grid is list:
            return grid[0] # todo find cell
        else:
            return grid

    @property
    def cell(self):
        return self.model.grid[self.pos][0]

    def step(self):
        destination = self.get_cell(self.random.choice(self.neighbors))

        self.model.grid.move_agent(self, destination.pos)
        destination.incrementVisitCount()
            

