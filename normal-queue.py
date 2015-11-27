from convergance import Simulation
from convergance_actor_generator import AutomaticGenerator
from convergance_actor_disposer import Disposer
from convergance_actor_delay import Delay
from convergance_actor_queue import Queue
from convergance_entity import Entity
from convergance_actor_probe import ActorProbe
from convergance_random_number import NORMAL, UNIFORM, RANDINT, TRIANGULAR, NumberGenerator
from convergance_statistic import drawProbs


# Entity Generation Random
# INTERVAL_RATE = NumberGenerator(NORMAL, mu=1, sigma=3)
INTERVAL_RATE = NumberGenerator(UNIFORM, a=3, b=6)

# Delay Random
DELAY_RATE_BAKER = NumberGenerator(UNIFORM, a=1, b=2)
DELAY_RATE_ABLE = NumberGenerator(TRIANGULAR, low=2, high=3, mode=6)

# DELAY_RATE_BAKER = NumberGenerator(RANDINT, a=1, b=7)
# DELAY_RATE_ABLE = NumberGenerator(RANDINT, a=1, b=5)

d1 = Disposer()
d1.logs = True

# 1 is Able's maximum simultanious clients
dl1 = Delay(d1, DELAY_RATE_ABLE.next, None, 1)
dl1.name = 'Delay'
dl1.logs = True


q1 = Queue([dl1])
q1.logs = True

pr1 = ActorProbe(q1)
pr1.name = 'Queue Probe'
q1.actorprobe = pr1

pr2 = ActorProbe(dl1)
pr2.name = 'Delay Probe'
dl1.actorprobe = pr2


g1 = AutomaticGenerator(q1, Entity, None, INTERVAL_RATE.next, 200)
g1.logs = True

sim = Simulation()
sim.logs = True

sim.addactor(d1)
sim.addactor(q1)
sim.addactor(dl1)
sim.addactor(g1)

sim.addprobe(pr1)
sim.addprobe(pr2)

sim.start()

drawProbs(pr1.calculatestatistics()[1], sim.tick, 'queue')
drawProbs(pr2.calculatestatistics()[1], sim.tick, 'delay')

print("Queue Utilization:", pr1.calculatestatistics()[0])
print("Delay Utilization:", pr2.calculatestatistics()[0])

