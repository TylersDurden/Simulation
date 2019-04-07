from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def render(frames, frame_rate, save, file_name):
    f = plt.figure()
    film = []
    for frame in frames:
        film.append([plt.imshow(frame, 'gray_r')])
    a = animation.ArtistAnimation(f, film, interval=frame_rate, blit=True, repeat_delay=900)
    if save:
        writer = FFMpegWriter(fps=frame_rate, metadata=dict(artist='Me'), bitrate=1800)
        a.save(file_name, writer=writer)
    plt.show()


def filter_preview(images):
    f, ax = plt.subplots(1, len(images.keys()))
    II = 0
    for image in images.keys():
        ax[II].imshow(images[image], 'gray_r')
        ax[II].set_title(image)
        II += 1
    plt.show()


def spawn_random_point(state):
    # Initialize a random position
    x = np.random.randint(0, state.shape[0], 1, dtype=int)
    y = np.random.randint(0, state.shape[1], 1, dtype=int)
    return [x, y]


def draw_centered_circle(canvas, radius, show):
    cx = canvas.shape[0]/2
    cy = canvas.shape[1]/2
    for x in np.arange(cx - radius, cx + radius, 1):
        for y in np.arange(cy - radius, cy + radius, 1):
            r =np.sqrt((x-cx)*(x-cx) + ((cy-y)*(cy-y)))

            if r <= radius:
                canvas[x, y] = 1
    if show:
        plt.imshow(canvas, 'gray_r')
        plt.show()
    return canvas


def draw_centered_box(canvas, sz, value, show):
    cx = np.array(canvas).shape[0]/2
    canvas = np.array(canvas)
    cy = canvas.shape[1]/2
    canvas[cx-sz:cx+sz,cy-sz:cy+sz] = value

    if show:
        plt.imshow(np.array(canvas), 'gray')
        plt.show()
    return canvas


def get_radius(a, b):
    dx = a[0] = b[0]
    dy = a[1] - b[1]
    return np.sqrt((dx**2) + (dy**2))


def bfs(graph_data, start):
    g = nx.from_dict_of_lists(graph_data)
    path = list()
    queue = [start]
    queued = list()
    while queue:
        vertex = queue.pop()
        for node in graph_data[vertex]:
            if node not in queued:
                queued.append(node)
                queue.append(node)
                path.append([vertex, node])
    return path


def dfs(graph, start):
    stack = [start]
    parents = {start:start}
    path = list()
    while stack:
        vertex = stack.pop(-1)
        for node in graph[vertex]:
            if node not in parents:
                parents[node] = vertex
                stack.append(node)
        path.append([parents[vertex], vertex])
    return path[1:]


def show_bulk_data(data, labels):
    for line in data.values():
        plt.plot(line)
    if 'xlabel' in labels.keys():
        plt.xlabel(labels['xlabel'])
    if 'ylabel' in labels.keys():
        plt.ylabel(labels['ylabel'])
    if 'title' in labels.keys():
        plt.title(labels['title'])
    plt.show()


def show_bulk_subplot(dataA, dataB,labels):
    f, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].grid()
    ax[1].grid()
    for line in dataA.values():
        ax[0].plot(line)
    for l in dataB.values():
        ax[1].plot(l)
    if 'title' in labels['f1'].keys():
        ax[0].set_title(labels['f1']['title'])
    if 'title' in labels['f2'].keys():
        ax[1].set_title(labels['f2']['title'])
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
                      9: [position[0]+1, position[1]+1]}
        position = directions[step]
        random_walk.append(directions[step])
    return random_walk, choice_pool


def ind2sub(index,dims):
    """
    Given an index and array dimensions,
    convert an index to [x,y] subscript pair.
    :param index:
    :param dims:
    :return tuple - subscripts :
    """
    subs = []
    ii = 0
    for y in range(dims[1]):
        for x in range(dims[0]):
            if index==ii:
                subs = [x,y]
                return subs
            ii +=1