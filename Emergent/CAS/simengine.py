from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import ColorAutomataSimulations
import numpy as np
import utility
import time


class Engine:
    state = [[]]
    width = 0
    height = 0
    n_particles = 0
    timescale = 0
    particle_counts = {'r': 0, 'g': 0, 'b': 0,
                       'c': 0, 'y': 0, 'm': 0,
                       'w':0}
    particle_data = {}
    verbose = False

    def __init__(self, config, RGBobj):
        self.width = config['width']
        self.height = config['height']
        self.n_particles = config['n_particles']
        self.add_particles(config)
        self.state, self.particle_data = self.construct_cloud(config,RGBobj)

    def add_particles(self, config):
        if 'verbose' in config.keys():
            self.verbose = config['verbose']
        if 'nRed' in config.keys():
            self.particle_counts['r'] = config['nRed']
            if self.verbose:
                print "\033[1m* \033[31m"+str(config['nRed'])+' Red Particles added\033[0m'
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
        if 'nYellow' in config.keys():
            self.particle_counts['y'] = config['nYellow']
            if self.verbose:
                print '\033[1m* \033[33m' + str(config['nYellow']) + ' Yellow Particles Added\033[0m'
        if 'nMagenta' in config.keys():
            self.particle_counts['m'] = config['nMagenta']
            if self.verbose:
                print "\033[1m* \033[35m" + str(config['nMagenta']) + ' Magenta Particles added\033[0m'

    def construct_cloud(self, config, RGB):
        has_time = False
        try:
            self.timescale = config['timescale']
            if self.verbose:
                print '* Constructing Simulation with ' + str(self.timescale) + " time steps "
            has_time = True
        except KeyError:
            pass

        world = np.zeros((self.width,self.height,3))
        cloud = {}
        ii = 0
        for ptype in self.particle_counts.keys():
            color = RGB.handles[ptype]
            for particle in range(self.particle_counts[ptype]):
                pt = utility.spawn_random_point(world)
                obj = ColorAutomataSimulations.Particle(ptype,pt)
                if has_time:
                    obj.generate_random_steps(self.timescale)
                world[pt[0], pt[1], :] = color[:, :, :]
                cloud[ii] = obj
                ii += 1
        return world, cloud

    def particle_recount(self):
        recount = {'r': 0, 'g': 0, 'b': 0, 'c': 0, 'y': 0, 'm': 0, 'w': 0}
        for particle in self.particle_data.values():
            recount[particle.color] += 1
        self.particle_counts = recount

    def run(self, RGB, animate, save):
        t0 = time.time()
        print 'Initial Particle Count'
        print str(self.particle_counts) + '\t' + str(len(self.particle_data.keys())) + ' Particles '
        model = ColorAutomataSimulations.StandardModel()
        model.initialize()
        if animate:
            f = plt.figure()
            film = []
        world = np.zeros(self.state.shape)
        collisions = []
        for step in range(self.timescale-1):
            for pid in self.particle_data.keys():
                try:
                    point = self.particle_data[pid]
                    # Particle Collisions
                    for pt in self.particle_data.keys():
                        if [self.particle_data[pt].x, self.particle_data[pt].x] == [point.x, point.y] and pt != pid:
                            collisions.append([point.color, self.particle_data[pt].color])
                            # TODO: Use ColorAutomataSimulations.StandardModel to handle collisions!
                            hitA = [str(point.color).upper(),str(self.particle_data[pt].color).upper(),'+']
                            hitB = [hitA[1], hitA[0], hitA[2]]
                            if hitA in model.events.values():
                                h = 0
                                for he in model.events.values():
                                    if he == hitA:
                                        point.color = model.rules[h]
                                        self.particle_data.pop(pt)
                                    h += 1
                            elif hitB in model.events.values():
                                k = 0
                                for it in model.events.values():
                                    if it == hitB:
                                        point.color = model.rules[k]
                                        self.particle_data.pop(pt)
                                    k += 1
                    world[point.x, point.y, :] = 0
                    point.set_position(point.steps[step])
                    world[point.x, point.y, :] = RGB.handles[point.color]
                except IndexError:
                    pass
                except KeyError:
                    pass
            ''' TODO:  
            Probability-based Particle state changes 
            '''
            if animate:
                film.append([plt.imshow(world)])
        self.particle_recount()
        print '\033[1mSimulation Finished \033[31m[' + str(time.time() - t0) + 's Elapsed]\033[0m'
        print " ** \033[1m\033[32m" + str(len(collisions)) + ' Particle Collisions Recorded\033[0m'
        print 'Final Particle Count:'
        print str(self.particle_counts) + '\t' + str(len(self.particle_data.keys()))+ ' Particles '
        if animate:
            a = animation.ArtistAnimation(f,film, interval=40,blit=True,repeat_delay=900)
            if save:
                w = FFMpegWriter(fps=40,bitrate=1800)
                a.save('particles_life_rules.mp4', writer=w)
            plt.show()
        return collisions
