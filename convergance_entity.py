class Entity:
    
    actor = None
    tickenteredactor = 0
    
    def __init__(self, data):
        self.generationick = 0
        self.disposationtick = 0
        
    def generate(self, tick):
        self.generationick = tick

    def dispose(self, tick):
        self.disposationtick = tick
            
