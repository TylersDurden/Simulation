from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import utility
import sys


def predatory_chase(path, opts, complex):
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


def draw_chase(prey_path, pred_path, shape, save, ani):
    f = plt.figure()
    state = np.zeros(shape)
    chase = []
    if len(pred_path) != len(prey_path):
        print "Chase sequence sizes don't match!!"
        print "Prey: " + str(len(prey_path))
        print "Pred: " + str(len(pred_path))
        exit(0)
    else:
        for step in range(len(prey_path)):
            prey = prey_path[step]
            pred = pred_path[step]
            state[prey[0]-2:prey[0]+2, prey[1]-2:prey[1]+2] = -1
            state[pred[0]-2:pred[0]+2, pred[1]-2:pred[1]+2] = 1
            chase.append([plt.imshow(state, 'gray')])
            state[prey[0]-2:prey[0]+2, prey[1]-2:prey[1]+2] = 0
            state[pred[0]-2:pred[0]+2, pred[1]-2:pred[1]+2] = 0
    a = animation.ArtistAnimation(f,chase,interval=50,blit=True,repeat_delay=900)
    if save:
        w = animation.FFMpegWriter(fps=ani['fps'],bitrate=1800)
        a.save(ani['name'], writer=w)
    plt.show()
    return chase


def one_way_chase(prey_start, pred_start):
    prey_seed, gene_sequence = utility.spawn_random_walk(prey_start, 270)
    pred_steps, prey_moves, caught = predatory_chase(prey_seed, {'start': [200, 200]})
    if caught:
        print 'Captured!'
    draw_chase(prey_moves, pred_steps, pred_start, False, {'fps': 50, 'name': 'basic_chase.mp4'})


def complex_chase(prey_start, pred_start, n_steps, activation):
    f = plt.figure()
    prey_seed_steps, sequence = utility.spawn_random_walk(prey_start, n_steps)
    state = np.zeros((250, 250))
    simulation = []
    tracker = []
    scared_prey = False
    for i in range(n_steps):
        if not scared_prey:
            step = prey_seed_steps[i]
            ''' Predator Eval '''
            dx = step[0] - pred_start[0]
            dy = step[1] - pred_start[1]
            r = np.sqrt(dx ** 2 + dy ** 2)
            tracker.append(r)
            if abs(dx) > abs(dy):
                if dx > 0:
                    pred_start = [pred_start[0] + 1, pred_start[1]]
                if dx <= 0:
                    pred_start = [pred_start[0] - 1, pred_start[1]]
                #TODO: dx>0 AND dy<0
                #TODO: dx>0 and dy<0
            if abs(dy) > abs(dx):
                if dy > 0:
                    pred_start = [pred_start[0], pred_start[1] + 1]
                if dy <= 0:
                    pred_start = [pred_start[0], pred_start[1] - 1]
                #TODO: dy>0 AND dx < 0
                #TODO: dy<0 AND dx <0
        else:
            dx = prey_seed_steps[i][0] - pred_start[0]
            dy = prey_seed_steps[i][1] - pred_start[1]
            if abs(dx) > abs(dx):
                if dx >= 0:
                    step = [step[0] - 1, step[1]]
                if dx <= 0:
                    step = [step[0] + 1, step[1]]
                # TODO: dx>0 AND dy<0
                # TODO: dx>0 and dy<0
            if abs(dy) > abs(dx):
                if dy >= 0:
                    step = [step[0], step[1] + 1]
                else:
                    step = [step[0], step[1] - 1]
                # TODO: dy>0 AND dx < 0
                # TODO: dy<0 AND dx <0
            dx = step[0] - pred_start[0]
            dy = step[1] - pred_start[1]
            r = np.sqrt(dx ** 2 + dy ** 2)
            tracker.append(r)
            if abs(dx) > abs(dy):
                if dx > 0:
                    pred_start = [pred_start[0] + 1, pred_start[1]]
                if dx <= 0:
                    pred_start = [pred_start[0] - 1, pred_start[1]]
            if abs(dy) > abs(dx):
                if dy > 0:
                    pred_start = [pred_start[0], pred_start[1] + 1]
                if dy <= 0:
                    pred_start = [pred_start[0], pred_start[1] - 1]

        ''' Prey Evade Sequence '''
        if int(r) == 0:
            print "CAPTURED"
            break
        if r <= activation:
            scared_prey = True
        else:
            scared_prey = False
        try:
            state[step[0] - 2:step[0] + 2, step[1] - 2:step[1] + 2] = -1
            state[pred_start[0] - 2:pred_start[0] + 2, pred_start[1] - 2:pred_start[1] + 2] = 1
            simulation.append([plt.imshow(state, 'gray')])
            state[step[0] - 2:step[0] + 2, step[1] - 2:step[1] + 2] = 0
            state[pred_start[0] - 2:pred_start[0] + 2, pred_start[1] - 2:pred_start[1] + 2] = 0
        except IndexError:
            pass
    a = animation.ArtistAnimation(f,simulation,interval=70,blit=True,repeat_delay=900)
    plt.show()

    plt.close()
    plt.plot(tracker)
    plt.plot(activation*np.ones((len(tracker),1)))
    plt.show()


def main():
    if '-demo' in sys.argv:
        prey_start = [100,130]
        pred_start = [200,200]
        one_way_chase(prey_start, pred_start)
    else:
        # Complex Chase
        prey_start = [50, 50]
        pred_start = [10, 10]
        r = utility.calculatle_rvec(pred_start, prey_start)
        print "Starting Complex Chase with initial Separation of " + str(r)
        complex_chase(prey_start,pred_start, 150, 35)


if __name__ == '__main__':
    main()
