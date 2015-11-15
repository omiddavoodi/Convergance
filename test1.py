from convergance import Simulation
from convergance_actor_generator import Generator
from convergance_actor_disposer import Disposer
from convergance_actor_branch import Branch
from convergance_actor_delay import Delay
from convergance_entity import Entity
from randomNumber import RANDINT, NumberGenerator
import random

a = NumberGenerator(RANDINT, a=1, b=2)
def randomInterval():
    return random.randint(1,2)

def branchFunction(data):
    return random.randrange(0,2)

def delayFunction(data):
    return random.randrange(2,5)

d1 = Disposer()
d1.name = "Disposer1"
d1.logs = True
d2 = Disposer()
d2.name = "Disposer2"
d2.logs = True
dl1 = Delay(d2, delayFunction)
dl1.name = "Delay1"
dl1.logs = True
b1 = Branch([d1, dl1], branchFunction)
b1.name = "Branch1"
b1.logs = True
g1 = Generator(b1, Entity, None, randomInterval, 20)
g1.name = "MyGenerator"
g1.logs = True
sim = Simulation()
sim.logs = True

sim.addactor(d1)
sim.addactor(d2)
sim.addactor(dl1)
sim.addactor(b1)
sim.addactor(g1)

sim.start()
