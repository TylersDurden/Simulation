from itertools import combinations
import numpy as np
import simengine
import utility


class StandardModel:
    Red = [1, 0, 0]
    Green = [0, 1, 0]
    Blue = [0, 0, 1]
    Purp = [1, 0, 1]
    Yell = [0, 1, 1]
    Teal = [1, 1, 0]
    Black = [0, 0, 0]
    White = [1, 1, 1]

    elementary = ['R', 'G', 'B', 'Y', 'P', 'T']
    operations = ['-', '+']
    events = {}
    rules = {}

    def __init__(self):
        self.events,self.rules = self.initialize()

    def initialize(self):
        event_vectors = {0: ['R', 'G', '+'],    # Red + Green
                         1: ['G', 'B', '+'],    # Green + Blue
                         2: ['P', 'G', '+'],    # Purple + Green
                         3: ['Y', 'R', '+'],    # Yellow + Red
                         4: ['Y', 'G', '+'],    # Yellow + Green
                         5: ['Y', 'P', '+'],    # Yellow + Purple (Green)
                         6: ['Y', 'P', '-'],    # Yellow - Purple (Blue)
                         7: ['T', 'G', '-'],    # Teal - Green (Blue)
                         8: ['T', 'P', '-'],    # Teal - Purple (Green)
                         9: ['Y', 'R', '-'],    # Yellow - Red (Green)
                         10:['Y', 'G', '-']     # Yellow - Green (Red)
                         }

        rules = {0: self.Blue,
                 1: self.Yell,
                 2: self.White,
                 3: self.White,
                 4: self.White,
                 5: self.Green,
                 6: self.Blue,
                 7: self.Blue,
                 8: self.Green,
                 9: self.Green,
                 10: self.Red}
        return event_vectors, rules

    def two_particle_collision(self, collision):
        if len(collision) > 2:
            print "More than two particles in collision"
            return ''
        a = str(collision[0]).upper()
        b = str(collision[1]).upper()
        event = [a, b, '+']
        # Isolate all additive events (collisions)
        combos = []
        [combos.append(list(combo)) for combo in combinations(self.elementary, 2)]
        events = {}
        ii = 0
        for pair in combos:
            events[ii] = pair.append('+')
            ii += 1


class RGB:
    R = [[]]
    G = [[]]
    B = [[]]
    Y = [[]]
    M = [[]]
    C = [[]]
    handles = {}

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.R = np.zeros((1,1,3))
        self.G = np.zeros((1,1,3))
        self.B = np.zeros((1,1,3))
        self.R[:,:,0] = 1
        self.G[:,:,1] = 1
        self.B[:,:,2] = 1
        self.Y = self.R + self.G
        self.M = self.R + self.B
        self.C = self.B + self.G
        self.handles['r'] = self.R
        self.handles['g'] = self.G
        self.handles['b'] = self.B
        self.handles['c'] = self.C
        self.handles['m'] = self.M
        self.handles['y'] = self.Y


class Particle:
    color = ''
    x = 0
    y = 0
    internal_state = 0
    steps = []

    def __init__(self, color_name, position):
        self.color = color_name
        self.x = position[0]
        self.y = position[1]

    def generate_random_steps(self, nsteps):
        self.steps, unused = utility.spawn_random_walk([self.x, self.y], nsteps)

    def set_position(self, location):
        self.x = location[0]
        self.y = location[1]


def main():
    initial_config = {'width': 150,
                      'height': 150,
                      'n_particles': 300,
                      'timescale': 100,
                      'nRed': 250,
                      'nGreen': 120,
                      'nBlue': 100,
                      'nYellow': 120,
                      'nMagenta': 50,
                      'nCyan': 0,
                      'verbose': True}

    rgb = RGB()
    sim = simengine.Engine(initial_config, rgb)
    collisions = sim.run(rgb, False, save=False)
    casm = StandardModel()
    casm.two_particle_collision(collisions.pop(np.random.randint(0,len(collisions)-1,1)[0]))


if __name__ == '__main__':
    main()
