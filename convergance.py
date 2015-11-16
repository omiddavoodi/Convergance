from convergance_event_manager import EventManager

class Simulation:
    tick = 0
    maxtick = 0
    eventmanager = EventManager()
    error = False
    finished = False
    actors = []
    logs = False
    
    def __init__(self):
        pass

    def start(self):
        if (self.logs):
            print("Simulation started: " + str(self.tick))
        
        for i in self.actors:
            i.start()

        while(True):
            if (not self.finished and not self.error and (self.maxtick == 0 or (self.tick < self.maxtick))):
                self.loop()
            
            else:
                break

        if (self.logs):
            print("Simulation finished: " + str(self.tick))

    def loop(self):
        event = self.eventmanager.getevent()
        if event == None:
            self.finished = True
            return

        self.tick = event[0]
        if (len(event) == 2):
            event[1]()
        
        else:
            event[1](event[2])
            
    def addactor(self, actor):
        self.actors.append(actor)
        actor.simulation = self
    
    def addprobe(self, probe):
        probe.simulation = self