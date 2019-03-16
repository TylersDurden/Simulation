from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np


def get_separation(a, b):
    """
    Return the Distance of a straight line
    between given points a and b.
    :param a:
    :param b:
    :return:
    """
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    return np.sqrt((dx**2)+(dy**2))


def show_bulk_data(data):
    for line in data.values():
        plt.plot(line)
    plt.show()


def spawn_random_point(state):
    # Initialize a random position
    x = np.random.randint(0, state.shape[0], 1, dtype=int)
    y = np.random.randint(0, state.shape[1], 1, dtype=int)
    return [x, y]


def bw_render(frames, frame_rate, save, fileNameOut):
    f = plt.figure()
    film = []
    for frame in frames:
        film.append([plt.imshow(frame, 'gray_r')])
    a = animation.ArtistAnimation(f, film, interval=frame_rate, blit=True, repeat_delay=900)
    if save:
        writer = FFMpegWriter(fps=frame_rate, metadata=dict(artist='Me'), bitrate=1800)
        a.save(fileNameOut, writer=writer)
    plt.show()


def spawn_random_walk(position, n_steps):
    choice_pool = np.random.randint(1, 10, n_steps)
    random_walk = list()
    for step in choice_pool:
        directions = {1: [position[0]-1, position[1]-1],
                      2: [position[0]-1, position[1]],
                      3: [position[0]-1, position[1]+1],
                      4: [position[0], position[1]-1],
                      5: position,
                      6: [position[0], position[1]+1],
                      7: [position[0]+1, position[1]-1],
                      8: [position[0]+1, position[1]],
                      9: [position[0]+1, position[0]+1]}
        random_walk.append(directions[step])
        position = directions[step]
    return random_walk, choice_pool


def generate_random_pool(settings):
    seed_data = {}
    random_displacements = {}
    dna = {}
    verbose = False
    if 'print_outs' in settings.keys():
        verbose = settings['print_outs']
    batch_size = settings['pool_size']
    walk_length = settings['walk_length']
    for pool_id in range(batch_size):
        step = settings['start']
        steps = []
        displacement = []
        raw_data = []
        for s in np.random.random_integers(1,9,walk_length).flatten():
            options = {1: [step[0] - 1, step[1] - 1],
                       2: [step[0] - 1, step[1]],
                       3: [step[0] - 1, step[1] + 1],
                       4: [step[0] - 1, step[1]],
                       5: step,
                       6: [step[0] + 1, step[1]],
                       7: [step[0] + 1, step[1] - 1],
                       8: [step[0] + 1, step[1]],
                       9: [step[0] + 1, step[1] + 1]}
            step = options[s]
            raw_data.append(s)
            steps.append(options[s])
            displacement.append(get_separation(settings['start'], options[s]))
        seed_data[pool_id] = steps
        random_displacements[pool_id] = displacement
        dna[pool_id] = raw_data
    n_steps_total = len(seed_data.keys())*len(seed_data.values())
    if verbose:
        print '\033[1mN Batches: '+str(batch_size)
        print 'Walk Length: ' + str(walk_length)
        print str(n_steps_total) + ' Steps Total\033[0m'
    return dna, seed_data, random_displacements


def pool_initialization(settings, batches):
    genetics = {}
    external = {}
    for i in range(batches):
        DNA, seed_pool, walk_traces = generate_random_pool(settings)
        genetics[i] = DNA
        external[i] = seed_pool

    return genetics, external


def generate_random_landscape(M, N, bit_depth):
    test = np.random.random_integers(0, bit_depth, M*N).reshape((M, N))
    reduction = [[1,1,1,1,1],
                 [1,1,1,1,1],
                 [1,1,0,1,1],
                 [1,1,1,1,1],
                 [1,1,1,1,1]]
    t0 = ndi.convolve(test, reduction, origin=0)
    return t0

