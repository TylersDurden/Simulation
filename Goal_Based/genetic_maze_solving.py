from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import genetic_maze_builder
import scipy.ndimage as ndi
import numpy as np
import utility


def evolution_brute(start, maze, limit):
    step_levels = np.linspace(10, 150, limit)
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


def wander(maze,start,n_steps,display):
    walk, dna = utility.spawn_random_walk(start,n_steps)
    steps = 0
    correct = []
    for step in walk:
        spot = maze[step[0], step[1]]
        if spot == 1:
            try:
                walk = utility.spawn_random_walk([step[0], step[1]], len(walk) - steps)
            except ValueError:
                break
        r = utility.calculatle_rvec(step, start)
        options = {1:[step[0]-1,step[1]-1],
                   2:[step[0]-1,step[1]],
                   3:[step[0]-1,step[1]+1],
                   4:[step[0]-1,step[1]],
                   5: step,
                   6:[step[0]+1,step[1]],
                   7:[step[0]+1,step[1]-1],
                   8:[step[0]+1,step[1]],
                   9:[step[0]+1, step[1]+1]}
        for opt in options.values():
            if utility.calculatle_rvec(opt,start) > r:
                step = opt
        correct.append(step)
        steps += 1
    if display:
        print "Made it " + str(steps) + " Steps"
    return steps, correct, dna


def radial_wander(start, depth,generated_maze, show):
    walker_pool_displacement = {}
    disp = 0
    best = 0

    for pt in range(batch_size):
        walk, sequence = utility.spawn_random_walk(start, depth)
        rvec = []
        score = 0
        for step in walk:
            try:
                if generated_maze[step[0], step[1]] == 1:
                    score += 1
            except IndexError:
                pass
            rvec.append(utility.calculatle_rvec(step, start))
        dr = np.diff(np.array(rvec)[1:]) + np.array(rvec)[2:]
        dR = dr[len(dr) - 1] - dr[0]
        if score > best and dR > disp:
            best = score
            disp = dR
            walker_pool_displacement[pt] = walk

    if show:
        print " Best Path: " + str(best)
        print "Total Path length: " + str(len(walk))
        print "Score: " + str(score)
        print "Displacement: " + str(disp)
        genetic_maze_builder.draw_walk(walk, start, generated_maze)
    return walker_pool_displacement, score


start = [20,20]
stop = [248, 28]
batch_size = 200
depth = 100
mgenes, scores = genetic_maze_builder.generate_primitives(36, (6, 6))
maze = genetic_maze_builder.generate_random_col(mgenes,6,10, False)

''' STRATEGIES 
[1] create an expanding search radius of random walks
and mutate these with the solutions that have lived 

[2] using batches of same step sized walks, slowly
evolve towards correct solution. 

[3] Brute Force + Evolution : Random Walks of entire total
radius modified with evolution to help converge slightly 
faster
'''     # TODO: Use a mix of random walking and conv weighted selecting
# TODO: Resplice a sequence instead of terminating it when hitting obstacle ?

radial_wander(start, depth,maze, True)