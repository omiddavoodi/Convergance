from convergance import Simulation
from convergance_actor_generator import Generator
from convergance_actor_disposer import Disposer
from convergance_actor_branch import Branch
from convergance_actor_delay import Delay
from convergance_actor_queue import Queue
from convergance_entity import Entity
from randomNumber import NORMAL, UNIFORM, NumberGenerator

# Entity Generation Random
INTERVAL_RATE = NumberGenerator(NORMAL, mu=1, sigma=3)

# Delay Random
DELAY_RATE = NumberGenerator(UNIFORM, a=1, b=5)


d1 = Disposer()
d1.logs = True

# 1 is Able's maximum simultanious clients
dl1 = Delay(d1, DELAY_RATE.next, None, 1)
dl1.name = 'Able'
dl1.logs = True

# 1 is Baker's maximum simultanious clients
dl2 = Delay(d1, DELAY_RATE.next, None, 1)
dl2.name = 'Baker'
dl2.logs = True

q1 = Queue([dl1, dl2])
q1.logs = True

g1 = Generator(q1, Entity, None, INTERVAL_RATE.next, 30)
g1.logs = True

sim = Simulation()
sim.logs = True

sim.addactor(d1)
sim.addactor(q1)
sim.addactor(dl1)
sim.addactor(dl2)
sim.addactor(g1)

sim.start()
