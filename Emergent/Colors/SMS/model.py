import matplotlib.pyplot as plt
import numpy as np
import engine as e
import utility


class Spectra:
    R = np.array([[]])
    G = np.array([[]])
    B = np.array([[]])
    Y = np.array([[]])
    M = np.array([[]])
    C = np.array([[]])
    K = np.array([[]])
    W = np.array([[]])

    color_handles = {}

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.R = [1,0,0]
        self.G = [0,1,0]
        self.B = [0,0,1]
        self.Y = self.R + self.G
        self.M = self.R + self.B
        self.C = self.B + self.G
        self.K = [0,0,0]
        self.W = [1,1,1]
        self.color_handles = {'r': self.R, 'g': self.G, 'b': self.B,
                         'c': self.C, 'm': self.M, 'y': self.Y,
                         'w': self.W, 'k': self.K}


class StandardModel:
    particle_types = ['R', 'G', 'B',
                      'C', 'M', 'Y',
                      'K', 'W']
    rgb = Spectra

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.rgb = Spectra()




sm = StandardModel()

# Particles should be able to have properties:
#  o  What are their collision rules?
#  o  Maybe each repel or attract some/all others?
#  o  Maybe each have rules about dissipation?
particles = {'r':250, 'b':250}
test_config = {'width': 100,
               'height': 100,
               'timescale': 250,
               'particle_counts': particles}
simulation = e.Engine(test_config)
