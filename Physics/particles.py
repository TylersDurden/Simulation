import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
import matplotlib.pyplot as plt
import numpy as np
import utility
import time


def spawn_random_walk_pool(world, pool_size, walk_length):
    data = {}
    for i in range(pool_size):
        pt = utility.spawn_random_point(world)
        walk, seq = utility.spawn_random_walk([pt[0], pt[1]], walk_length)
        data[i] = walk
    return data


def spawn_walk_pool_common_origin(pool_size, walk_length, start):
    data = {}
    for i in range(pool_size):
        walk, seq = utility.spawn_random_walk([start[0], start[1]], walk_length)
        data[i] = walk
    return data


def draw_walks_in_parallel(walk_data, state, erase, save):
    f = plt.figure()
    film = []

    nk = len(walk_data.keys())
    ns = len(walk_data[walk_data.keys().pop()])
    print "N Walkers: " + str(nk)
    print "N Steps: " + str(ns)

    for i in range(ns):
        for step in range(nk):
            if erase and i>=1:
                try:
                    s = walk_data[step][i-1]
                    state[s[0], s[1]] = 0
                except IndexError:
                    pass
            try:
                step = walk_data[step][i]
                state[step[0], step[1]] = 1
            except IndexError:
                pass
        film.append([plt.imshow(state, 'gray')])
    a = animation.ArtistAnimation(f,film,interval=40,blit=True,repeat_delay=900)
    if save['do']:
        w = FFMpegWriter(fps=save['fps'],bitrate=1800)
        a.save(save['name'],w)
    plt.show()
    plt.close()
    return film


t0 = time.time()
world = np.zeros((150, 150))
pool_size = 250
n_steps = 250

random_walks_common = spawn_walk_pool_common_origin(pool_size, n_steps, [105, 105])
random_walks = spawn_random_walk_pool(np.zeros((50,50)),pool_size,n_steps)

print 'Finished. ['+str(time.time()-t0)+'s Elapsed]'
print 'Rendering Simulation 1'
datar = draw_walks_in_parallel(random_walks, world, True, {'do':False,'fps':20,'name':'randomly.mp4'})
plt.close()
print 'Rendering Simulation 2'
common_meta = {'do': True, 'fps': 20, 'name': 'common_origin_fireflies.mp4'}
datac = draw_walks_in_parallel(random_walks_common, np.zeros((250, 250)), True, common_meta)