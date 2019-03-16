import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import evoutils
import time
import sys


class EvolutionaryCrawler:
    DNA = {}
    n_batches = 0
    n_walks_per_batch = 0
    n_steps_per_walk = 0
    world = [[]]

    def __init__(self, genes, paths):
        self.DNA = genes
        self.n_batches = len(genes.keys())
        self.n_walks_per_batch = len(genes[genes.keys()[0]])
        self.n_steps_per_walk = len(genes[genes.keys()[0]][0])
        # Generate a landscape for the walk to attempt to navigate
        self.world = evoutils.generate_random_landscape(250, 250, 4)

    def batch_cycle(self):
        n_steps = 0
        steps = 0
        for batch in self.DNA.keys():
            for walkers in range(self.n_walks_per_batch):
                for step in self.DNA[self.DNA.keys()[batch]][walkers]:

                    n_steps += 1

        print "FINISHED " + str(n_steps) + " WALKS TOTAL"
        print steps
        
    def show_fields(self):
        print "N Batches: " + str(self.n_batches)
        print "Batch Size: " + str(self.n_walks_per_batch)
        print "N Steps Per Walk: " + str(self.n_steps_per_walk)


def generate_universal_surface(settings):
    randomness = 0.3
    if 'random' in settings.keys():
        randomness = settings['random']


def main():
    full_scale = True
    t0 = time.time()

    # SETUP #
    settings = {'print_outs': False,
                'start': [0, 0],
                'stop': [100, 100],
                'r0': 0,
                'debugging': False,
                'randomized': True,
                'pool_size': 100,
                'walk_length': 150}

    r0 = evoutils.get_separation(settings['start'], settings['stop'])
    settings['r0'] = r0

    # MODES OF OPERATION #
    if 'one_shot' in sys.argv:
        basic_seed, disp_tracks = evoutils.generate_random_pool(settings)
        evoutils.show_bulk_data(disp_tracks)
        full_scale = False

    if full_scale:
        genetics, traces = evoutils.pool_initialization(settings, 10)
        ec1 = EvolutionaryCrawler(genetics, traces)
        ec1.show_fields()
        ec1.batch_cycle()

    print str(time.time() - t0) + 's Elapsed'


if __name__ == '__main__':
    main()