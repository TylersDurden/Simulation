import matplotlib.pyplot as plt
import numpy as np
import simengine
import utility
import time
import sys


class StandardModel:
    Red = [1, 0, 0]
    Green = [0, 1, 0]
    Blue = [0, 0, 1]
    Purp = [1, 0, 1]
    Yell = [0, 1, 1]
    Teal = [1, 1, 0]
    Black = [0, 0, 0]
    White = [1, 1, 1]

    elementary = ['R', 'G', 'B', 'Y', 'M', 'C']
    operations = ['-', '+']
    events = {}
    rules = {}

    def __init__(self):
        self.events,self.rules = self.initialize()

    def initialize(self):
        event_vectors = {0: ['R', 'G', '+'],    # Red + Green
                         1: ['G', 'B', '+'],    # Green + Blue
                         2: ['M', 'G', '+'],    # Purple + Green
                         3: ['Y', 'R', '+'],    # Yellow + Red
                         4: ['Y', 'G', '+'],    # Yellow + Green
                         5: ['Y', 'M', '+'],    # Yellow + Purple (Green)
                         6: ['R', 'B', '+'],
                         7: ['M', 'G', '+'],
                         8: ['M', 'R', '+'],
                         9: ['W', 'R', '+'],
                         10: ['W', 'G', '+'],
                         11: ['W', 'B', '+'],
                         12: ['W', 'M', '+'],
                         13: ['W', 'Y', '+'],
                         14: ['W', 'C', '+'],
                         15: ['C', 'M', '+'],
                         16: ['C', 'Y', '+']}

        rules = {0: 'y',
                 1: 'c',
                 2: 'w',
                 3: 'r',
                 4: 'y',
                 5: 'w',
                 6: 'm',
                 7: 'w',
                 8: 'y',
                 9: 'r',
                 10: 'g',
                 11: 'b',
                 12: 'm',
                 13: 'y',
                 14: 'c',
                 15: 'w',
                 16: 'w'}
        return event_vectors, rules


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
        self.handles['w'] = np.ones((1,1,3))


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
    if 'demo' in sys.argv:
        initial_config = {'width': 250,
                          'height': 250,
                          'n_particles': 10,
                          'timescale': 250,
                          'nRed': 300,
                          'nGreen': 300,
                          'nBlue': 400,
                          'nYellow': 0,
                          'nMagenta': 0,
                          'nCyan': 0,
                          'verbose': True}

        rgb = RGB()
        sim = simengine.Engine(initial_config, rgb)
        collisions = sim.run(RGB=rgb, animate=True, save=True)
        casm = StandardModel()
        exit(0)
    elif 'npVsz' in sys.argv:
        rgb = RGB
        const_time = 100
        dims = [50,100,150,250,350,450,550]
        np =   [10,20,30,40,50,100,500]
        ncs = [['nRed','nBlue'],['nRed','nGreen'],
               ['nRed','nBlue','nGreen'],['nCyan','nMagenta','nYellow'],
               ['nRed','nBlue','nGreen','nCyan'],['nRed','nBlue','nGreen','nCyan','nMagenta'],
               ['nRed','nBlue','nGreen','nCyan','nMagenta','nYellow']]
        opts = ['nRed','nBlue','nGreen','nCyan','nMagenta','nYellow']
        collision_data = []
        runtime_data = []
        for shape in dims:
            width = shape
            height = shape
            for n_particles in np:
                for particle_combos in ncs:
                    config = {'width':width,
                              'height':height,
                              'n_particles':n_particles,
                              'timescale':const_time}
                    # TODO: Automate nColor selections
                    config['verbose'] = False
                    tic = time.time()
                    collisions = simengine.Engine(config, rgb).run(RGB=rgb,animate=False,save=False)
                    toc = time.time()
                    runtime_data.append(float(toc-tic))
                    collision_data.append(float(collisions))
        plt.plot(np.array(collision_data))
        plt.plot(np.array(runtime_data))
        plt.show()


if __name__ == '__main__':
    main()
