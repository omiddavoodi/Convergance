from convergance_actor import Actor

class Generator(Actor):
    
    def __init__(self, destination, entitytype, entitycreationdata, intervalfunction, maxentities=0):
        Actor.__init__(self)
        self.destination = destination
        self.entitytype = entitytype
        self.entitycreationdata = entitycreationdata
        self.intervalfunction = intervalfunction
        self.maxentities = maxentities
        self.entitiescreated = 0
        self.name = "Generator"

    def start(self):
        Actor.start(self)
        self.simulation.eventmanager.addevent(self.simulation.tick + self.intervalfunction(), self.create)
    
    def create(self):
        if (self.maxentities == 0 or (self.entitiescreated < self.maxentities)):
            self.entitiescreated += 1
            ent = self.entitytype(self.entitycreationdata)
            if (self.logs):
                print(self.name + ": Created Entity at Tick:" + str(self.simulation.tick))
            
            if (self.actorprobe):
                self.actorprobe.logleave(self.simulation.tick)
            
            self.destination.enter(ent)
            self.simulation.eventmanager.addevent(self.simulation.tick + self.intervalfunction(), self.create)

                    
    def act(self, entity, data=None):
        print("Error: Generator should not have an entity inside")
        self.simulation.error = True

    def enter(self, entity):
        print("Error: Generator cannot be a destination")
        self.simulation.error = True
