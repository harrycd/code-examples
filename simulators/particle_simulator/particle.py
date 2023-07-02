import math


class Particle:
    def __init__(self):
        self.x, self.y, self.z = 0, 0, 0  # coordinates
        self.x0, self.y0, self.z0 = 0, 0, 0  # initial coordinates
        self.vx, self.vy, self.vz = 0, 0, 0  # velocities
        self.fx, self.fy, self.fz = 0, 0, 0  # forces
        self.mass = 1  # mass
        self.radius = 1  # radius of spherical particle
        self.colour = (0, 0, 0)  # colour of representation
        self.neighbours = []    # list of particles
        self.locked = False     # flag to indicate that position should not change

    def get_displacement(self):
        return math.sqrt(
            (self.x - self.x0) * (self.x - self.x0)
            + (self.y - self.y0) * (self.y - self.y0)
            + (self.z - self.z0) * (self.z - self.z0)
        )

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z)
