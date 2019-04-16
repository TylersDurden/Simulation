from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import utility
import model
import time


class Particle:
    color = ''
    x = 0
    y = 0
    steps = []
    repels = []
    attracts = []

    def __init__(self, label, position):
        self.color = label
        self.x = position[0]
        self.y = position[1]

    def set_position(self, newpos, repel, attract):
        self.x = newpos[0]
        self.y = newpos[1]

    def apply_rule(self, rules):
        for rule in rules:
            if self.color in rule.split(' '):
                if self.color == rule.split(' ')[0] and rule.split(' ')[1]=='repels':
                    self.repels.append(rule.split(' ')[2])
                if self.color == rule.split(' ')[2] and rule.split(' ')[1]=='repels':
                    self.repels.append(rule.split(' ')[0])
                if self.color == rule.split(' ')[0] and rule.split(' ')[1]=='attracts':
                    self.attracts.append(rule.split(' '[2]))
                if self.color == rule.split(' ')[2] and rule.split(' ')[1]=='attracts':
                    self.repels.append(rule.split(' ')[0])


class Engine:
    config = {}
    timescale = 0
    n_particles = 0
    width = 0
    height = 0
    state = [[]]
    verbose = False

    nred = 0
    ngreen = 0
    nblue = 0
    ncyan = 0
    nmagenta = 0
    nyellow = 0
    nwhite = 0
    nblack = 0

    particle_count = {'r':nred,
                      'g':ngreen,
                      'b':nblue,
                      'c':ngreen,
                      'm':nmagenta,
                      'y':nyellow,
                      'k':nblack,
                      'w':nwhite}

    color_handles = {'r': '\033[31mRed\033[0m',
                     'g': '\033[32mGreen\033[0m',
                     'b': '\033[34mBlue\033[0m',
                     'c': '\033[36mCyan\033[0m',
                     'm': '\033[35mMagenta\033[0m',
                     'y': '\033[33mYellow\033[0m',
                     'k': '\033[2mBlack\033[0m',
                     'w': '\033[1mWhite\033[0m'}
    repel_strength = 0
    attract_strength = 0

    def __init__(self, configuration):
        self.config = configuration
        cloud = self.initialize()
        self.run(cloud)

    def initialize(self):
        RULES = []
        self.width = self.config['width']
        self.height = self.config['height']
        self.timescale = self.config['timescale']
        self.state = np.zeros((self.width, self.height, 3))
        particle_types = self.config['particle_counts']
        if 'verbose' in self.config.keys():
            self.verbose = self.config['verbose']
        if 'rules' in self.config.keys():
            ptypes = self.config['rules'].keys()
            for color in ptypes:
                for rule in self.config['rules'][color].keys():
                    try:
                        print color + ' ' + rule + ' ' + self.config['rules'][color][rule].pop()
                        RULES.append(color + ' ' + rule + ' ' + self.config['rules'][color][rule].pop())
                    except IndexError:
                        pass
            if 'attract_strength' in self.config.keys():
                print "* Simulation Strength of Attraction is " + str(self.config['attract_strength'])
                self.attract_strength = self.config['attract_strength']
            if 'repel_strength' in self.config.keys():
                print "* Simulation Strength of Repellant Force is " + str(self.config['repel_strength'])
                self.repel_strength = self.config['repel_strength']
        return self.add_particles(particle_types, RULES)

    def add_particles(self, particle_types, rules):
        cloud = {}
        rgb = model.Spectra()
        rgb.initialize()
        ii = 0
        for color in particle_types.keys():
            try:
                self.particle_count[color] = particle_types[color]
                # POPULATE self.state
                for pid in range(self.particle_count[color]):
                    pt = utility.spawn_random_point(self.state)
                    particle = Particle(color, pt)
                    particle.apply_rule(rules)
                    particle.steps, unused = utility.spawn_random_walk(pt, self.timescale)
                    cloud[ii] = particle
                    self.state[pt[0], pt[1], :] = rgb.color_handles[color]
                    ii += 1
                if self.verbose:
                    print "Added " + str(particle_types[color]) + ' \033[1m' + self.color_handles[color] + \
                          ' Particles to Simulation with ' + str(self.timescale) + ' Steps\033[0m'
            except KeyError:
                continue

        return cloud

    def run(self, cloud):
        f = plt.figure()
        film = []
        rgb = model.Spectra()
        rgb.initialize()
        world = self.state
        for step in range(self.timescale):
            for particle in cloud.values():
                try:
                    move = particle.steps[step]
                    world[particle.x, particle.y, :] = 0
                    particle.set_position(move, self.repel_strength, self.attract_strength)
                    world[particle.x, particle.y, :] = rgb.color_handles[particle.color]
                except IndexError:
                    continue
            film.append([plt.imshow(world)])
            # TODO:
            # Apply Collisions
            # Apply Attraction repulsion rules

        a = animation.ArtistAnimation(f, film, interval=50, blit=True, repeat=900)
        plt.show()


def main():
    particles = {'r': 150, 'b': 150}
    test_config = {'width': 150,
                   'height': 150,
                   'timescale': 250,
                   'particle_counts': particles,
                   'rules': {'r': {'repels': ['r'], 'attracts': ['b']},
                             'b': {'repels': ['b'], 'attracts': ['r']}},
                   'repel_strength': 5,
                   'attract_strength': 5,
                   'verbose': True}
    simulation = Engine(test_config)


if __name__ == '__main__':
    main()
