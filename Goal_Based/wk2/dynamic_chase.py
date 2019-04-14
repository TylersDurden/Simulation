from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import utility
import time
import sys


class Predator:
    x = 0
    y = 0
    prey = []
    target = []
    steps = []
    displacement = []

    def __init__(self,position):
        self.x = position[0]
        self.y = position[1]

    def assign_targets(self,prey):
        [self.prey.append(target) for target in prey]

    def asses_targets(self):
        displacements = {}
        for prey in self.prey:
            displacements[float(utility.get_displacement([self.x,self.y], [int(prey[0]),int(prey[1])]))] =\
                [int(prey[0]),int(prey[1])]
        closest = np.array(displacements.keys()).min()
        self.target = closest

    def set_position(self, position):
        self.x = position[0]
        self.y = position[1]

class Prey:
    x = 0
    y = 0
    steps = []

    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]


class ComplexChase:
    width = 0
    height = 0

    # Some Basic hardcoded color values for repeated use
    R = np.zeros((1, 1, 3))
    G = np.zeros((1, 1, 3))
    B = np.zeros((1, 1, 3))
    R[:, :, 0] = 1
    G[:, :, 1] = 1
    B[:, :, 2] = 1

    def __init__(self, config):
        self.width = config['dims'][0]
        self.height = config['dims'][1]
        self.N_Predators = config['n_pred']
        self.N_Prey = config['n_prey']
        self.N_Steps = config['n_steps']
        self.Predator_Starts = config['pred_start_points']
        self.Prey_Starts = config['prey_start_points']
        self.pred_starts_random = config['pred_starts_random']
        self.prey_starts_random = config['prey_starts_random']

        # Start Setting up the Simulation Params
        if self.pred_starts_random:
            for pd in range(self.N_Predators):
                self.Predator_Starts[pd] = utility.spawn_random_point(np.zeros((self.width,
                                                                                self.height)))
        else:
            for d in range(self.N_Predators):
                x1 = int(raw_input('Enter Predator(s) x1:'))
                y1 = int(raw_input('Enter Predator(s) y1:'))
                print '1 Predator will Be Initialized @ \033[1m\033[33m[' + \
                      str(x1) + ',' + str(y1) + ']\033[0m'
                pred_start = [x1, y1]
                self.Predator_Starts[d] = pred_start
        if self.prey_starts_random:
            print "\033[1m\033[31m[*] Prey Will Start From Random Locations [*]\033[0m"
            for py in range(self.N_Prey):
                self.Prey_Starts[py] = utility.spawn_random_point(np.zeros((self.width,
                                                                            self.height)))
        else:
            for y in range(self.N_Prey):
                x1 = int(raw_input('Enter Prey(s) x1:'))
                y1 = int(raw_input('Enter Prey(s) y1:'))
                print '1 Prey will Be Initialized @ \033[1m\033[33m[' + \
                      str(x1) + ',' + str(y1) + ']\033[0m'
                prey_start = [x1, y1]
                self.Prey_Starts[y] = prey_start

        # Display Simulation Settings/Parameters
        print str(len(self.Prey_Starts)) + ' Different Predator Starting Locations ' + str(self.N_Prey) + ' Prey]'
        print str(len(self.Predator_Starts)) + ' Different Prey Starting Locations [' + str(self.N_Predators) + ' Predators]'
        print '\033[1m\033[32m========================= :: BEGINNING_SIMULATION :: =======' \
              '====================\033[0m'

    def initialize_state(self):
        state = np.zeros((self.width, self.height, 3))
        for pdpos in self.Predator_Starts.values():
            state[pdpos[0], pdpos[1], :] = self.R
        for pypos in self.Prey_Starts.values():
            state[pypos[0], pypos[1], :] = self.B
        # plt.imshow(state)
        # plt.title('INITIAL_STATE')
        # plt.show()
        return state

    def run(self):
        # Setup Initial State
        state = self.initialize_state()

        # Predators have initial advantage and scope world first
        Predators = self.initialize_predators()

        # Now set up the Prey
        Prey = self.initialize_prey()

        f = plt.figure()
        film = []
        # Do the chasing
        for step in range(self.N_Steps):
            for prey in Prey:
                try:
                    pos = prey.steps[step]
                    for predator in Predators:
                        target = prey
                        dx = prey.x-predator.x
                        dy = prey.y-predator.y
                        r = dx**2+dy**2
                        predator.displacement.append(r)
                        if np.abs(dx) > np.abs(dy):
                            if dx < 0:
                                predator.set_position([predator.x - 1, predator.y])
                            if dx > 0:
                                predator.set_position([predator.x + 1, predator.y])
                        if abs(dx) < abs(dy):
                            if dy > 0:
                                predator.set_position([predator.x, predator.y + 1])
                            if dy < 0:
                                predator.set_position([predator.x, predator.y - 1])
                        predator.steps.append([predator.x, predator.y])
                        state[predator.x, predator.y, :] = self.R
                    state[pos[0], pos[1], :] = self.B
                    film.append([plt.imshow(state)])

                except IndexError:
                    pass

        a = animation.ArtistAnimation(f,film,interval=40,blit=True,repeat_delay=900)
        plt.show()
        # TODO: How Will Predators Choose WHICH prey to chase first?
        # TODO: Make them know to switch targets if another is closer?
        # TODO: Remove prey from state and calculations after captured


    def initialize_predators(self):
        predators = []
        for pred_pos in self.Predator_Starts.values():
            p = Predator(pred_pos)
            prey = []
            for prey_pos in self.Prey_Starts.values():
                prey.append(prey_pos)
            p.assign_targets(prey)
            p.asses_targets()
            predators.append(p)
        return predators

    def initialize_prey(self):
        prey = []
        for p in self.Prey_Starts.values():
            prey_movts = []
            [prey_movts.append(step) for step in utility.spawn_random_walk(p, self.N_Steps)]
            pobj = Prey(p)
            pobj.steps = prey_movts
            prey.append(pobj)
        return prey


def main():
    # Define World Parameters
    width = 250
    height = 250

    N_Predators = 2
    N_Prey = 30

    # Simulation Parameters
    N_Steps = 200
    pred_starts_random = True
    prey_starts_random = True
    predator_starts = {}
    prey_starts = {}

    simulation_data = {'dims': [width, height],
                       'n_prey': N_Prey,
                       'n_pred': N_Predators,
                       'n_steps': N_Steps,
                       'prey_starts_random': prey_starts_random,
                       'pred_starts_random': pred_starts_random,
                       'pred_start_points': predator_starts,
                       'prey_start_points': prey_starts}

    CC = ComplexChase(simulation_data)
    CC.run()


if __name__ == '__main__':
    main()