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
    columns[columns.shape[0]-3:columns.shape[0],:] = 0
    if show:
        plt.imshow(columns, 'gray')
        plt.show()

    return columns


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


if __name__ == '__main__':
    main()
