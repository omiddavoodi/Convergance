from convergance_actor import Actor

class Storage(Actor):

    def __init__(self, destination, initialinventory=[]):
        Actor.__init__(self)
        self.destination = destination
        self.initialinventory = initialinventory
        self.name = "Storage"

    def start(self):
        Actor.start(self)
        for i in self.initialinventory:
            self.entities.append(i)

    def release(self, count):
        if (count > 0):
            if self.actorprobe:
                for i in range(0,count-len(self.entities),1):
                    self.actorprobe.logfailure(self.simulation.tick)
            if (self.logs):
                print(self.name + ": Released " + str(min(len(self.entities), count)) + " items to " + self.destination.name + " at Tick:" + str(self.simulation.tick))
            
            ret = self.entities[:count]
            for i in ret:
                self.act(i, self.destination)
        else:
            if (self.logs):
                print(self.name + ": Released all items to " + self.destination.name + " at Tick:" + str(self.simulation.tick))
            
            for i in self.entities:
                self.act(i, self.destination)
        
    def act(self, entity, data=None):
        
        Actor.leave(self, entity)
        data.enter(entity)

    def enter(self, entity):
        if (self.logs):
            print(self.name + ": Stored at Tick:" + str(self.simulation.tick))

        Actor.enter(self, entity)
