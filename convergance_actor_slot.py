from convergance_actor import Actor

class Slot(Actor):
    
    def __init__(self):
        Actor.__init__(self)
        self.name = 'Slot'
        
    def start(self):
        pass

    def act(self, entity, data=None):
        if (self.logs):
            print(self.name + ": Stored Entity at Tick:" + str(self.simulation.tick))
        
    def enter(self, entity):
        Actor.enter(self, entity)
        self.act(entity)
