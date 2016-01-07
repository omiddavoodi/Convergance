import os, copy, time

class CA2D:
    def __init__(self, name='CA - 2D', rows=10, columns=10, defaultState=0, log=False, init=None, delay=0.2):
        self.nextGeneration = None
        self.states = {}
        self.name = name
        self.defaultState = defaultState
        self.log = log
        self.delay = delay
        if init is None:
            self.rows = rows
            self.columns = columns
            self.map = [[self.defaultState for j in range(columns)] for i in range(rows)]

        else:
            self.map = init
            self.rows = len(init)
            self.columns = len(init[0])

    def setColor(self, dic):
        self.states = copy.deepcopy(dic)

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

        del self.map
        self.map = copy.deepcopy(temp)
        del temp
        
        return 1

    def draw(self):
        for i in self.map:
            print(''.join([self.states.get(j) for j in i]))
        
    def runInConsole(self):
        os.system('cls')
        self.draw()
        while True:
            time.sleep(self.delay)
            os.system('cls')
            self.tick()
            self.draw()


class CA1D:
	pass
