from convergance_actor import Actor

class Disposer(Actor):
    
    def __init__(self):
        Actor.__init__(self)
        self.name = 'Disposer'
        
    def start(self):
        pass

    def act(self, entity, data=None):
        if (self.logs):
            print(self.name + ": Disposed Entity at Tick:" + str(self.simulation.tick))
        Actor.leave(self, entity)
        del entity

    def enter(self, entity):
        Actor.enter(self, entity)
        self.act(entity)
