import enum
import turtle

class CA2DDisplay:
    def __init__(self, colors=None, name=None):
        self.colors = colors or {}
        self.name = name
        self.initTurtle()

    def initTurtle(self):
        self.t = turtle.Turtle()
        turtle.delay(0)
        self.t.speed(0)
        self.t.hideturtle()
        self.t.pu()

    def draw(self, map):
        self.t.clear()
        wstep = 400 / len(map[0])
        hstep = 600 / len(map)
        size = min(wstep, hstep)
        self.t.pensize(300 / size)
        for i in range(len(map)):
            for j in range(len(map[i])):
                self.t.pencolor(self.colors.get(map[i][j], 'black'))
                self.t.goto(i * hstep - 300, j * wstep - 200)
                self.t.dot()


def drawLeaveEnter(list, title):
    number = 600
    if len(list) > number:
        tempList = []
        step = int(len(list) / number)
        for i in range(1, number):
            tmp = list[(i - 1) * step : i * step]
            tempList.append(sum(tmp) / len(tmp))

        list = tempList

    length = 400 / len(list)
    maximum = 600 / max(list)

    t = turtle.Turtle()
    turtle.delay(0)
    t.speed(0)
    t.hideturtle()
    t.pensize(4)
    t.pu()
    t.goto(-300, -200)
    t.pd()
    t.fd(600)
    t.pu()
    t.goto(-300, -200)
    t.pd()
    t.goto(-300, +200)
    t.pu()
    t.pensize(2)
    t.pencolor('black')
    t.goto(-280, +195)
    t.write("%s: [%d:%d]" % (title, len(list), max(list)), align='left', font=('Times New Roman', 16))
    t.goto(-300, -200)
    t.pencolor('red')
    t.pd()

    num = 0
    for i in list:
        t.goto(i * maximum - 300, num * length - 200)
        num += 1
        t.goto(i * maximum - 300, num * length - 200)

        # t.write(str((i, [i])), align='left', font=('Times New Roman', 10))

    turtle.done()

def drawProbs(list, lastTick, title):
    my = 0
    for i in list:
        if i[-1] > my:
            my = i[-1]

    if my == 0:
        print("empty probe")
        return

    number = 3 * 600
    if len(list) > number:
        tempList = []
        step = int(len(list) / number)
        for i in range(1, number):
            tmpLst = list[(i - 1) * step : i * step]
            elem = [0, 0]
            for i in tmpLst:
                elem[0] += i[0]
                if elem[1] < i[1]:
                    elem[1] = i[1]

                if my < i[1]:
                    my = i[1]

            elem[0] /= len(tmpLst) * step * 3
            tempList.append(elem)
        lastTick = number
        list = tempList


    length = 400 / my
    maximum = 600 / lastTick

    t = turtle.Turtle()
    turtle.delay(0)
    t.speed(0)
    t.hideturtle()
    t.pensize(4)
    t.pu()
    t.goto(-300, -200)
    t.pd()
    t.fd(600)
    t.pu()
    t.goto(-300, -200)
    t.pd()
    t.goto(-300, +200)
    t.pu()
    t.pensize(2)
    t.pencolor('black')
    t.goto(-280, +195)
    t.write("%s: [%d:%d]" % (title, my, lastTick), align='left', font=('Times New Roman', 16))
    t.goto(-300, -200)
    t.pencolor('red')
    t.pd()
    
    for i in list:
        t.goto(i[0] * maximum - 300, i[1] * length - 200)
        # t.write(str((i, [i])), align='left', font=('Times New Roman', 10))

    turtle.done()

class elementType(enum.Enum):
    entity = 1
    process = 2
    delay = 3
    resource = 4
    queue = 5


class baseEntity:
    name = ''
    type = ''

class entity(baseEntity):
    lastDelayTick = 0


class Statistic:
    lastTick = 0
    obj = {}
    lastUniqueId = 0

    def __init__(self):
        pass

    def registerEntity(self, enType=None, enName=''):
        if enType:
            self.lastUniqueId += 1
            self.obj[self.lastUniqueId] = {
                'name': enName,
                'type': enType
            }

            if enType == elementType.entity:
                self.obj[self.lastUniqueId]['lastDelayTick'] = 0
                self.obj[self.lastUniqueId]['delay'] = []
                self.obj[self.lastUniqueId]['createTime'] = 0
                self.obj[self.lastUniqueId]['disposeTime'] = 0

            elif enType == elementType.process:
                self.obj[self.lastUniqueId]['lastDelayTick'] = 0
                self.obj[self.lastUniqueId]['delay'] = []

            elif enType == elementType.delay:
                self.obj[self.lastUniqueId]['lastDelayTick'] = 0

            elif enType == elementType.resource:
                self.obj[self.lastUniqueId]['queue'] = []
                self.obj[self.lastUniqueId]['queueTick'] = []
                self.obj[self.lastUniqueId]['serviceLength'] = []

            elif enType == elementType.queue:
                self.obj[self.lastUniqueId]['len'] = []
                self.obj[self.lastUniqueId]['lenTick'] = []


            return self.lastUniqueId

        return None

    def signal(self, enId=None, **kwargv):
        pass


    def end(self):
        pass

if __name__ == "__main__":
    entity = {
        'Able': [],
        'Baker': [],
    }
    queue = []
    totalQueue = 0
    delayQueue = []
    inQueue = [(0 ,0)] # (tick, len)

    startTick = 0
    endTick = 0

    for line in open('logs.txt'):
        line = line.split(':')
        if line[0] in entity:
            line[1] = line[1].split()
            if 'Delays' in line[1][0]:
                entity[line[0]].append(float(line[1][4]))

        elif line[0] == 'Queue':
            line[1] = line[1].split()
            if line[1][0] == 'Enqueued':
                queue.append(float(line[-1]))
                inQueue.append((float(line[-1]), inQueue[-1][1] + 1))

            elif line[1][0] == 'Dequeued':
                lastDelay = float(line[-1]) - queue[0]
                if lastDelay == 0:
                    inQueue.pop()

                else:
                    inQueue.append((float(line[-1]), inQueue[-1][1] - 1))

                totalQueue += lastDelay
                delayQueue.append(lastDelay)
                del queue[0]

        elif line[0] == 'Simulation started':
            startTick = float(line[-1])

        elif line[0] == 'Simulation finished':
            endTick = float(line[-1])

    print('Simulation Time: ' + str(endTick - startTick))
    print('Total Queue Time: ' + str(totalQueue))

    delayQueue = sorted(delayQueue)

    s = 0
    step = 10
    index = 0
    tmp = 0
    queueTimeList = []
    while index < len(delayQueue):
        if s <= delayQueue[index] <= (s + step):
            tmp += 1

        else:
            print("N.O. of Delay in [%d, %d): %d" % (s, s + step, tmp))
            s += step
            queueTimeList.append(tmp)
            tmp = 0

        index += 1

    for i in entity:
        print('Utilization for ' + i + ": " + str(sum(entity[i])/(endTick - startTick)) + " : " + str(len(entity[i])))

    t = turtle.Turtle()
    turtle.delay(0)
    t.speed(0)
    t.hideturtle()
    t.pensize(4)
    t.pu()
    t.goto(-300, -200)
    t.pd()
    t.fd(600)
    t.pu()
    t.goto(-300, -200)
    t.pd()
    t.goto(-300, +200)
    t.pu()
    t.pensize(2)
    t.pencolor('red')
    t.goto(-280, +180)
    t.write("Queue Delay", align='left', font=('Times New Roman', 16))
    t.goto(-300, -200)
    t.pd()

    length = 400 / max(queueTimeList)
    maximum = 600 / len(queueTimeList)

    for i in range(len(queueTimeList)):
        t.goto(i * maximum - 280, queueTimeList[i] * length - 200)
        t.write(str((i, queueTimeList[i])), align='left', font=('Times New Roman', 10))


    t.pu()
    t.pensize(2)
    t.pencolor('blue')
    t.goto(-280, +150)
    t.write("Queue Length", align='left', font=('Times New Roman', 16))
    t.goto(-300, -200)
    t.pd()


    mx = 0
    for i in inQueue:
        if i[-1] > mx:
            mx = i[-1]

    length = 400 / mx
    maximum = 600 / inQueue[-1][0]

    for i in inQueue:
        t.goto(i[0] * maximum - 280, i[1] * length - 200)

    turtle.done()
