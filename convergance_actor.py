class Actor:
    name = "Unnamed"
    
    def __init__(self):
        self.entities = []
        self.accepts_new = True
        self.callbackleave = []
        self.simulation = None
        self.logs = False
        self.actorprobe = None
        self.actorenterprobe = None
        self.actorleaveprobe = None
        self.metadata = None
    
    def act(self, entity, data = None):
        pass

    def enter(self, entity):
        entity.actor = self
        entity.tickenteredactor = self.simulation.tick
        self.entities.append(entity)
        if (self.actorprobe):
            self.actorprobe.logenter(self.simulation.tick, entity)
        if (self.actorenterprobe):
            self.actorenterprobe.logenter(self.simulation.tick, entity)
        entity.onEnter(self)

    def leave(self, entity):
        self.entities.remove(entity)
        entity.actor = None
        for i in self.callbackleave:
            i(entity)
        if (self.actorprobe):
            self.actorprobe.logleave(self.simulation.tick, entity)
        if (self.actorleaveprobe):
            self.actorleaveprobe.logleave(self.simulation.tick, entity)
        entity.onLeave(self)

    def start(self):
        pass

    def registerforleavecalback(self, actorcallback):
        self.callbackleave.append(actorcallback)
