from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import utility


def generate_primitives(n_blocks, psize):
    primitives = {}
    primitives[-1] = np.zeros(psize)

    for i in range(n_blocks):
        pxls = np.random.random_integers(0,1,psize[0]*psize[1]).reshape(psize)
        primitives[i] = pxls
    scores = count_blocks(primitives)
    return primitives, scores


def count_blocks(primitives):
    diplomat = {}
    for c in primitives.keys():
        score = np.count_nonzero(np.array(primitives[c]))
        diplomat[score] = primitives[c]
    return diplomat


def generate_random_col(primitives,depth, ncols, show):
    columns = np.zeros((primitives[0].shape[0]*depth,ncols*primitives[0].shape[0]))
    k = primitives[0].shape[0]
    for i in range(ncols):
        col = primitives[-1]
        for j in np.random.random_integers(0, 10, depth):
            col = np.array(np.concatenate((col, primitives[j - 1]), 0))
        columns[:,k*i:k*i+k] = col[:-k,:]
    # Add Padding
    columns[:,0:k] = 0
    columns[:,columns.shape[1] - k:columns.shape[1]] = 0
    columns[columns.shape[0]-k:columns.shape[0],:] = 0
    if show:
        plt.imshow(columns, 'gray')
        plt.show()

    return columns


def wander(maze,start,n_steps,display):
    walk, dna = utility.spawn_random_walk(start,n_steps)
    steps = 0
    correct = []
    for step in walk:
        spot = maze[step[0], step[1]]
        if spot == 1:
            break
        correct.append(step)
        steps += 1
    if display:
        print "Made it " + str(steps) + " Steps"
    return steps, correct, dna


def evolution_brute(start, maze, limit):
    step_levels = np.linspace(10, 350, limit)
    print str(len(step_levels)) + " Levels of Step-Length Created"
    maxima = 0
    fittest = {}
    while maxima < 150:
        for stepnum in step_levels:
            n_steps = int(stepnum)
            score, path, dna = wander(maze, start, n_steps, False)
            if score > maxima:
                maxima = score
                fittest[maxima] = path
    print str(len(fittest.keys())) + " Different Lengths of Walk Saved"
    print "Longest Walk: " + str(maxima)
    print fittest.keys()
    return fittest[maxima], fittest


def draw_walk(path, start, world):
    f = plt.figure()
    film = []
    for step in path:
        world[step[0],step[1]] = 1
        film.append([plt.imshow(world, 'gray')])
        world[step[0],step[1]] = 0
    a = animation.ArtistAnimation(f,film,interval=40,blit=True,repeat_delay=900)
    plt.show()


def main():
    N = 16
    psize = np.zeros((4, 4)).shape
    primitives, scores = generate_primitives(10, psize)
    g2 = generate_random_col(primitives, N, N, False)
    generated_maze = np.abs(g2 - generate_random_col(primitives, N, N, False))

    start = [1, 1]
    goal = []

    ''' STRATEGIES 
    [1] create an expanding search radius of random walks
    and mutate these with the solutions that have lived 
    
    [2] using batches of same step sized walks, slowly
    evolve towards correct solution. 
    
    [3] Brute Force + Evolution : Random Walks of entire total
    radius modified with evolution to help converge slightly 
    faster
    '''
    # best_walk, candidates = evolution_brute(start,generated_maze,100)
    # draw_walk(best_walk,start,world=generated_maze)
    # for parent in candidates.keys():
    #     draw_walk(candidates[parent], start, world=generated_maze)

if __name__ == '__main__':
    main()
