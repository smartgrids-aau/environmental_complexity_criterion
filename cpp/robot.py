from mesa import Agent


class Robot(Agent):
    def __init__(self, id, pos, model):
        super().__init__(id, model)
        print(pos)
        self.x, self.y = pos
        self.color = "#"+''.join([self.random.choice('0123456789ABCDEF') for j in range(6)])

    @property
    def neighbors(self):
        return self.model.grid.get_neighborhood(self.pos, False, False)

    @property
    def cell(self):
        return self.model.grid[self.pos][0]

    def step(self):
        destination = self.random.choice(self.neighbors)

        self.model.grid.move_agent(self, destination)
        self.model.grid[destination][0].incrementVisitCount()
            

