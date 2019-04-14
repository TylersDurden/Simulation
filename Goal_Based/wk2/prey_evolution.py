from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import utility
import time
import sys

R = np.zeros((1,1,3))
G = np.zeros((1,1,3))
B = np.zeros((1,1,3))
R[:,:,0] = 1
G[:,:,1] = 1
B[:,:,2] = 1


def spawn_walk_pool_common_origin(pool_size, walk_length, start):
    data = list()
    [data.append(utility.spawn_random_walk(start,walk_length)) for walk in range(pool_size)]
    return data


def predatory_chase(path, opts):
    """
    :: Predatory_Chase ::
    Given the path of given prey, and some chase
    parameter options (opts), this function starts
    from the given arbitrary location and using the
    the same number of steps as the prey, a predator
    attempts to catch the prey.
    ================== Example Usage ====================
    predatory_chase(prey_seed, {'start': predator_start})
    =====================================================
    :param path:
    :param opts:
    :return predatorPath []
    :return preyPath []
    :return captured bool
    """
    start = opts['start']
    tracker = []
    chase = []
    follow = []
    captured = False
    for step in path:
        dx = step[0]-start[0]
        dy = step[1]-start[1]
        r = np.sqrt(dx**2 + dy**2)
        tracker.append(r)
        if np.abs(dx) > np.abs(dy):
            if dx < 0:
                start = [start[0]-1, start[1]]
            if dx > 0:
                start = [start[0]+1, start[1]]
        if abs(dx) < abs(dy):
            if dy > 0:
                start = [start[0], start[1]+1]
            if dy < 0:
                start = [start[0], start[1]-1]
        chase.append(start)
        follow.append(step)
        if r == 0:
            captured = True
            break
    return chase, follow, captured


def simulate_n_generations(dims, origin, pool):
    fitness = {}
    state = np.zeros((dims[0],dims[1],3))
    n_gens = len(pool)
    n_steps = len(pool[0])
    captures = {}
    failures = {}
    successful = 0
    fails = 0
    for gen in range(n_gens):
        prey_steps = pool[gen]
        predator = {'start': utility.spawn_random_point(np.zeros(dims)),
                    'pid':gen}
        pred_moves, evade, captured = predatory_chase(prey_steps, predator)
        if captured:
            successful += 1
            captures[successful] = [prey_steps, pred_moves]
        else:
            failures[fails] = [prey_steps, pred_moves]
            fails += 1
    print '\033[1m'+str(float((successful*100)/n_gens)) + \
          "%\033[0m of Generations \033[1m\033[31mCaptured\033[0m"

    return fitness, captures, fails


def main():
    save = False
    width = 150
    height = 150
    prey_start = [10, 30]

    pooling = 100
    n_steps = 105

    generation = spawn_walk_pool_common_origin(pool_size=pooling,
                                               walk_length=n_steps,
                                               start=prey_start)
    fitness, captures, failures = simulate_n_generations([width, height], prey_start, generation)

    if 'save' in sys.argv:
        save = True
        file_name = str(raw_input('\033[1m\033[37mEnter Name for saved Animation: \033[0m'))
    if 'show_success' in sys.argv:
        f = plt.figure()
        film = list()
        for i in range(len(captures.keys())):
            test_prey = captures[1][0]
            test_pred = captures[1][1]
            state = np.zeros((width, height, 3))
            plt.title('CAPTURES')
            for step in range(len(test_pred)):
                prey = test_prey[step]
                pred = test_pred[step]
                state[prey[0]-2:prey[0], prey[1]-2:prey[1], :] = B
                state[pred[0], pred[1], :] = R
                film.append([plt.imshow(state)])
                state[prey[0]-2:prey[0], prey[1]-2:prey[1], :] = 0
                state[pred[0], pred[1], :] = 0
            state[pred[0], pred[1], :] = G
            film.append([plt.imshow(state)])
            film.append([plt.imshow(state)])
        a = animation.ArtistAnimation(f, film, interval=50, blit=True, repeat_delay=1900)
        if save:
            w = FFMpegWriter(fps=50,bitrate=1800)
            a.save(file_name,writer=w)
        plt.show()
        plt.close()


if __name__ == '__main__':
    main()
