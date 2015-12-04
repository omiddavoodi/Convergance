from convergance import Simulation
from convergance_actor_generator import AutomaticGenerator
from convergance_actor_disposer import Disposer
from convergance_actor_delay import Delay
from convergance_actor_queue import Queue
from convergance_entity import Entity
from convergance_actor_probe import ActorProbe
from convergance_random_number import NORMAL, UNIFORM, RANDINT, TRIANGULAR, NumberGenerator
from convergance_statistic import drawProbs

INTERVAL_RATE = NumberGenerator(UNIFORM, a=3, b=4)
DELAY_RATE_1 = NumberGenerator(TRIANGULAR, low=5, high=6, mode=9)
DELAY_RATE_2 = NumberGenerator(UNIFORM, a=1, b=2)

d1 = Disposer()
d1.logs = True

dl1 = Delay(d1, DELAY_RATE_1.next, None, 1)
dl1.name = 'Delay 2'
dl1.logs = True

pr1 = ActorProbe(dl1)
pr1.name = 'Probe Delay 2'
dl1.actorprobe = pr1

q1 = Queue([dl1])
q1.name = 'Queue 2'
q1.logs = True

pr2 = ActorProbe(q1)
pr2.name = 'Probe Queue 2'
q1.actorprobe = pr2

dl2 = Delay(q1, DELAY_RATE_2.next, None, 1)
dl2.name = 'Delay 1'
dl2.logs = True

pr3 = ActorProbe(dl2)
pr3.name = 'Probe Delay 1'
dl2.actorprobe = pr3

q2 = Queue([dl2])
q2.name = 'Queue 1'
q2.logs = True

pr4 = ActorProbe(q2)
pr4.name = 'Probe Queue 1'
q2.actorprobe = pr4

g1 = AutomaticGenerator(q2, Entity, None, INTERVAL_RATE.next, 1000)
g1.logs = True

sim = Simulation()
sim.logs = True

sim.addactor(d1)
sim.addactor(dl1)
sim.addactor(q1)
sim.addactor(dl2)
sim.addactor(q2)
sim.addactor(g1)

sim.addprobe(pr1)
sim.addprobe(pr2)
sim.addprobe(pr3)
sim.addprobe(pr4)

sim.start()

drawProbs(pr2.calculatestatistics()[1], sim.tick, 'queue 1')
drawProbs(pr4.calculatestatistics()[1], sim.tick, 'queue 2')
drawProbs(pr1.calculatestatistics()[1], sim.tick, 'delay 1')
drawProbs(pr3.calculatestatistics()[1], sim.tick, 'delay 2')

print("Queue 1 Utilization:", pr2.calculatestatistics()[0])
print("Queue 2 Utilization:", pr4.calculatestatistics()[0])
print("Delay 1 Utilization:", pr1.calculatestatistics()[0])
print("Delay 2 Utilization:", pr3.calculatestatistics()[0])

