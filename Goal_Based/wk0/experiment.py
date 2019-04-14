import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import utility
import time
import sys


class EvolutionaryCrawler:
    start = []
    goal = []
    pool_size = 0
    depth = 0
    distance = 0
    iterations = 0

    def __init__(self, r, a, b, walk_size, batch_size, n_batches):
        self.distance = r
        self.start = a
        self.goal = b
        self.depth = walk_size
        self.pool_size = batch_size
        self.iterations = n_batches

        self.process_batch(self.initialize())

    def seed_gene_pool(self):
        genetics = list()
        for i in range(self.pool_size):
            genetics.append(np.random.random_integers(1, 9, self.depth))
        return genetics

    def process_batch(self, batch_data):
        walk_data = {}
        for pool_id in batch_data.keys():
            walk_data[pool_id] = self.pool_processor(pool_id, batch_data[pool_id])

    def pool_processor(self, pool_id, gene_pool):
        best_scores = {}
        trace = []
        helix = 0

        for pool in gene_pool.keys():
            a = self.start
            for random_walk in gene_pool[pool]:
                best_steps, score = self.first_layer_eval(random_walk)
        return best_scores

    def first_layer_eval(self, path):
        best_steps = []
        score = 0

        return best_steps, score

    def initialize(self):
        seed_genome = {}
        for i in range(self.iterations):
            seed_genome[i] = self.seed_gene_pool()
        return seed_genome


def track_path(walk, start, stop, show):
    displacement = list()
    dist_to_goal = list()
    initial_distance = np.sqrt((start[0]-stop[0])**2 + (start[1]-stop[1])**2)
    for step in walk:
        dx = step[0] - start[0]
        dy = step[1] - start[1]
        gx = step[0] - stop[0]
        gy = step[1] - stop[1]
        rD = np.sqrt((dx**2) + (dy**2))
        rG = np.sqrt((gx**2) + (gy**2))
        displacement.append(rD)
        dist_to_goal.append(rG)
    drd = np.diff(np.array(displacement)[1:])
    drg = dist_to_goal[2:]+np.diff(np.array(dist_to_goal)[1:])

    best_dist = drg.min()           # Using the derivative of dist to goal (drg) and
    mark_bd = 0                     # the derivative of displacement Find the longest
    mark_pt = []                    # sequence of overall positive slope [noting start
    i = 0                           # pos of positive slope], and hopefully scan through
    for pt in drg.flatten():        # while increasing derivative threshold, and in the
        if pt == best_dist:         # end find the longest sequence of steps which lead
            mark_bd = i             # to the most positive increase in both displacement,
            mark_pt.append(i)       # minimizing distance to goal, and steps that did both
        i += 1                      # at the same time!

    # print "Initial Goal Distance: " + str(initial_distance)
    # print "Minimum Goal Distance: " + str(dist_to_goal[mark_bd+2]) + " @ ["+str(walk[mark_bd+2]) + \
    #       ']('+str(mark_bd)+')'
    # print '=========================================================================================='
    if show:
        plt.plot(displacement)
        plt.plot(dist_to_goal)
        plt.plot(drg)
        plt.plot(drd)
        plt.grid()
        plt.legend(['displacement', 'dist. to goal', 'dG/dt', 'dR/dt'])
        plt.show()
    return dist_to_goal[mark_bd+2], walk[mark_bd+2], mark_bd+2


def main():
    t0 = time.time()

    A = [0, 0]
    B0 = [100, 100]
    depth = 150
    batch_size = 750
    n_batches = 250
    r = np.sqrt((A[0]-B0[0])**2 + (A[1]-B0[1])**2)
    mutation_markers = {}
    progress = []
    '''
        Using the derivative of dist to goal (drg) and
        the derivative of displacement, Find the longest
        sequence of overall positive slope [noting start
        pos of positive slope], and hopefully scan through
        while increasing derivative threshold. 
        
        *  Find the longest sequence of steps which lead to the 
           most positive increases in displacement, 
        
        *  minimize distance to goal
        
        *  reward steps that do both at the same time! 

    '''
    EvolutionaryCrawler(r, A, B0, depth, batch_size, n_batches)
    print '\033[1mSimulation FINISHED \033[34m['+str(time.time()-t0)+'s Elapsed]\033[0m'
    if '-brute' in sys.argv:
        print '\033[1m\033[31m\t:: BEGINNING BRUTE_FORCE SEARCH :: \033[0m'
        print '\033[1m\033[33mUsing Random Walk Seed Length:\033[0m\033[1m ' + str(depth) + '\033[0m'
        print '\033[1m\033[33mUsing Batch Size:\033[0m\033[1m ' + str(batch_size) + '\033[0m'
        print '\033[1m\033[33mUsing N Batches:\033[0m\033[1m ' + str(n_batches) + '\033[0m'
        brute_points = []
        t = []
        for j in range(n_batches):
            for i in range(batch_size):
                random_walk, score = utility.spawn_random_walk(A, depth)
                best_dist, best_pt, mark = track_path(random_walk, A, B0, False)
                mutation_markers[i] = mark
                progress.append(best_dist)
            brute_points.append(np.array(progress).min())
            t.append(time.time() - t0)
        print '\033[1mFINISHED \033[31m[' + str(time.time() - t0) + 's Elapsed]\033[0m'
        print str(A) + '--?--' + str(B0) + '\033[1m\tDistance:' + str(r) + '\033[0m'
        print "MINIMUM DISTANCE TO GOAL FOUND: " + str(np.array(progress).min())

        plt.title('Brute Force Search')
        plt.xlabel('time (s)')
        plt.ylabel('Minimum Distance To Goal Found')
        plt.plot(t, np.array(brute_points))
        plt.show()


if __name__ == '__main__':
    main()
