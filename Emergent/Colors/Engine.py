import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndi
import imutil
import Engine
import Logic
import colors


class Particle:
    color = ''
    x = 0
    y = 0
    loc = []

    def __init__(self, label, position):
        if len(position) == 2:
            self.color = label
            self.x = position[0]
            self.y = position[1]
            self.loc = position
        else:
            print "Illegal Construction!"
            exit(0)


class Engine:
    config = {}
    width = 0
    height = 0
    n_particles = 0
    timescale = 0
    particle_counts = {'r': 0, 'g': 0, 'b': 0,
                       'c': 0, 'm': 0, 'y': 0}
    verbose = False

    def __init__(self, config):
        self.initialize(config)

    def initialize(self, config):
        self.width = config['width']
        self.height = config['height']
        self.n_particles = config['n_particles']
        self.add_particles(config)

    def add_particles(self, config):
        if 'verbose' in config.keys():
            self.verbose = config['verbose']
        if 'nRed' in config.keys():
            self.particle_counts['r'] = config['nRed']
            if self.verbose:
                print "\033[1m* \033[31m" + str(config['nRed']) + ' Red Particles added\033[0m'
        if 'nGreen' in config.keys():
            self.particle_counts['g'] = config['nGreen']
            if self.verbose:
                print "\033[1m* \033[32m" + str(config['nGreen']) + ' Green Particles added\033[0m'
        if 'nBlue' in config.keys():
            self.particle_counts['b'] = config['nBlue']
            if self.verbose:
                print "\033[1m* \033[34m" + str(config['nBlue']) + ' Blue Particles added\033[0m'
        if 'nCyan' in config.keys():
            self.particle_counts['c'] = config['nCyan']
            if self.verbose:
                print "\033[1m* \033[36m" + str(config['nCyan']) + ' Cyan Particles added\033[0m'
        if 'nMagenta' in config.keys():
            self.particle_counts['m'] = config['nMagenta']
            if self.verbose:
                print "\033[1m* \033[35m" + str(config['nMagenta']) + ' Magenta Particles added\033[0m'

    def construct_cloud(self):
        has_time = False
        try:
            self.timescale = self.config['timescale']
            if self.verbose:
                print '* Constructing Simulation with ' + str(self.timescale) + " time steps "
            has_time = True
        except KeyError:
            pass

        world = np.zeros((self.width, self.height, 3))
        cloud = {}
        rgb = colors.RGB()
        rgb.initialize()
        ii = 0
        for ptype in self.particle_counts.keys():
            color = rgb.handles[ptype]
            for particle in range(self.particle_counts[ptype]):
                pt = imutil.spawn_random_point(world)
                obj = Particle(ptype, pt)
                if has_time:
                    obj.generate_random_steps(self.timescale)
                world[pt[0], pt[1], :] = color[:, :, :]
                cloud[ii] = obj
                ii += 1
        return world, cloud


size = 250
n_particles = 1000
test_config = {'width': size,
                'height': size,
                'n_particles': 100,
                'timescale': 100,
                'nRed': n_particles / 3,
                'nGreen': n_particles / 3,
                'nBlue': n_particles / 3,
                'nYellow': 0,
                'nCyan': 0,
                'nMagenta': 0,
                'verbose': True}

sim = Engine(test_config)
state, cloud = sim.construct_cloud()