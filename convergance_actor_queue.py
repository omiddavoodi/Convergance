from convergance_actor import Actor

class Queue(Actor):

    def __init__(self, destinations):
        Actor.__init__(self)
        self.destinations = destinations
        self.name = "Queue"

    def start(self):
        Actor.start(self)
        for i in self.destinations:
            i.registerforleavecalback(self.leavecallback)
    
    def leavecallback(self, data):
        for i in self.destinations:
            if (i.accepts_new):
                if (len(self.entities)):
                    self.act(self.entities[-1], i)
        

    def act(self, entity, data=None):
        if (self.logs):
            print(self.name + ": Dequeued to " + data.name + " at Tick:" + str(self.simulation.tick))
        
        Actor.leave(self, entity)
        data.enter(entity)

    def enter(self, entity):
        if (self.logs):
            print(self.name + ": Enqueued at Tick:" + str(self.simulation.tick))

        Actor.enter(self, entity)
        for i in self.destinations:
            if (i.accepts_new):
                if (len(self.entities)):
                    self.act(self.entities[-1], i)
