from convergance import Simulation
from convergance_actor_generator import AutomaticGenerator
from convergance_actor_disposer import Disposer
from convergance_actor_delay import Delay
from convergance_actor_queue import Queue
from convergance_entity import Entity
from convergance_actor_probe import ActorProbe
from convergance_actor_branch import Branch
from convergance_random_number import NORMAL, UNIFORM, RANDINT, TRIANGULAR, NumberGenerator
from convergance_statistic import drawProbs, drawLeaveEnter

INTERVAL_RATE = NumberGenerator(UNIFORM, a=1, b=4)
DELAY_RATE_3 = NumberGenerator(TRIANGULAR, low=6, high=16, mode=10)
DELAY_RATE_2 = NumberGenerator(UNIFORM, a=2, b=4)
DELAY_RATE_1 = NumberGenerator(UNIFORM, a=0, b=4)

MAX_ENTITIES = 100000

d1 = Disposer()
d1.logs = False
d1.deleteentityfrommemory = False

########################################################

dl4 = Delay(d1, DELAY_RATE_1.next, None, 1)
dl4.name = 'Delay 4'
dl4.logs = False

pr6 = ActorProbe(dl4)
pr6.name = 'Probe Delay 4'
dl4.actorprobe = pr6

pr7 = ActorProbe(dl4)
pr7.name = 'Global Probe'
pr7.calculatenumentities = True
dl4.actorleaveprobe = pr7


q4 = Queue([dl4])
q4.name = 'Queue 4'
q4.logs = False

pr5 = ActorProbe(q4)
pr5.name = 'Probe Queue 4'
q4.actorprobe = pr5

########################################################

dl3 = Delay(q4, DELAY_RATE_2.next, None, 0)
dl3.name = 'Delay 3'
dl3.logs = False

pr4 = ActorProbe(dl3)
pr4.name = 'Probe Delay 3'
dl3.actorprobe = pr4

q3 = Queue([dl3])
q3.name = 'Queue 3'
q3.logs = False

pr3 = ActorProbe(q3)
pr3.name = 'Probe Queue 3'
q3.actorprobe = pr3

########################################################

dl2 = Delay(q4, DELAY_RATE_3.next, None, 5)
dl2.name = 'Delay 2'
dl2.logs = False

pr2 = ActorProbe(dl2)
pr2.name = 'Probe Delay 2'
dl2.actorprobe = pr2

q2 = Queue([dl2])
q2.name = 'Queue 2'
q2.logs = False

pr1 = ActorProbe(q2)
pr1.name = 'Probe Queue 2'
q2.actorprobe = pr1

########################################################

branchFunction = NumberGenerator(RANDINT, a=0, b=1)
b1 = Branch([q3, q2], branchFunction.next)

b1.actorenterprobe = pr7

g1 = AutomaticGenerator(b1, Entity, None, INTERVAL_RATE.next, MAX_ENTITIES)
g1.logs = False

sim = Simulation()
sim.logs = False

sim.addactor(g1)
sim.addactor(b1)
sim.addactor(d1)
sim.addactor(q2)
sim.addactor(dl2)
sim.addactor(q3)
sim.addactor(dl3)
sim.addactor(q4)
sim.addactor(dl4)

sim.addprobe(pr1)
sim.addprobe(pr2)
sim.addprobe(pr3)
sim.addprobe(pr4)
sim.addprobe(pr5)
sim.addprobe(pr6)
sim.addprobe(pr7)

sim.start()

drawProbs(pr1.calculatestatistics()[1], sim.tick, 'Customer Service Queue')
####drawProbs(pr3.calculatestatistics()[1], sim.tick, 'queue 3')
drawLeaveEnter(pr4.enters, 'Self Service Enters')
drawProbs(pr4.calculatestatistics()[1], sim.tick, 'Self Service Timeline')

drawProbs(pr5.calculatestatistics()[1], sim.tick, 'End Queue Timeline')

ne = pr2.calculatestatistics()[1]
#print(ne)
numz = 0
for i in range(1, len(ne)):
    if (ne[i-1][1] < 5):
        numz += (ne[i][0] - ne[i-1][0]) * (1 - ne[i][1] / 5)
if (ne[len(ne)-1][1] < 5):
    numz += (sim.tick - ne[len(ne)-1][0]) * (1 - ne[len(ne)-1][1] / 5)
utilization = 1 - (numz / sim.tick)

print("Customer Service Utilization:", utilization)
print("Customer Service Queue Utilization:", pr1.calculatestatistics()[0])
print("End Queue Utilization:", pr5.calculatestatistics()[0])
print("End Server Utilization:", pr6.calculatestatistics()[0])
k = 0
for i in d1.entities:
    k += i.disposationtick - i.generationick

k = k / len(d1.entities)

print("Average System Time:", k)
t = pr7.calculatestatistics()[1]

yt = 0
for i in range(1, len(t)):
    yt += (t[i][0] - t[i-1][0]) * t[i][1]
yt /= sim.tick

print("Average Count in System:", yt)

print("Arrival Rate:", MAX_ENTITIES/sim.tick)
