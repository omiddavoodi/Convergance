
class Statistic:
    lastTick = 0
    Entity = {}

    def __init__(self):
        pass

    def registerEntity(self):
        pass

    def signalEntity(self):
        pass


if __name__ == "__main__":
    entity = {
        'Able': [],
        'Baker': [],
    }
    queue = []
    totalQueue = 0
    delayQueue = []

    startTick = 0
    endTick = 0

    f = open('logs.txt')
    for line in f:
        line = line.split(':')
        if line[0] in entity:
            line[1] = line[1].split()
            if 'Delays' in line[1][0]:
                entity[line[0]].append(float(line[1][4]))

        elif line[0] == 'Queue':
            line[1] = line[1].split()
            if line[1][0] == 'Enqueued':
                queue.append(float(line[-1]))

            elif line[1][0] == 'Dequeued':
                totalQueue += float(line[-1]) - queue[0]
                delayQueue.append(float(line[-1]) - queue[0])
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
    while index < len(delayQueue):
        if s <= delayQueue[index] <= (s + step):
            tmp += 1

        else:
            print("N.O. of Delay in [%d, %d): %d" % (s, s + step, tmp))
            s += step
            tmp = 0

        index += 1

    for i in entity:
        print('Utilization for ' + i + ": " + str(sum(entity[i])/(endTick - startTick)) + " : " + str(len(entity[i])))
