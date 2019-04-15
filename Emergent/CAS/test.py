from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import ColorAutomataSimulations
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import utility as imutil
import numpy as np
import simengine
import time

rgb = ColorAutomataSimulations.RGB()
rgb.initialize()

examplol = np.zeros((6, 6, 3))
examplol[3, 2] = rgb.R
examplol[3, 3] = rgb.G
examplol[2, 3] = rgb.B
examplol[2, 2] = rgb.Y
