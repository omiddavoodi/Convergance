from convergance_actor import Actor

class Delay(Actor):

    def __init__(self, destination, delayinterval, delayintervaldata=None, maxentities=0):
        Actor.__init__(self)
        self.destination = destination
        self.delayinterval = delayinterval
        self.delayintervaldata = delayintervaldata
        self.maxentities = maxentities
        self.name = "Delay"
        
    def enddelay(self, data):
        Actor.leave(self, data)
        if (self.maxentities != 0 and self.maxentities > len(self.entities)):
            self.accepts_new = True
        
        if (self.logs):
            print(self.name + ": Delay ended at Tick:" + str(self.simulation.tick))
        
        self.destination.enter(data)
            
    def act(self, entity, data=None):
        interval = self.delayinterval(self.delayintervaldata)
        if (self.logs):
            print(self.name + ": Delays Entity for interval " + str(interval) + " at Tick:" + str(self.simulation.tick))
        
        self.simulation.eventmanager.addevent(self.simulation.tick + interval, self.enddelay, entity)
                

    def enter(self, entity):
        if (not self.accepts_new):
            print("Error: Entered into Delay when accepts_new = False")
            self.simulation.error = True
            return
        
        Actor.enter(self, entity)
        self.act(entity)
        if (self.maxentities != 0 and self.maxentities <= len(self.entities)):
            self.accepts_new = False
