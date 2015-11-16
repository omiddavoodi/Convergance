class ActorProbe:
    
    actor = None
    enters = []
    leaves = []
    delays = []
    numentities = {}
    simulation = None
    
    def __init__(self, actor):
        self.actor = actor
        
    def logenter(self, tick, entity):
        self.enters.append(tick)
        entity.tickenteredactor = tick
        self.numentities[tick] = len(self.actor.entities)
        
    def logleave(self, tick, entity):
        self.leaves.append(tick)
        self.delays.append(tick - entity.tickenteredactor)
        self.numentities[tick] = len(self.actor.entities)