class Entity:
    
    actor = None
    tickenteredactor = 0
    
    def __init__(self, data):
        self.generationick = 0
        self.disposationtick = 0
        self.simulation = None
        
    def generate(self, tick, simulation):
        self.generationick = tick
        self.simulation = simulation
        
    def dispose(self, tick):
        self.disposationtick = tick
        
    def onEnter(self, actor):
        pass

    def onLeave(self, actor):
        pass
