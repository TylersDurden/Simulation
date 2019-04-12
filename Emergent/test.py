from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutil
import time


red = np.zeros((1, 1, 3))
green = np.zeros((1, 1, 3))
blue = np.zeros((1, 1, 3))
red[:, :, 0] = 1
green[:, :, 1] = 1
blue[:, :, 2] = 1


def build_cloud(dims, config, show):
    # Load Test Configuration
    n_red = config['nred']
    n_blu = config['nblu']
    n_grn = config['ngrn']

    red_starts = []
    blu_starts = []
    grn_starts = []

    dummy_state = np.zeros(dims)
    # Populate initial particle positions
    [red_starts.append(imutil.spawn_random_point(dummy_state)) for i in range(n_red)]
    [grn_starts.append(imutil.spawn_random_point(dummy_state)) for j in range(n_grn)]
    [blu_starts.append(imutil.spawn_random_point(dummy_state)) for k in range(n_blu)]

    # Draw Cloud
    state = np.zeros((dims[0], dims[1], 3))
    for r in red_starts:
        state[r[0],r[1],:] = red
    for g in grn_starts:
        state[g[0],g[1],:] = green
    for b in blu_starts:
        state[b[0],b[1],:] = blue
    color_cloud = {'r': red_starts, 'g': grn_starts, 'b': blu_starts}
    if show:
        plt.imshow(state)
        plt.show()

    return color_cloud, state


def pad_cloud(width, height, particles):
    initial_state = np.zeros((width + width / 2, height + height / 2, 3))
    initial_state[width / 4:width / 4 + particles.shape[0],
                  height / 4:height / 4 + particles.shape[1], :] = particles[:, :, :]
    return initial_state


def split_cloud(initial_state, show):
    rch = initial_state[:, :, 0]
    gch = initial_state[:, :, 1]
    bch = initial_state[:, :, 2]
    if show:
        f, ax = plt.subplots(1, 4, figsize=(12, 4))
        ax[0].imshow(rch)
        ax[0].set_title('Red Channel')
        ax[1].imshow(gch)
        ax[1].set_title('Green Channel')
        ax[2].imshow(bch)
        ax[2].set_title('Blue Channel')
        ax[3].imshow(initial_state)
        ax[3].set_title('Cloud')
        plt.show()
    return rch, gch, bch


def main():
    t0 = time.time()
    N_RED = 145
    N_GRN = 155
    N_BLU = 145

    RSteps = 10
    GSteps = 10
    BSteps = 10

    width = 120
    height = 120

    red_activation = 4
    green_activation = 4
    blue_activation = 3

    k0 = [[1,1,1],
          [1,1,1],
          [1,1,1]]

    k2 = [[1,1,1,1],
          [1,0,0,1],
          [1,0,0,1],
          [1,1,1,1]]

    test_config = {'nred': N_RED,
                   'ngrn': N_GRN,
                   'nblu': N_BLU,
                   'gsteps': GSteps,
                   'bsteps': BSteps,
                   'rsteps': RSteps}

    cloud, particles = build_cloud([100, 100], config=test_config, show=False)
    state = pad_cloud(width, height, particles)
    dims = state.shape
    rch, gch, bch = split_cloud(state, False)
    initial_state = state  # Save for later
    n = len(np.array(rch).flatten())

    print 'Starting Simulation \033[1m\033[31m['+str(time.time()-t0)+'s Elapsed]\033[0m'
    f = plt.figure()
    film = list()
    film.append([plt.imshow(state)])
    step = 0
    try:
        for step in range(10):
            rch = state[:, :, 0]
            gch = state[:, :, 1]
            bch = state[:, :, 2]

            state = np.zeros(dims)
            world = np.zeros(dims)
            state[:, :, 0] = ndi.convolve(np.array(rch), k0)
            state[:, :, 1] = ndi.convolve(np.array(gch), k0)
            state[:, :, 2] = ndi.convolve(np.array(bch), k0)
            for i in range(n):
                [x, y] = imutil.ind2sub(i, dims)
                red_cell = state[x, y, 0]
                grn_cell = state[x, y, 1]
                blu_cell = state[x, y, 2]
                if red_cell >= red_activation and grn_cell < green_activation and blu_cell < blue_activation:
                    world[x, y, :] = [0, 1, 0]
                if grn_cell >= green_activation and red_cell < red_activation and blu_cell < blue_activation:
                    world[x, y, :] = [0, 0, 1]
                if blu_cell >= blue_activation and red_cell < red_activation and grn_cell < green_activation:
                    world[x, y, :] = [1, 0, 0]
            film.append([plt.imshow(world)])
    except KeyboardInterrupt:
        print '\033[1m'+str(step) + '\033[0m Steps Simulated \033[1m\033[31m'+str(time.time()-t0)+'s Elapsed'
        pass

    print 'Rendering Simulation \033[1m\033[31m['+str(time.time()-t0)+'s Elapsed]\033[0m'
    a = animation.ArtistAnimation(f, film, interval=750, blit=True, repeat_delay=900)
    w = FFMpegWriter(fps=2, bitrate=1800)
    a.save('cas_k1.mp4', writer=w)
    print 'Finished \033[1m\033[31m['+str(time.time()-t0)+'s Elapsed]\033[0m'
    plt.show()
    plt.imshow(initial_state)
    plt.title('Initial State')
    plt.show()


if __name__ == '__main__':
    main()
