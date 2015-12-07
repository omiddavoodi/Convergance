from convergance_actor import Actor

class Generator(Actor):
    
    def __init__(self, destination, entitytype, entitycreationdata, maxentities=0, batch=False, batchfunction=None):
        Actor.__init__(self)
        self.destination = destination
        self.entitytype = entitytype
        self.entitycreationdata = entitycreationdata
        self.batch = batch
        self.batchfunction = batchfunction
        self.maxentities = maxentities
        self.entitiescreated = 1
        self.name = "Generator"

    def start(self):
        Actor.start(self)
        
    def create(self):
        if (not self.batch):
            num = 1
        else:
            num = self.batchfunction(self.simulation)
        for i in range(num):
            if (self.maxentities == 0 or (self.entitiescreated < self.maxentities)):
                self.entitiescreated += 1
                ent = self.entitytype(self.entitycreationdata)
                ent.generate(self.simulation.tick)
                if (self.logs):
                    print(self.name + ": Created Entity at Tick:" + str(self.simulation.tick))
                
                if (self.actorprobe):
                    self.actorprobe.logleave(self.simulation.tick, ent)
                
                self.destination.enter(ent)
            
                    
    def act(self, entity, data=None):
        print("Error: Generator should not have an entity inside")
        self.simulation.error = True

    def enter(self, entity):
        print("Error: Generator cannot be a destination")
        self.simulation.error = True

class AutomaticGenerator(Generator):

    def __init__(self, destination, entitytype, entitycreationdata, intervalfunction, maxentities=0, batch=False, batchfunction=None):
        Generator.__init__(self, destination, entitytype, entitycreationdata, maxentities, batch, batchfunction)
        self.intervalfunction = intervalfunction
        

        self.name = "AutomaticGenerator"

    def start(self):
        Generator.start(self)
        self.simulation.eventmanager.addevent(self.simulation.tick + self.intervalfunction(), self.create)

    def create(self):
        if (self.maxentities == 0 or (self.entitiescreated < self.maxentities)):
            self.simulation.eventmanager.addevent(self.simulation.tick + self.intervalfunction(), self.create)
        Generator.create(self)  
