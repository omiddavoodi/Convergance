from convergance_actor import Actor

class EventGenerator(Actor):

    def __init__(self, event, intervalfunction, maxevents=0):
        Actor.__init__(self)
        self.event = event
        self.eventsgenerated = 1
        self.maxevents = maxevents
        self.intervalfunction = intervalfunction
        self.name = "EventGenerator"

    def start(self):
        Actor.start(self)
        self.simulation.eventmanager.addevent(self.simulation.tick + self.intervalfunction(), self.generate)

    def generate(self):
        if (self.maxevents == 0 or self.eventsgenerated < self.maxevents):
            if (self.logs):
                    print(self.name + ": Generate Event at Tick:" + str(self.simulation.tick))
                
            self.simulation.eventmanager.addevent(self.simulation.tick, self.event)
            self.simulation.eventmanager.addevent(self.simulation.tick + self.intervalfunction(), self.generate)
    
    def act(self, entity, data=None):
        print("Error: EventGenerator should not have an entity inside")
        self.simulation.error = True

    def enter(self, entity):
        print("Error: EventGenerator cannot be a destination")
        self.simulation.error = True
        
