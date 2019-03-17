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
        # Seed the Crawler's GenePool with Random Walks Data
        self.initialize(genes, settings)
        self.show_fields()
        # self.world = evoutils.generate_random_landscape(250, 250, 4)  TODO: Save this for later, too complex

        # Generate a landscape for the walk to attempt to navigate
        self.world = evoutils.generate_simple_landscape(250, 250, 5)
        self.world[self.goal[0]:self.goal[0]+5,self.goal[1]:self.goal[1]+5] = -1

        # [1] Convert random gene pool to walk data and Evaluate
        genome = self.batch_cycle()

        # Return indexed scores for Fitness Evaluation
        scores, best_walk = self.distance_evaluation(genome)
        # evoutils.animate_walk(self.start, best_walk, self.world)

        # [2] SELECTION PROCESS
        radial_pts, fitness_ids = self.prune_batch_data(scores, True)
        fitness = self.assign_fitness(radial_pts,fitness_ids,genome)
        # Create mechanism for randomly selecting from Pool
        # Then use it to cross-over/mutate from new genetics
        evoutils.show_bulk_subplot(scores, fitness, {'f1': {'title': 'Initial Pop.'},
                                                     'f2': {'title': 'Pruned Pop*Fitness'}})
        self.mutation(0.5,genome,fitness_ids, fitness)

    def mutation(self, rate, dna, fitness_markers, fitness):
        DNA = {}
        fit = 0
        for genome_id in dna.keys():
            if genome_id in fitness_markers.keys():
               fit += 1
        print fit
        return DNA

    def assign_fitness(self, radial_pts, fitness_ids, genome):
        fitness = {}
        if len(fitness_ids.keys()) != len(radial_pts.keys()):
            print '\033[1m\033[31m  Dimensions of Data are Incorrect! \033[0m'
            exit(0)
        for gene_id in genome.keys():
            try:
                radial_displacement = radial_pts[gene_id]
                fitness[gene_id] = np.array(radial_displacement)
            except KeyError:
                pass
        return fitness

    def prune_batch_data(self,scores, verbose):
        # First, Prune Out terrible paths
        data_pts = {}
        fit_map = {}
        id = 0
        ii = 0
        for trace in scores.values():
            features = []
            for step in trace:
                features.append(step)
            if np.array(features).mean() < self.initial_distance:
                data_pts[ii] = features
                ii += 1
                fit_map[id] = ii
            id += 1
        if verbose:
            # evoutils.show_bulk_data(data_pts, {})
            p_ratio = len(data_pts.keys())/float(len(scores.keys()))*100
            print str(p_ratio) + '% of Paths Pruned ['+str(len(data_pts.keys())) +\
                                 ' Paths Remaining for Mutation/Crossover]'
        return data_pts, fit_map

    def distance_evaluation(self, genome):
        solved = False
        best_score = self.initial_distance
        best_walk = 0
        walker_scores = {}
        for gene_id in genome.keys():
            walk = genome[gene_id]
            data = []
            for step in walk:
                # self.world[step[0], step[1]]
                score = evoutils.get_separation(step, self.goal)
                if score == 0:
                    print "SOLVED "
                    solved = True
                    break
                data.append(score)
            if score < best_score:
                best_score = score
                best_walk = gene_id
            walker_scores[gene_id] = np.array(data)
            if solved:
                break
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
                'start': [40, 50],
                'stop': [0, 0],
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
        genetics, traces = evoutils.pool_initialization(settings, 1)
        ec1 = EvolutionaryCrawler(genetics, settings)


    print str(time.time() - t0) + 's Elapsed'


if __name__ == '__main__':
    main()