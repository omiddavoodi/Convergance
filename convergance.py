from convergance_event_manager import EventManager

class Simulation:
    
    
    def __init__(self):
        self.tick = 0
        self.maxtick = 0
        self.eventmanager = EventManager()
        self.messages = []
        self.error = False
        self.finished = False
        self.actors = []
        self.agents = []
        self.logs = False

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
        for i in self.messages:
            if i[2] is None:
                for j in agents:
                    j.onMessage(i[0], i[1])
            else:
                i[2].onMessage(i[0], i[1])
        self.messages.clear()
        
        #print('loop')
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

    def addagent(self, agent):
        self.agents.append(agent)
        agent.simulation = self
    
    def addprobe(self, probe):
        probe.simulation = self

    def addmessage(self, m):
        self.messages.append(m)
