import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutil


class PointCloud:
    points = {}
    vectors = {}
    mapping = {}
    state = [[]]
    leaders = []

    def __init__(self, world, cloud, n_leaders, verbosity):
        self.state = world
        self.points = cloud
        self.mapping, self.vectors, ncnxs = PointCloud.connect_cloud(self.points, verbosity)
        self.leaders = self.check_connectivity(n_leaders)

    @staticmethod
    def connect_cloud(cloud, verbose):
        graph = {}
        vects = {}
        n_connections = 0
        for id in cloud.keys():
            connections = []
            radii = []
            for i in cloud.keys():
                if i != id:
                    connections.append(cloud[i])
                    n_connections += 1
                    radii.append(imutil.get_radius(cloud[id], cloud[i]))
            graph[id] = connections
            vects[id] = radii
        if verbose:
            print str(len(graph.keys())) + " Nodes"
            print str(n_connections) + " N Connections Made"
        return graph, vects, n_connections

    def check_connectivity(self, top_n):
        i = 0
        connectivity = {}
        for id in self.mapping.keys():
            rad_mean = np.array(self.vectors[id]).mean()
            connectivity[rad_mean] = id
        top_nodes = []
        connected = np.array(connectivity.keys())
        connected.sort()
        for i in connected[0:top_n]:
            top_nodes.append(connectivity[i])
        return top_nodes

    def update(self, n_steps):
        film = []
        entropy = {}
        for id in self.leaders:
            pt = self.points[id]
            random_steps, seq = imutil.spawn_random_walk(pt, n_steps)
            entropy[id] = random_steps
            # create n_steps of random mov't for ea leader
        # move the leaders in those directions while
        # all others try to optimize their positions
        step = 0
        for pid in self.points.keys():
            if pid in self.leaders:
                move = entropy[pid][step]
                self.state[move[0], move[1]] = 1
            # maximize radius from others, minimize distance from the leaders
            # else:


def main():
    N_PTS = 25
    SIZE = 250
    STATE = np.zeros((SIZE, SIZE))
    cloud = {}

    # Populate with N Random Points
    for pt_id in range(N_PTS):
        pt = imutil.spawn_random_point(STATE)
        STATE[pt[0], pt[1]] = 1
        cloud[pt_id] = pt

    ptc = PointCloud(STATE, cloud, n_leaders=3, verbosity=True)

    for i in range(10):
        ptc.update(5)


if __name__ == '__main__':
    main()
