from convergance_entity import Entity
from convergance_actor import Actor

class Agent (Entity):
    def __init__(self, data):
        Entity.__init__(self, data)
        self.name = "Agent"
        self.onenter = data['onenter']
        self.onleave = data['onleave']
        self.attributes = data['start']()
        
    def onMessage(self, message, sender):
        if (self.simulation.logs):
            print(self.name + " recieved message at tick " + str(self.simulation.tick))

    def sendMessage(self, message, target):
        self.simulation.addmessage((message, self, target))

    def propagateMessage(self, message):
        self.simulation.addmessage((message, self, None))

    def onEnter(self, actor):
        Entity.onEnter(self, actor)
        self.onenter(actor, self)

    def onLeave(self, actor):
        Entity.onLeave(self, actor)
        self.onleave(actor, self)

    def leaveActor(self, actor=None):
        if (actor == None):
            type(actor).leave(self.actor, self)
        else:
            try:
                type(actor).leave(actor, self)
            except:
                pass

    def enterActor(self, actor):
        type(actor).enter(actor, self)
