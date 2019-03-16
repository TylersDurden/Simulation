import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import evoutils
import time
import numpy as np


def generate_random_pool(settings):
    seed_data = {}
    random_displacements = {}
    verbose = False
    if 'print_outs' in settings.keys():
        verbose = True
    batch_size = settings['pool_size']
    walk_length = settings['walk_length']
    for pool_id in range(batch_size):
        step = settings['start']
        steps = []
        displacement = []
        for s in np.random.random_integers(1,9,walk_length).flatten():
            options = {1: [step[0] - 1, step[1] - 1],
                       2: [step[0] - 1, step[1]],
                       3: [step[0] - 1, step[1] + 1],
                       4: [step[0] - 1, step[1]],
                       5: step,
                       6: [step[0] + 1, step[1]],
                       7: [step[0] + 1, step[1] - 1],
                       8: [step[0] + 1, step[1]],
                       9: [step[0] + 1, step[1] + 1]}
            step = options[s]
            steps.append(options[s])
            displacement.append(evoutils.get_separation(settings['start'],options[s]))
        seed_data[pool_id] = steps
        random_displacements[pool_id] = displacement
    n_steps_total = len(seed_data.keys())*len(seed_data.values())
    if verbose:
        print "Finished Simulation "
        print '\033[1mN Batches: '+str(batch_size)
        print 'Walk Length: ' + str(walk_length)
        print str(n_steps_total) + ' Steps Total\033[0m'
    return seed_data, random_displacements


def main():
    t0 = time.time()
    settings = {'print_outs': True,
                'start': [],
                'stop': [],
                'r0': 0,
                'debugging': True,
                'randomized': True,
                'pool_size': 100,
                'walk_length': 150}
    start = [0, 0]
    goal = [100, 100]
    r0 = evoutils.get_separation(start, goal)
    settings['start'] = start
    settings['stop'] = goal
    settings['r0'] = r0

    seed_pool, walk_traces = generate_random_pool(settings)
    print str(time.time()-t0) + 's Elapsed'
    evoutils.show_bulk_data(walk_traces)
    '''
    get the distribution of end displacements and sort paths based on this
    get the distribution of min dist to goal and sort paths based on this
    '''


if __name__ == '__main__':
    main()