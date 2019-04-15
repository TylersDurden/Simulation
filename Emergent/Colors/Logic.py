import matplotlib.pyplot as plt
import numpy as np
import imutil
import Engine
import colors


class Model:
    particleInteractionTable = {}
    standard_model = {}
    particleIdVector = []
    particleCount = {}
    dimensions = []
    particles = {}

    def __init__(self, configuration):
        self.initialize(configuration)

    def initialize(self, configuration):
        """ ::  Initialize ::
        example configuration ->
        config = {'piv': ['R','G','B','C','M','Y'],
                  'shape': [width, height]
                  'particle_count': {1:100, 2:10}, (-> 100 Red and 10 Green)
                 }
        :param configuration:
        :return:
        """
        self.particleIdVector = configuration['piv']   # [ 'R','G','B',.. etc]
        self.dimensions = configuration['shape']
        self.particleCount = configuration['particle_count']

        self.particleInteractionTable = {'1-2':6,
                                         '1-3':5,
                                         '1-4':8,
                                         '1-5':[],
                                         '1-6':[],
                                         '1-7':1,
                                         '2-3':4,
                                         '2-4':[],
                                         '2-5':8,
                                         '2-6':[],
                                         '2-7':2,
                                         '3-4':[],
                                         '3-5':[],
                                         '3-6':8,
                                         '3-7':3,
                                         '4-5':8,
                                         '4-6':8,
                                         '4-7':4,
                                         '5-6':8,
                                         '5-7':5,
                                         '6-7':6}
        self.standard_model = {1: [1, 0, 0],
                               2: [0, 1, 0],
                               3: [0, 0, 1],
                               4: [0, 1, 1],
                               5: [1, 0, 1],
                               6: [1, 1, 0],
                               7: [0, 0, 0],
                               8: [1, 1, 1]}
