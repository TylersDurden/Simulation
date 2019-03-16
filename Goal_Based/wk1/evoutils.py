from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
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