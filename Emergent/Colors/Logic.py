import matplotlib.pyplot as plt
import numpy as np
import imutil
import Engine
import colors


class Model:
    particles = {}
    particleInteractionTable = {}
    def __init__(self, configuration):
        