class Actor:
    name = "Unnamed"

    def __init__(self):
        self.entities = []
        self.accepts_new = True
        self.callbackleave = []
        self.simulation = None
        self.logs = False
    
    def act(self, entity, data=None):
        pass

    def enter(self, entity):
        self.entities.append(entity)

    def leave(self, entity):
        self.entities.remove(entity)
        for i in self.callbackleave:
            i(entity)

    def start(self):
        pass

    def registerforleavecalback(self, actorcallback):
        self.callbackleave.append(actorcallback)
