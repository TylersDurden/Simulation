import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import time

R = np.zeros((1,1,3))
G = np.zeros((1,1,3))
B = np.zeros((1,1,3))
R[:,:,0] = 1
G[:,:,1] = 1
B[:,:,2] = 1


def build_cloud(dims,config):
    n_red = config['nred']
    n_blu = config['nblu']
    n_grn = config['ngrn']

    red_starts = {}   # Cloud dictionaries of
    blu_starts = {}   # initial states
    grn_starts = {}

    




N_RED = 20
N_GRN = 20
N_BLU = 0

width = 250
height = 250
