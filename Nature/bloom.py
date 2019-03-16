import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import utility
import sys


def convolution_layer(imat, show):

    kernel_1 = [[1, 1, 1, 1],
                [1, 0, 0, 1],
                [1, 0, 0, 1],
                [1, 1, 1, 1]]

    kernel_2 = [[1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1]]

    kernel_3 = [[1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 0, 1],
                [1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1]]

    kernel_4 = [[1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 1, 1],
                [1, 1, 0, 0, 1, 1],
                [1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1]]

    layer = {'n0': ndi.convolve(imat, kernel_1),
             'n1': ndi.convolve(imat, kernel_2),
             'n2': ndi.convolve(imat, kernel_3),
             'n3': ndi.convolve(imat, kernel_4)}
    layer['self'] = imat
    if show:
        utility.filter_preview(layer)
    return layer


seeds = {}
score = {}
n_seeds = 256
for i in range(n_seeds):
    seeds[i+1] = np.random.random_integers(0, 1, 512/2).reshape((16, 16))
    score[i+1] = np.count_nonzero(np.array(seeds[i+1]))


plt.hist(score.values())
plt.show()
