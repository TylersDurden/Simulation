from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import utility
import time
import sys


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

    def run(self):
        # Setup Initial State
        state = np.zeros((self.width, self.height, 3))
        for pdpos in self.Predator_Starts.values():
            state[pdpos[0],pdpos[1],:] = self.R
        for pypos in self.Prey_Starts.values():
            state[pypos[0],pypos[1],:] = self.B
        plt.imshow(state)
        plt.title('INITIAL_STATE')
        plt.show()

        # Predators have initial advantage and scope world first
        pred_rvecs = {}
        for pred_pos in self.Predator_Starts.values():
            for prey_pos in self.Prey_Starts.values():
                pred_rvecs[float(utility.get_displacement([pred_pos[0], pred_pos[1]],
                                                          [prey_pos[0], pred_pos[1]]))] = \
                    [pred_pos, prey_pos]

        '''    Now Do the Chasing    '''
        # TODO: How Will Predators Choose WHICH prey to chase first?
        # TODO: Make them know to switch targets if another is closer?
        # TODO: Remove prey from state and calculations after captured

def main():
    # Define World Parameters
    width = 250
    height = 250

    N_Predators = 2
    N_Prey = 3

    # Simulation Parameters
    N_Steps = 200
    pred_starts_random = False
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