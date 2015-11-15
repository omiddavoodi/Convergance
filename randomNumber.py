import random

RANDOM = 1
UNIFORM = 2
TRIANGULAR = 3
BETA = 4
EXP = 5
GAMMA = 6
GAUSS = 7
LOGNORM = 8
NORMAL = 9
VONMISES = 10
PARETO = 11
WEIBULL = 12
RANDINT = 13

gens = {
    RANDOM: {
        'name': 'random',
        'args': None
    },
    UNIFORM: {
        'name': 'uniform',
        'args': { 
            'a': 0, 
            'b': 1
        }
    },
    TRIANGULAR: {
        'name': 'triangular',
        'args': { 
            'low': 0.0,
            'high': 1.0,
            'mode': None
        }
    },
    BETA: {
        'name': 'betavariate',
        'args': { 
            'alpha': 0.1,
            'beta': 0.1
        }
    },
    EXP: {
        'name': 'expovariate',
        'args': { 
            'lambd': 1
        }
    },
    GAMMA: {
        'name': 'gammavariate',
        'args': { 
            'alpha': 0.1,
            'beta': 0.1
        }
    },
    GAUSS: {
        'name': 'gauss',
        'args': { 
            'mu': 0,
            'sigma': 0
        }
    },
    LOGNORM: {
        'name': 'lognormvariate',
        'args': { 
            'mu': 0,
            'sigma': 0
        }
    },
    NORMAL: {
        'name': 'normalvariate',
        'args': { 
            'mu': 0,
            'sigma': 0
        }
    },
    VONMISES: {
        'name': 'vonmisesvariate',
        'args': { 
            'mu': 0,
            'kappa': 0
        }
    },
    PARETO: {
        'name': 'paretovariate',
        'args': { 
            'alpha': 0
        }
    },
    WEIBULL: {
        'name': 'weibullvariate',
        'args': { 
            'alpha': 0.1,
            'beta': 0.1
        }
    },
    RANDINT: {
        'name': 'randint',
        'args': {
            'a': 0,
            'b': 2
        }
    }
}

class NumberGenerator():
    __rn = None
    __arg = None

    def __init__(self, type=RANDOM, **kwargv):      
        self.__rn = getattr(random, gens[type]['name'])
        self.__arg = {}
        if gens[type]['args']:
            for key, value in gens[type]['args'].items():
                self.__arg[key] = kwargv.get(key, value)


    def next(self, *args):
        return self.__rn(**self.__arg)


if __name__ == "__main__":
    a = NumberGenerator()
    print(a.next())

    a = NumberGenerator(TRIANGULAR, low=2, mode=3, high=90)
    print(a.next())

    a = NumberGenerator(NORMAL, mu=0.4, sigma=3)
    print(a.next())

    a = NumberGenerator(RANDINT, a=0, b=3)
    print(a.next())

