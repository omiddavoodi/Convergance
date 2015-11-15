from convergance_actor import Actor

class Branch(Actor):

    def __init__(self, branchactors, branchfunction):
        Actor.__init__(self)
        self.branchactors = branchactors
        self.branchfunction = branchfunction
        self.name = "Branch"
        
    def act(self, entity, data=None):
        Actor.leave(self, entity)
        nextactor = self.branchactors[self.branchfunction(data)]
        nextactor.enter(entity)

    def enter(self, entity):
        if (self.logs):
            print(self.name + ": Decided at Tick:" + str(self.simulation.tick))
        
        Actor.enter(self, entity)
        self.act(entity)
