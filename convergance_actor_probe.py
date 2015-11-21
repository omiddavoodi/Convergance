class ActorProbe:
    
    
    
    def __init__(self, actor):
        self.enters = []
        self.leaves = []
        self.delays = []
        self.numentities = {}
        self.actor = actor
        self.simulation = None
        self.logs = False
        self.name = "Probe1"
        
    def logenter(self, tick, entity):
        self.enters.append(tick)
        entity.tickenteredactor = tick
        self.numentities[tick] = len(self.actor.entities)
        if (self.logs):
            print("Logged Enter At " + str(tick) + " for " + self.name + " with len " + str(len(self.actor.entities)))
        
    def logleave(self, tick, entity):
        self.leaves.append(tick)
        self.delays.append(tick - entity.tickenteredactor)
        self.numentities[tick] = len(self.actor.entities)
        if (self.logs):
            print("Logged Leave At " + str(tick) + " for " + self.name + " with len " + str(len(self.actor.entities)))
    
    def calculatestatistics(self):
        ne = [i for i in self.numentities.items()]
        ne.sort()
        numz = 0
        for i in range(1, len(ne)):
            if (ne[i-1][1] == 0):
                numz += ne[i][0] - ne[i-1][0]
        if (ne[len(ne)-1][1] == 0):
            numz += self.simulation.tick - ne[len(ne)-1][0]
        utilization = 1 - (numz / self.simulation.tick)
        
        
        
        return utilization, ne
    