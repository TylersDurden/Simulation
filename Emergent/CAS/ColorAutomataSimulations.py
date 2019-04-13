from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import utility
import time


class StandardModel:
    Red = [1, 0, 0]
    Green = [0, 1, 0]
    Blue = [0, 0, 1]
    Purp = [1, 0, 1]
    Yell = [0, 1, 1]
    Teal = [1, 1, 0]
    Black = [0, 0, 0]
    White = [1, 1, 1]

    elementary = ['R', 'G', 'B', 'Y', 'P', 'T']
    operations = ['-', '+']
    events = {}
    rules = {}

    def __init__(self):
        self.events,self.rules = self.initialize()

    def initialize(self):
        event_vectors = {0: ['R', 'G', '+'],    # Red + Green
                         1: ['G', 'B', '+'],    # Green + Blue
                         2: ['P', 'G', '+'],    # Purple + Green
                         3: ['Y', 'R', '+'],    # Yellow + Red
                         4: ['Y', 'G', '+'],    # Yellow + Green
                         5: ['Y', 'P', '+'],    # Yellow + Purple (Green)
                         6: ['Y', 'P', '-'],    # Yellow - Purple (Blue)
                         7: ['T', 'G', '-'],    # Teal - Green (Blue)
                         8: ['T', 'P', '-'],    # Teal - Purple (Green)
                         9: ['Y', 'R', '-'],    # Yellow - Red (Green)
                         10:['Y', 'G', '-']     # Yellow - Green (Red)
                         }

        rules = {0: self.Blue,
                 1: self.Yell,
                 2: self.White,
                 3: self.White,
                 4: self.White,
                 5: self.Green,
                 6: self.Blue,
                 7: self.Blue,
                 8: self.Green,
                 9: self.Green,
                 10: self.Red}
        return event_vectors, rules


class RGB:
    R = [[]]
    G = [[]]
    B = [[]]
    Y = [[]]
    M = [[]]
    C = [[]]

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.R = np.zeros((1,1,3))
        self.G = np.zeros((1,1,3))
        self.B = np.zeros((1,1,3))
        self.R[:,:,0] = 1
        self.G[:,:,1] = 1
        self.B[:,:,2] = 1
        self.Y = self.R + self.G
        self.M = self.R + self.B
        self.C = self.B + self.G


class Particle:
    color = ''
    x = 0
    y = 0
    internal_state = 0

    def __init__(self, color_name, position):
        self.color = color_name
        self.x = position[0]
        self.y = position[1]


def main():
    initial_config = {'width': 250,
                      'height': 250,
                      'n_particles': 300,
                      'nRed': 100,
                      'nGreen': 100,
                      'nBlue': 100,
                      'nYellow': 0,
                      'nMagenta': 0,
                      'nCyan': 0}

    casm = StandardModel()
    rgb = RGB()



if __name__ == '__main__':
    main()
