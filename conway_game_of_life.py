from convergance_statistic import CA2DDisplay
from convergance_cellular_automata import CA2D
import random


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
            return 1

    else:
        if live < 2: # under-population
            return 0

        if live == 2 or live == 3: # lives on to the next generation
            return 1

        if live > 3: # over-population
            return 0

    return selfState


block = [[1, 1], [1, 1]]
blink = [
            [1, 1, 1],
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

kOmidTest = random.randrange(15, 30)
OmidsTest = [[random.randrange(0,2) for j in range(kOmidTest)] for i in range(random.randrange(15,30))]

colors = {0: 'black', 1: 'red'}
myCa = CA2D('conway game of life', init=Pentadecathlon, log=False, delay=1)
myCa.setColor(colors)
myCa.setNextGeneration(conway)

myCaDisplay = CA2DDisplay(name=myCa.name, colors=colors)
myCa.setDisplay(myCaDisplay.draw)
myCa.run(500)
