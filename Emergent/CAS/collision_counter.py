import matplotlib.pyplot as plt
import ColorAutomataSimulations
import numpy as np
import simengine
import time


class CloudChamber:
    configuration = {}
    n_collisions = 0
    collision_data = []
    computation_cost = 0

    def __init__(self, test_config, collisions, tic):
        self.configuration = test_config
        self.n_collisions = len(collisions)
        self.collision_data = collisions
        self.computation_cost = tic

    @staticmethod
    def multivariable_experiment():
        experiment_data = []
        # First Test Three Particle Collisions [R, G, B], even mixes
        for shape in Ws:
            state = np.zeros((shape, shape))
            for ts in Ts:
                for n_particles in SZs:
                    config = {'width': state.shape[0],
                              'height': state.shape[1],
                              'n_particles': n_particles,
                              'timescale': ts,
                              'nRed': n_particles / 3,
                              'nGreen': n_particles / 3,
                              'nBlue': n_particles / 3,
                              'nYellow': 0,
                              'nCyan': 0,
                              'nMagenta': 0,
                              'verbose': True}
                    t0 = time.time()
                    sim = simengine.Engine(config, rgb)
                    collisions = sim.run(rgb, False, False)
                    cc = CloudChamber(config, collisions, time.time() - t0)
                    experiment_data.append(cc)
        '''
        Compare N Collisions to state size

        Compare N Collisions to N Particles / state size  
        '''
        collision_detections = {}
        for k in Ws:
            collision_detections[k] = []
        for test in experiment_data:
            size = test.configuration['width']
            dt = test.computation_cost
            collision_detections[size].append(test.n_collisions)

        plt.plot(collision_detections.keys(), collision_detections.values())
        plt.show()


casm = ColorAutomataSimulations.StandardModel()
rgb = ColorAutomataSimulations.RGB()
Ws = [50, 100, 150, 200, 250]
Ts = [10, 50, 100, 150, 250]
SZs = [20, 50, 100, 200, 500]

nhits = []
timer = []
for size in Ws:
    for n_particles in SZs:
        config = {'width': size,
                  'height': size,
                  'n_particles': 100,
                  'timescale': 100,
                  'nRed': n_particles / 3,
                  'nGreen': n_particles / 3,
                  'nBlue': n_particles / 3,
                  'nYellow': 0,
                  'nCyan': 0,
                  'nMagenta': 0,
                  'verbose': True}
        sim = simengine.Engine(config, rgb)
        tic = time.time()
        collisions = sim.run(rgb, False, False)
        toc = time.time()
        timer.append(toc - tic)
        nhits.append(len(collisions))

plt.plot(nhits)
plt.plot(timer)
plt.show()
