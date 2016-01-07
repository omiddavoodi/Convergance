import os, copy, time, random

DELAY = 0.2

class CA:
    def __init__(self, name='CA - 2D', rows=10, columns=10, defaultState=0, log=False, init=None):
        self.nextGeneration = None
        self.states = {}
        self.name = name
        self.defaultState = defaultState
        self.log = log

        if init is None:
            self.rows = rows
            self.columns = columns
            self.map = [[self.defaultState for j in range(columns)] for i in range(rows)]

        else:
            self.map = init
            self.rows = len(init)
            self.columns = len(init[0])

    def setColor(self, dic):
        self.states = dic

    def setNextGeneration(self, NGFunction=None):
        self.nextGeneration = NGFunction

    def getMap(self):
        return self.map

    def checkForExtend(self):
        for i in range(self.rows):
            if self.map[i][0] != self.defaultState:
                if self.log:
                    print('extending columns for: (%d, 0)' % i)

                self.columns += 1
                for j in range(self.rows):
                    self.map[j].insert(0, self.defaultState)

                break

        for i in range(self.rows):
            if self.map[i][-1] != self.defaultState:
                if self.log:
                    print('extending columns for: (%d, -1)' % i)

                self.columns += 1
                for j in range(self.rows):
                    self.map[j].append(self.defaultState)

                break

        for i in range(self.columns):
            if self.map[0][i] != self.defaultState:
                if self.log:
                    print('extending rows for: (0, %d)' % i)

                self.rows += 1
                self.map.insert(0, [self.defaultState for j in range(self.columns)])
                break

        for i in range(self.columns):
            if self.map[-1][i] != self.defaultState:
                if self.log:
                    print('extending rows for: (-1, %d)' % i)

                self.rows += 1
                self.map.append([self.defaultState for j in range(self.columns)])
                break 

    def tick(self):
        if self.nextGeneration is None:
            return 0

        self.checkForExtend()

        temp = copy.deepcopy(self.map)
        
        for i in range(self.rows):
            for j in range(self.columns):
                temp[i][j] = self.nextGeneration(i, j, self.map)

        self.map = copy.deepcopy(temp)
        
        return 1

    def draw(self):
        # uses self.tick and self.states
        for i in self.map:
            print(''.join([self.states.get(j) for j in i]))
        
    def runInConsole(self):
        os.system('cls')
        self.draw()
        while True:
            time.sleep(DELAY)
            os.system('cls')
            self.tick()
            self.draw()


def conway(i, j, map):
    selfState = map[i][j]
    live = 0
    for pos in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        try:
            if map[i + pos[0]][j + pos[1]] == 1:
                live += 1
        except:
            pass

    if selfState == 0:
        if live == 3: # reproduction
            # print('reproduction')
            return 1

    else:
        if live < 2: # under-population
            # print('under-population')
            return 0

        if live == 2 or live == 3: # lives on to the next generation
            # print('lives')
            return 1

        if live > 3: # over-population
            # print('over-population')
            return 0

    return selfState

block = [[1, 1], [1, 1]]
blink = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
Pentadecathlon = [
                    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                    [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
                    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                ]

Beacon = [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
        ]

kOmidTest = random.randrange(15,30)
OmidsTest = [[random.randrange(0,2) for j in range(kOmidTest)] for i in range(random.randrange(15,30))]

myCa = CA('conway game of lime', init=OmidsTest, log=False)
myCa.setColor({0: '-', 1: 'X'})
myCa.setNextGeneration(conway)
myCa.runInConsole()
