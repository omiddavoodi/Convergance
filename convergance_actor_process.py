from convergance_actor import Actor

class Process(Actor):

    def __init__(self, destination, function):
        Actor.__init__(self)
        self.destination = destination
        self.function = function
        self.name = "Process"
        
    def act(self, entity, data=None):
        function(entity)
        Actor.leave(self, entity)
        self.destination.enter(entity)

    def enter(self, entity):
        if (self.logs):
            print(self.name + ": Processed at Tick:" + str(self.simulation.tick))
        
        Actor.enter(self, entity)
        self.act(entity)
