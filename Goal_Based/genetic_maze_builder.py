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


def generate_random_col(primitives,depth, ncols):
    columns = np.zeros((primitives[0].shape[0]*depth,ncols*primitives[0].shape[0]))
    for i in range(ncols):
        col = primitives[-1]
        for j in np.random.random_integers(0, 10, depth):
            col = np.array(np.concatenate((col, primitives[j - 1]), 0))
        columns[:,3*i:3*i+3] = col[:-3,:]
    # Add Padding
    columns[:,0:3] = 0
    columns[:,columns.shape[1] - 3:columns.shape[1]] = 0
    columns[columns.shape[0]-3:columns.shape[0],:] = 0
    plt.imshow(columns, 'gray')
    plt.show()

    return columns


N = 12
psize = np.zeros((3,3)).shape
primitives, scores = generate_primitives(10, psize)
generated_maze = generate_random_col(primitives,N,N)


