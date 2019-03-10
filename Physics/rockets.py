import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import utility


class Rocket:
    position = []
    width = 0
    height = 0
    world = [[]]
    trajectory = []
    velocity = 0

    def __init__(self, pos, state, width, height):
        self.position = pos
        self.world = state
        self.width = width
        self.height = height
        #self.initialize()

    def initialize(self):
        self.world[self.position[0] - self.height / 2:self.position[0] + self.height / 2,
        self.position[1] - self.width / 2:self.position[1] + self.width / 2] = 1
        self.trajectory.append(self.position)

    def thrust(self, direction, velocity):
        """
        Thrusters point in the following configs:
                  ^ [-1, 0]
         [0,-11]< + > [0, 1]
                  V
               [1, 0]
        :param direction:
        :param velocity:
        :return:
        """

        self.position = [self.position[0]+velocity*direction[0],
                         self.position[1]+velocity*direction[1]]
        # self.world[self.position[0] - self.height / 2:self.position[0] + self.height / 2,
        #            self.position[1] - self.width / 2:self.position[1] + self.width / 2] = 1
        self.trajectory.append(self.position)

    def draw_trajectoy(self):
        f = plt.figure()
        film = []
        for pos in self.trajectory:
            self.world[pos[0] - self.height / 2:pos[0] + self.height / 2,
                       pos[1] - self.width / 2:pos[1] + self.width / 2] = 1
            film.append([plt.imshow(self.world, 'gray')])
            self.world[pos[0] - self.height / 2:pos[0] + self.height / 2,
            pos[1] - self.width / 2:pos[1] + self.width / 2] = 0

        a = animation.ArtistAnimation(f,film,interval=100,blit=True,repeat_delay=900)
        plt.show()


world = np.zeros((500, 250))
# Add Rocket (size 5,10)
R = Rocket([100,100],world,5,10)

launch = [[1,0],[1,0],[1,0],[1,0],[1,0],[1,1]]
for move in launch:
    R.thrust(move, 10)
R.draw_trajectoy()