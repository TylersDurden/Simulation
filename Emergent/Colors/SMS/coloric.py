import numpy as np
import utility
import engine
import model


class Spectra:
    R = [[]]
    G = [[]]
    B = [[]]
    Y = [[]]
    M = [[]]
    C = [[]]
    K = [[]]
    W = [[]]

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.R[:, :, 0] = 1
        self.G[:, :, 1] = 1
        self.B[:, :, 2] = 1
        self.Y = self.R + self.G
        self.M = self.R + self.B
        self.C = self.B + self.G
        self.K = np.zeros((1, 1, 3))
        self.W = np.ones((1, 1, 3))
