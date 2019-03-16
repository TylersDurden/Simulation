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

    start = []
    goal = []
    initial_distance = 0

    def __init__(self, genes, settings):
        self.initialize(genes, settings)
        # Generate a landscape for the walk to attempt to navigate
        # self.world = evoutils.generate_random_landscape(250, 250, 4)  TODO: Save this for later, too complex
        self.world = evoutils.generate_simple_landscape(250, 250, 5)
        self.world[self.goal[0]:self.goal[0]+5,self.goal[1]:self.goal[1]+5] = -1
        # Convert random gene pool to walk data and Evaluate
        # Then return indexed scores for Fitness Evaluation
        genome = self.batch_cycle()
        scores, best_walk = self.distance_evaluation(genome)
        # SELECTION PROCESS
        # evoutils.animate_walk(self.start, best_walk, self.world)
        evoutils.show_bulk_data(scores, {'title': 'Initial Population',
                                         'ylabel': 'Distance From Goal',
                                         'xlabel': 'N Steps'})

        # Create mechanism for randomly selecting from Pool
        # Then use it to cross-over/mutate from new genetics


    def distance_evaluation(self, genome):
        best_score = self.initial_distance
        best_walk = 0
        walker_scores = {}
        for gene_id in genome.keys():
            walk = genome[gene_id]
            data = []
            for step in walk:
                # self.world[step[0], step[1]]
                score = evoutils.get_separation(step, self.goal)
                data.append(score)
            if score < best_score:
                best_score = score
                best_walk = gene_id
            walker_scores[gene_id] = np.array(data)
        return walker_scores, genome[best_walk]

    def initialize(self, genes, settings):
        self.DNA = genes
        self.n_batches = len(genes.keys())
        self.n_walks_per_batch = len(genes[genes.keys()[0]])
        self.n_steps_per_walk = len(genes[genes.keys()[0]][0])
        self.start = settings['start']
        self.goal = settings['stop']
        self.initial_distance = evoutils.get_separation(self.start, self.goal)

    def batch_cycle(self):
        n = 0
        genetic_data = {}
        for batch in self.DNA.keys():
            for walkers in range(self.n_walks_per_batch):
                dna = self.DNA[self.DNA.keys()[batch]][walkers]
                genetic_data[n] = evoutils.dna2steps(self.start, dna)
                n += 1
        return genetic_data

    def show_fields(self):
        print '================================='
        print '\033[1m| EVOLUTIONARY_CRAWLER SETTINGS |\033[0m'
        print '================================='
        print '\033[1m\033[32mN Batches: \033[0m' + str(self.n_batches)
        print "\033[1m\033[34mBatch Size: \033[0m" + str(self.n_walks_per_batch)
        print "\033[1m\033[31mN Steps Per Walk: \033[0m" + str(self.n_steps_per_walk)
        print '================================='


def main():
    full_scale = True
    t0 = time.time()

    # SETUP #
    settings = {'print_outs': False,
                'start': [100, 100],
                'stop': [0, 0],
                'r0': 0,
                'debugging': False,
                'randomized': True,
                'pool_size': 400,
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
        ec1 = EvolutionaryCrawler(genetics, settings)
        ec1.show_fields()

    print str(time.time() - t0) + 's Elapsed'


if __name__ == '__main__':
    main()