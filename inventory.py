from convergance import Simulation
from convergance_actor_generator import Generator
from convergance_actor_disposer import Disposer
from convergance_actor_queue import Queue
from convergance_entity import Entity
from convergance_actor_probe import ActorProbe
from convergance_actor_branch import Branch
from convergance_actor_storage import Storage
from convergance_actor_event_generator import EventGenerator
from convergance_random_number import NORMAL, UNIFORM, RANDINT, TRIANGULAR, NumberGenerator
from convergance_statistic import drawProbs, drawLeaveEnter

UNSOLD = 0
SOLD = 1
MIN_STORAGE_ENTITIES = 5
INIT_STORGAE_ENTITIES = 20
MAX_STORAGE_ENTITIES = 20
STORAGE_CHECK_INTERVAL = 3
DAY_INTERVAL = 500
BUY_RATE = NumberGenerator(UNIFORM, a=4, b=12)
BUY_INTERVAL = NumberGenerator(UNIFORM, a=0, b=30)

class Newspaper(Entity):
    def __init__(self, data):
        Entity.__init__(self, data)
        self.status = SOLD


d1 = Disposer()
d1.name = "Bought Newspapers"

d2 = Disposer()
d2.name = "Recycled Newspapers"

pr1 = ActorProbe(d1)
pr1.name = 'Bought Newspapers Probe'
d1.actorprobe = pr1

pr2 = ActorProbe(d2)
pr2.name = 'Recycled Newspapers Probe'
d2.actorprobe = pr2

def branchFunction(entity):
    global SOLD
    if entity.status == SOLD:
        return 0
    return 1

b1 = Branch([d1, d2], branchFunction)

s1 = Storage(b1, [Newspaper(None) for i in range(INIT_STORGAE_ENTITIES)])

pr3 = ActorProbe(s1)
pr3.name = 'Storage Probe'
s1.actorprobe = pr3


batchCount = 0
def generatorBatchNumberFunction(simulation):
    global batchCount
    return batchCount

g1 = Generator(s1, Newspaper, None,0, True, generatorBatchNumberFunction)
pr4 = ActorProbe(g1)
pr4.name = 'Generator Probe'
g1.actorprobe = pr4

def regularStorageChecks():
    global s1
    global g1
    global batchCount
    if (len(s1.entities) < MIN_STORAGE_ENTITIES):
        batchCount = MAX_STORAGE_ENTITIES - len(s1.entities)
        g1.create()

def regularStorageChecksInterval():
    global STORAGE_CHECK_INTERVAL
    return STORAGE_CHECK_INTERVAL

e1 = EventGenerator(regularStorageChecks, regularStorageChecksInterval)
e1.name = "Storage Check Event"

def dayCycle():
    global s1
    global UNSOLD
    for i in s1.entities:
        i.status = UNSOLD
    s1.release(-1)

def dayInterval():
    global DAY_INTERVAL
    return DAY_INTERVAL

e2 = EventGenerator(dayCycle, dayInterval)
e2.name = "Day Cycle Event"

def buyEvent():
    global s1
    global BUY_RATE

    s1.release(int(BUY_RATE.next()))

e3 = EventGenerator(buyEvent, BUY_INTERVAL.next)
e3.name = "Buy Event"

sim = Simulation()
sim.maxtick = 5000
sim.logs = True

sim.addactor(d1)
sim.addactor(d2)
sim.addactor(b1)
sim.addactor(s1)
sim.addactor(g1)
sim.addactor(e1)
sim.addactor(e2)
sim.addactor(e3)

sim.addprobe(pr1)
sim.addprobe(pr2)
sim.addprobe(pr3)

sim.start()

drawLeaveEnter(pr1.enters, 'Sold')
drawLeaveEnter(pr2.enters, 'Recycled')
drawLeaveEnter(pr3.failures, 'Lost Opportunity')
#drawLeaveEnter(pr4.leaves, 'Newspapers Generated')
print("Sold:",len(pr1.enters))
print("Recycled:",len(pr2.enters))
print("Lost Opportunity:",len(pr3.failures))
print("Total Newspapers Generated:",len(pr4.leaves))
