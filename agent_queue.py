from convergance import Simulation
from convergance_actor_generator import AutomaticGenerator
from convergance_actor_disposer import Disposer
from convergance_actor_slot import Slot
from convergance_actor_delay import Delay
from convergance_actor_queue import Queue
from convergance_entity_agent import Agent
from convergance_actor_probe import ActorProbe
from convergance_random_number import NORMAL, UNIFORM, RANDINT, TRIANGULAR, NumberGenerator
from convergance_statistic import drawProbs



# Entity Generation Random
# INTERVAL_RATE = NumberGenerator(NORMAL, mu=1, sigma=3)
INTERVAL_RATE = NumberGenerator(UNIFORM, a=1, b=2)

# Delay Random
DELAY_RATE_BAKER = NumberGenerator(UNIFORM, a=1, b=2)
DELAY_RATE_ABLE = NumberGenerator(TRIANGULAR, low=2, high=8, mode=6)
DELAY_EAT = NumberGenerator(TRIANGULAR, low=10, high=20, mode=17)
DELAY_RATE_BAKER = NumberGenerator(UNIFORM, a=1, b=2)

# DELAY_RATE_BAKER = NumberGenerator(RANDINT, a=1, b=7)
# DELAY_RATE_ABLE = NumberGenerator(RANDINT, a=1, b=5)

s1 = Slot()

d1 = Delay(s1, DELAY_EAT.next, None)
d1.name = 'Eat'
#d1.logs = True

# Fast Food
dl1 = Delay(d1, DELAY_RATE_ABLE.next, None, 5)
dl1.name = 'Wait For Fast Food'
#dl1.logs = True

q1 = Queue([dl1])
q1.name = 'Fast Food Queue'
q1.metadata = {'quality': NumberGenerator(UNIFORM, a=3, b=6),
               'cost': NumberGenerator(UNIFORM, a=2, b=7)
               }
#q1.logs = True

pr1 = ActorProbe(q1)
pr1.name = 'Queue Probe'
q1.actorprobe = pr1

pr2 = ActorProbe(dl1)
pr2.name = 'Delay Probe'
dl1.actorprobe = pr2



# Hot Dog Stand
dl2 = Delay(d1, DELAY_RATE_ABLE.next, None, 5)
dl2.name = 'Wait For Hot Dog Stand'
#dl2.logs = True

q2 = Queue([dl2])
q2.name = 'Hot Dog Stand Queue'
q2.metadata = {'quality': NumberGenerator(UNIFORM, a=1, b=3),
               'cost': NumberGenerator(UNIFORM, a=1, b=3)
               }
#q2.logs = True

pr3 = ActorProbe(q2)
pr3.name = 'Hot Dog Stand Queue Probe'
q2.actorprobe = pr3

pr4 = ActorProbe(dl2)
pr4.name = 'Hot Dog Stand Delay Probe'
dl2.actorprobe = pr4


# Restaurant
dl3 = Delay(d1, DELAY_RATE_ABLE.next, None, 5)
dl3.name = 'Wait Restaurant'
#dl3.logs = True

q3 = Queue([dl3])
q3.name = 'Restaurant Queue'
q3.metadata = {'quality': NumberGenerator(UNIFORM, a=7, b=10),
               'cost': NumberGenerator(UNIFORM, a=8, b=11)
               }
#q3.logs = True

pr5 = ActorProbe(q3)
pr5.name = 'Queue Probe'
q3.actorprobe = pr5

pr6 = ActorProbe(dl3)
pr6.name = 'Delay Probe'
dl3.actorprobe = pr6

def randomchoice(l):
    s = NumberGenerator(UNIFORM, a=0, b=len(l)).next()
    return l[int(s)]

top = {'a':0,
       'b':0,
       'c':0,
       'd':0,
       'e':0,
       'f':0,
       'g':0,
       'h':0,
       'i':0
       }

def AgentOnEnter(actor, self):
    global s1, d1, q1, q2, q3, top
    if (actor == s1):
        #Decide which food court to go to
        a1 = self.attributes['fastfoodscore']
        a2 = self.attributes['hotdogscore']
        a3 = self.attributes['restaurantscore']

        if (a1 > a2 and a1 > a3):
            top['a'] += 1
            nex = q1
        elif (a2 > a1 and a2 > a3):
            top['b'] += 1
            nex = q2
        elif (a3 > a1 and a3 > a2):
            top['c'] += 1
            nex = q3
        elif (a1 == a2):
            top['d'] += 1
            if (a3 == a1):
                nex = randomchoice((q1, q2, q3))
            else:
                nex = randomchoice((q1, q2))
        elif (a1 == a3):
            top['e'] += 1
            nex = randomchoice((q1, q3))
        elif (a2 == a3):
            top['f'] += 1
            nex = randomchoice((q2, q3))
        self.attributes['entertime'] = self.simulation.tick
        self.attributes['lastentered'] = nex
        self.leaveActor(s1)
        self.enterActor(nex)
        if (nex == q1):
            top['g'] += 1
        elif (nex == q2):
            top['h'] += 1
        elif (nex == q3):
            top['i'] += 1
            
    elif (actor == d1):
        le = self.attributes['lastentered']
        t = self.simulation.tick - self.attributes['entertime']
        q = le.metadata['quality'].next()
        c = le.metadata['cost'].next()
        scr = 0
        if (t > self.attributes['timethereshold']):
            scr -= 1
        if (q < self.attributes['qualitythereshold']):
            scr -= 1
        if (c > self.attributes['costthereshold']):
            scr -= 1
            
        if (le == q1):
            self.attributes['fastfoodscore'] += scr
        elif (le == q2):
            self.attributes['hotdogscore'] += scr
        elif (le == q3):
            self.attributes['restaurantscore'] += scr
        mn = max(self.attributes['fastfoodscore'], self.attributes['hotdogscore'], self.attributes['restaurantscore'])
        self.attributes['fastfoodscore'] -= mn
        self.attributes['hotdogscore'] -= mn
        self.attributes['restaurantscore'] -= mn

def AgentOnLeave(actor, self):
    pass

def AgentOnStart():
    
    return {'fastfoodscore':0,
            'restaurantscore':0,
            'hotdogscore':0,
            'entertime':0,
            'lastentered': None,
            'timethereshold': NumberGenerator(UNIFORM, a=1, b=9).next(),
            'qualitythereshold': NumberGenerator(UNIFORM, a=1, b=10).next(),
            'costthereshold': NumberGenerator(TRIANGULAR, low=1, high=10, mid=2).next()
            }

g1 = AutomaticGenerator(s1, Agent, {'onenter': AgentOnEnter, 'onleave': AgentOnEnter, 'start': AgentOnStart}, INTERVAL_RATE.next, 800)
#g1.logs = True

sim = Simulation()
sim.maxtick = 100000
#sim.logs = True

sim.addactor(d1)

sim.addactor(s1)

sim.addactor(q1)
sim.addactor(dl1)

sim.addactor(q2)
sim.addactor(dl2)

sim.addactor(q3)
sim.addactor(dl3)

sim.addactor(g1)

sim.addprobe(pr1)
sim.addprobe(pr2)
sim.addprobe(pr3)
sim.addprobe(pr4)
sim.addprobe(pr5)
sim.addprobe(pr6)

sim.start()

#drawProbs(pr1.calculatestatistics()[1], sim.tick, 'queue')
#drawProbs(pr2.calculatestatistics()[1], sim.tick, 'delay')

#print("Queue Utilization:", pr1.calculatestatistics()[0])
#print("Delay Utilization:", pr2.calculatestatistics()[0])

print('Fastfood:' + str(len(pr1.enters)))
print('Hotdog:' + str(len(pr3.enters)))
print('Restaurant:' + str(len(pr5.enters)))

