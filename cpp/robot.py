from mesa import Agent



class Robot(Agent):
    def __init__(self, id, pos, model, planner):
        super().__init__(id, model)
        print(pos)
        self.x, self.y = pos
        self.planner = planner
        self.color = "#"+''.join([self.random.choice('0123456789ABCDEF') for j in range(6)])

    @property
    def cell(self):
        return self.model.grid[self.pos][0]

    def step(self):
        destination = self.planner.next_destination(self)
        if destination != None:
            self.model.grid.move_agent(self, destination.pos)
            destination.incrementVisitCount()
            

