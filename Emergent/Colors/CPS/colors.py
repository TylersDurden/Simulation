import matplotlib.pyplot as plt
import numpy as np
import imutil
import Engine
import Logic


class RGB:
    R = [[]]
    G = [[]]
    B = [[]]
    Y = [[]]
    M = [[]]
    C = [[]]
    K = [[]]
    W = [[]]
    handles = {}

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.R = np.zeros((1,1,3))
        self.G = np.zeros((1,1,3))
        self.B = np.zeros((1,1,3))
        self.W = np.ones((1,1,3))
        self.K = np.zeros((1,1,3))
        self.R[:, :, 0] = 1
        self.G[:, :, 1] = 1
        self.B[:, :, 2] = 1
        self.Y = self.R + self.G
        self.M = self.R + self.B
        self.C = self.B + self.G
        self.handles['r'] = self.R
        self.handles['g'] = self.G
        self.handles['b'] = self.B
        self.handles['c'] = self.C
        self.handles['m'] = self.M
        self.handles['y'] = self.Y
        self.handles['k'] = self.K
        self.handles['w'] = self.W


