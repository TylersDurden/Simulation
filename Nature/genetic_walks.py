import matplotlib.pyplot as plt
import numpy as np
import utility
import time
import sys


def spawn_random_walk(position, n_steps):
    choice_pool = np.random.randint(1, 10, n_steps)
    random_walk = list()
    for step in choice_pool:
        directions = {1: [position[0]-1, position[1]-1],
                      2: [position[0]-1, position[1]],
                      3: [position[0]-1, position[1]+1],
                      4: [position[0], position[1]-1],
                      5: position,
                      6: [position[0], position[1]+1],
                      7: [position[0]+1, position[1]-1],
                      8: [position[0]+1, position[1]],
                      9: [position[0]+1, position[0]+1]}
        random_walk.append(directions[step])
        position = directions[step]
    return random_walk, choice_pool


def track_walk(start, goal, steps):
    displacement = []
    from_goal = []
    for step in steps:
        r = [(step[0] - goal[0]), (step[1] - goal[1])]
        g = np.sqrt(r[0] * r[0] + r[1] * r[1])
        r = np.sqrt((step[0]-start[0])*(step[0]-start[0]) + (step[1]-start[1])*(step[1]-start[1]))
        from_goal.append(g)
        displacement.append(r)
    dG = np.diff(np.array(from_goal)[1:])
    dR = np.diff(np.array(displacement)[1:])
    return displacement, from_goal, dG, dR


def fitness(start,stop,path, dG, ddG, dR, ddR, state, show):
    fitness = []
    ii = 0
    for step in path[2:]:
        if ddR[ii] >= 0:
            fitness.append(True)
        if ddR[ii] > 0 >= ddG[ii]:
            fitness.append(True)
        if 0 >= ddG[ii]:
            fitness.append(True)
        else:
            fitness.append(False)
        ii += 1
    if show:
        f, ax = plt.subplots(1,2)
        ax[0].imshow(draw_walk(state, start, stop, path), 'gray')
        ax[1].plot(dG)
        ax[1].plot(dR)
        plt.show()
    return fitness


def draw_walk(initial_state, start, target, walk):
    state = initial_state
    state[start[0],start[1]] = 1
    state[target[0]:target[0]+5, target[1]:target[1]+5] = -1
    for step in walk:
        state[step[0], step[1]] = 1
    return state


def mutate(sequence, walk, fitness, mutation_factor):
    new_walk = []
    mutate = np.random.random_integers(0, 2, int(mutation_factor*len(walk)))
    m = np.abs(np.random.randn(len(walk))) < mutation_factor
    ii = 0
    for step in sequence:
        try:
            if fitness[ii]:
                new_walk.append(step)
            else:
                if m[ii]:
                    new_walk.append(np.random.random_integers(1, 9, 1)[0])
                else:
                    new_walk.append(step)
        except IndexError:
            new_walk.append(np.random.random_integers(1, 9, 1)[0])
            pass
        ii += 1
    position = walk[0]
    random_walk = list()
    for step in new_walk:
        directions = {1: [position[0] - 1, position[1] - 1],
                      2: [position[0] - 1, position[1]],
                      3: [position[0] - 1, position[1] + 1],
                      4: [position[0], position[1] - 1],
                      5: position,
                      6: [position[0], position[1] + 1],
                      7: [position[0] + 1, position[1] - 1],
                      8: [position[0] + 1, position[1]],
                      9: [position[0] + 1, position[0] + 1]}
        random_walk.append(directions[step])
        position = directions[step]
    return random_walk


class GeneticWalkers:
    n_walkers = 0
    walk_size = 0
    mutate_factor = 0.0
    paths = {}
    walker_data = {}
    state = [[]]
    has_start = False
    has_end = False
    defined_start = []
    defined_end = []
    solved = False
    isVerbose = False
    animate = False
    TOTAL_WALKS = 0

    def __init__(self, n, m, opts, dims, verbosity):
        self.isVerbose = verbosity
        self.initialize(n, m, opts, dims)

    def run(self):
        simulation = []
        paths = {}
        for seed in range(self.n_walkers):
            if self.has_start and self.has_end:
                random_walk, sequence = spawn_random_walk(self.defined_start, self.walk_size)
                dR, dG, ddG, ddR = track_walk(self.defined_start, self.defined_end, random_walk)
                f = fitness(self.defined_start,
                                  self.defined_end,
                                  random_walk,
                                  dG,ddG,dR,ddR,
                                  self.state, False)
                paths[seed] = random_walk
                self.paths[seed] = random_walk
                self.walker_data[seed] = [f, sequence, random_walk, dR, dG, ddR, ddG]
            else:
                print "This feature is undeveloped for now! "
                exit(0)
        while not self.solved:
            # TODO: Check if any walks reached goal
            for step_id in self.paths.keys():
                if not self.check_solved(self.paths[step_id]):
                    fit = self.walker_data[step_id][0]
                    seq = self.walker_data[step_id][1]
                    walk = self.walker_data[step_id][2]
                    child = mutate(seq, walk, fit, self.mutate_factor)
                    self.paths[step_id] = child
                    self.walker_data[step_id] = [fit, seq, child]
                else:
                    print "Finished!"
                    self.solved = True
                    return self.paths[step_id], step_id
        return simulation, step_id

    def check_solved(self, path):
        self.TOTAL_WALKS += 1
        if self.has_end:
            for step in path:
                if step[0] == self.defined_end[0] and step[1] == self.defined_end[1]:
                    return path
                    print "SOLVED!"
                    exit(0)
        else:
            print "No Endpoint has been specified :("
            return []

    def initialize(self,walkers,steps,args, state):
        self.n_walkers = walkers
        self.walk_size = steps
        if len(args.keys()) > 0:
            self.argparse(args)
        self.state = state

    def argparse(self, args):
        if 'start' in args.keys():
            self.defined_start = args['start']
            self.has_start = True
        if 'stop' in args.keys():
            self.defined_end = args['stop']
            self.has_end = True
        if 'mutation' in args.keys():
            self.mutate_factor = float(args['mutation'])
        if 'animate' in args.keys():
            self.animate = args['animate']
        if self.isVerbose:
            print '\033[1m* Starting Point Defined at \033[32m' + str(self.defined_start)+'\033[0m'
            print '\033[1m* End Point Defined at \033[36m' + str(self.defined_end)+'\033[0m'
            print '\033[1m* Using a Mutation Factor of: \033[35m' + str(self.mutate_factor)+'\033[0m'
            print '\033[1m* Gene Pool Size: \033[33m' + str(self.n_walkers)+'\033[0m'
            print '\033[1m* Walk Length [Steps]: \033[93m' + str(self.walk_size)+'\033[0m'


def main():
    T0 = time.time()
    # SINGLE WALK

    state = np.zeros((250, 250))
    start = [15, 15]
    target = [184, 186]
    state[target[0]-1:target[0]+1,target[1]-1:target[1]+1] = 1
    R = np.sqrt((target[0]-start[0])**2 + (target[1]-start[1])**2)
    print '\033[1m\033[31mTARGET IS ' + str(R) + ' units away\033[0m'
    n_steps = 255

    if '-test' in sys.argv:
        random_walk, sequence = spawn_random_walk(start, n_steps)
        dR, dG, ddG, ddR = track_walk(start, goal=target, steps=random_walk)
        evaluated = fitness(start, target, random_walk, dG, ddG, dR, ddR, state, False)
        child_walk = mutate(sequence, random_walk, evaluated, 0.5)

    g = GeneticWalkers(15000, n_steps, {'start':start,'stop':target,'mutation': 0.5, 'animate':True}, state, True)
    try:
        simulation_data, step_id = g.run()
        # print str(len(simulation_data)) + "[simulation size]"
        if g.animate:
            utility.render_random_walk(simulation_data, g.state, 100, True, 'firefly.mp4')
    except KeyboardInterrupt:
        pass

    DT = time.time()-T0
    print '\033[1mFINISHED ['+str(DT)+'s Elapsed]'
    print '\033[31m'+str(g.TOTAL_WALKS) + ' Total Walks Simulated \033[0m'


if __name__ == '__main__':
    main()

