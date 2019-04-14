import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndi
import imutil
import Engine
import Logic


class Colors:

    r = np.zeros((1, 1, 3))
    g = np.zeros((1, 1, 3))
    b = np.zeros((1, 1, 3))
    c = np.zeros((1, 1, 3))
    m = np.zeros((1, 1, 3))
    y = np.zeros((1, 1, 3))
    k = np.zeros((1, 1, 3))

    r3 = np.zeros((3, 3, 3))
    g3 = np.zeros((3, 3, 3))
    b3 = np.zeros((3, 3, 3))
    c3 = np.zeros((3, 3, 3))
    m3 = np.zeros((3, 3, 3))
    y3 = np.zeros((3, 3, 3))
    k3 = np.zeros((3, 3, 3))

    def __init__(self):
        self.initialize()
        self.show_colors()

    def initialize(self):
        self.r[:, :, :] = [1, 0, 0]
        self.g[:, :, :] = [0, 1, 0]
        self.b[:, :, :] = [0, 0, 1]
        self.c[:, :, :] = [0, 1, 1]
        self.m[:, :, :] = [1, 0, 1]
        self.y[:, :, :] = [1, 1, 0]

        self.r3[1, 1, :] = [1, 0, 0]
        self.g3[1, 1, :] = [0, 1, 0]
        self.b3[1, 1, :] = [0, 0, 1]
        self.c3[1, 1, :] = [0, 1, 1]
        self.m3[1, 1, :] = [1, 0, 1]
        self.y3[1, 1, :] = [1, 1, 0]

    def show_colors(self):
        f, ax = plt.subplots(2, 3)
        ax[0, 0].imshow(self.r)
        ax[0, 1].imshow(self.g)
        ax[0, 2].imshow(self.b)
        ax[1, 0].imshow(self.c)
        ax[1, 1].imshow(self.m)
        ax[1, 2].imshow(self.y)
        plt.show()


Colors()