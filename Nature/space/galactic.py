import matplotlib.pyplot as plt
import numpy as np
import imutil


class Asteroid:
    x = 0
    y = 0
    vx = 0
    vy = 0

    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]

    def set_position(self, position):
        self.x = position[0]
        self.y = position[1]

    def assign_velocity_components(self, vx, vy):
        self.vx = vx
        self.vy = vy


def add_asteroids(state, n):
    astroids = {}
    # Draw an asteroid belt
    for i in range(n):
        point = imutil.spawn_random_point(state)
        state[point[0], point[1]] = 1
        astroids[i] = point
    return state, astroids


def assign_asteroid_velocities(astroid_data, assignments):
    astroids = []
    ii = 0
    for aid in astroid_data.keys():
        apt = astroid_data[aid]
        a = Asteroid(apt)
        [vx, vy] = assignments[ii]
        a.assign_velocity_components(vx, vy)
        astroids.append(a)
        ii += 1
    return a


def main():
    # Basic Simulation Parameters
    width = 350
    height = 400
    n_pts = 500
    world = np.zeros((width, height))

    # Create a large round blob in center
    center_mass = imutil.draw_centered_circle(world, 50, False)
    space, astroids = add_asteroids(center_mass, n_pts)
    # plt.imshow(space, 'gray')
    # plt.show()

    # Register CenterPlanet Location
    # Enable simulation effects


if __name__ == '__main__':
    main()


