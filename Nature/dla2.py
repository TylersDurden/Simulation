import numpy as np, utility, sys


def create_start(padding, state, verbose):
    """
    Select random starting point within given
    2D state matrix.
    :param padding:
    :param state:
    :param verbose:
    :return:
    """
    rx = np.random.randint(0 + padding, state.shape[0] - padding, 1)[0]
    ry = np.random.randint(0 + padding, state.shape[1] - padding, 1)[0]
    start = [rx, ry]
    if verbose:
        print start
    return start


def feed_steps_to_state(start, state, steps):
    #history = []
    n = 0
    for step in steps:
        try:
            x = start[0]
            y = start[1]
            state[x, y] = 0
            directions = {1: [x-1, y-1],
                      2: [x, y-1],
                      3: [x+1, y-1],
                      4: [x-1, y],
                      5: [x, y],
                      6: [x+1, y],
                      7: [x-1, y+1],
                      8: [x, y+1],
                      9: [x+1, y+1]}

            # If there's something already there,
            # leave the particle before moving on
        
            next_step = state[directions[step][0],directions[step][1]]
        except IndexError:
            # Out of Bounds!
            break
        if step != 5 and next_step == 1:
            state[x, y] = 1
            #history.append(state)
            break
        elif step != 5:
            start = directions[step]
            #history.append(state)
            if n == len(steps):
                state[start[0], start[1]] = 0
            else:
                state[start[0], start[1]] = 1
        n += 1
    return state


def splice_timeline(series1, series2):
    """
    Sequentially add each element from
    one list [series1] to the end of the
    second list [series2]. Returns the new
    combined list. 
    :param series1: 
    :param series2: 
    :return series2: 
    """
    for item in series1:
        series2.append(item)
    return series2


def draw_square_lattice(state):
    state[30:40, 110:120] = 1
    state[30:40, 130:140] = 1

    state[50:60, 90:100] = 1
    state[50:60, 110:120] = 1
    state[50:60, 130:140] = 1
    state[50:60, 150:160] = 1

    state[70:80, 70:80] = 1
    state[70:80, 90:100] = 1
    state[70:80, 110:120] = 1
    state[70:80, 130:140] = 1
    state[70:80, 150:160] = 1
    state[70:80, 170:180] = 1

    state[90:100, 50:60] = 1
    state[90:100, 70:80] = 1
    state[90:100, 90:100] = 1
    state[90:100, 110:120] = 1
    state[90:100, 130:140] = 1
    state[90:100, 150:160] = 1
    state[90:100, 170:180] = 1
    state[90:100, 190:200] = 1

    state[110:120, 30:40] = 1
    state[110:120, 50:60] = 1
    state[110:120, 70:80] = 1
    state[110:120, 90:100] = 1
    state[110:120, 110:120] = 1
    state[110:120, 130:140] = 1
    state[110:120, 150:160] = 1
    state[110:120, 170:180] = 1
    state[110:120, 190:200] = 1
    state[110:120, 210:220] = 1

    state[130:140, 30:40] = 1
    state[130:140, 50:60] = 1
    state[130:140, 70:80] = 1
    state[130:140, 90:100] = 1
    state[130:140, 110:120] = 1
    state[130:140, 130:140] = 1
    state[130:140, 150:160] = 1
    state[130:140, 170:180] = 1
    state[130:140, 190:200] = 1
    state[130:140, 210:220] = 1

    state[150:160, 50:60] = 1
    state[150:160, 70:80] = 1
    state[150:160, 90:100] = 1
    state[150:160, 110:120] = 1
    state[150:160, 130:140] = 1
    state[150:160, 150:160] = 1
    state[150:160, 170:180] = 1
    state[150:160, 190:200] = 1

    state[170:180, 70:80] = 1
    state[170:180, 90:100] = 1
    state[170:180, 110:120] = 1
    state[170:180, 130:140] = 1
    state[170:180, 150:160] = 1
    state[170:180, 170:180] = 1

    state[190:200, 90:100] = 1
    state[190:200, 110:120] = 1
    state[190:200, 130:140] = 1
    state[190:200, 150:160] = 1

    state[210:220, 110:120] = 1
    state[210:220, 130:140] = 1
    return state


def main():
    n_steps = 150
    n_particles = 5500
    dimensions = [240, 240]
    animated = False
    if '-show' in sys.argv:
        animated = True
        n_particles = 2000
    if '-cm' not in sys.argv:
        center_mass_size = 5
    else:
        center_mass_size = int(input('Enter Box size: '))

    # Numbering scheme for direction keys
    # [[1,2,3],
    #  [4,5,6],
    #  [7,8,9]]
    state = np.zeros(dimensions)
    center_x = int(state.shape[0]) / 2
    center_y = int(state.shape[1]) / 2

    if '-chk' in sys.argv:
        state = draw_square_lattice(state)

    else:
        # Put a box in the center
        state[center_x - center_mass_size:center_x + center_mass_size,
              center_y - center_mass_size:center_y + center_mass_size] = 1

    data = []

    for particle in range(n_particles):
        start = create_start(10, np.zeros((dimensions[0],dimensions[1])), False)
        steps = np.random.randint(1, 9, n_steps)

        # print "Starting from "+str(start)

        state = feed_steps_to_state(start, state, steps)
        data.append(np.array(state))

    print "Simulation completed."
    if animated:
        print "Rendering " + str(len(data)) + " Frames"
        utility.ImageProcessing.render(data, False, 1, False, '')
    else:
        import matplotlib.pyplot as plt
        plt.title('Final State [Generation '+str(n_particles)+']')
        plt.imshow(state, 'gray_r')
        plt.show()


if __name__ == '__main__':
    main()
